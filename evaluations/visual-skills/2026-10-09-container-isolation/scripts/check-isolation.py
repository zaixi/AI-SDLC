#!/usr/bin/env python3
"""Check container file access; optional CLI smoke test, never a skill benchmark.

Requires Docker and Python's standard library. Credentials and raw CLI diagnostics
remain outside the repository. No model selection or shared agent daemon is used.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import uuid


def run(args, **kwargs):
    return subprocess.run(args, check=True, text=True, capture_output=True, **kwargs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-smoke", action="store_true")
    parser.add_argument("--result", type=Path, required=True)
    options = parser.parse_args()
    report = {"benchmark_answers": 0, "model_smoke_requested": options.model_smoke}
    context = Path(__file__).resolve().parent
    # Isolate Docker's own writable config from the host's read-only home.
    with tempfile.TemporaryDirectory(prefix="visual-file-isolation-") as scratch:
        root = Path(scratch)
        assigned = root / "assigned"
        assigned.mkdir()
        (assigned / "visible.txt").write_text("isolated-probe-readable\n")
        peer = root / "peer-only.txt"
        peer.write_text("not-mounted\n")
        docker = ["docker", "--config", str(root / "docker-config")]
        image = "visual-skill-file-check:local"
        run(docker + ["build", "-t", image, str(context)])
        image_id = run(docker + ["image", "inspect", "--format", "{{.Id}}", image]).stdout.strip()
        base = docker + ["run", "--rm", "--user", "1000:1000",
                         "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
                         "--read-only", "--tmpfs", "/tmp:rw,nosuid,size=128m",
                         "--mount", f"type=bind,src={assigned},dst=/input,readonly"]
        shell = '''set -eu
test "$(cat /input/visible.txt)" = isolated-probe-readable
test ! -e "$1"
test ! -e /workspace/AI-SDLC
test ! -e /var/run/docker.sock
if touch /input/write-check 2>/dev/null; then exit 1; fi
echo filesystem-checks-passed
'''
        check = run(base + ["--network", "none", image, "sh", "-c", shell, "probe", str(peer)])
        report["filesystem"] = {
            "image_id": image_id,
            "assigned_file_readable": True,
            "peer_host_file_absent": True,
            "host_repository_absent": True,
            "docker_socket_absent": True,
            "assigned_mount_readonly": True,
            "network": "none",
            "check_output": check.stdout.strip(),
        }
        if options.model_smoke:
            # Resolve the existing runtime auth file without displaying its path
            # or contents. It is mounted read-only, never copied into the image.
            runtime_home = os.environ.get("CODEX_HOME")
            auth = Path(runtime_home) / "auth.json" if runtime_home else Path.home() / ".codex/auth.json"
            binary = shutil.which("codex")
            if not binary or not auth.is_file():
                report["model_smoke"] = {"status": "not_run", "reason": "CLI or auth file absent"}
            else:
                cli = Path(binary).resolve()
                args = base + ["--tmpfs", "/home/tester:rw,nosuid,uid=1000,gid=1000,mode=700",
                               "--tmpfs", "/home/tester/.codex:rw,nosuid,uid=1000,gid=1000,mode=700",
                               "--mount", f"type=bind,src={auth},dst=/home/tester/.codex/auth.json,readonly",
                               "--mount", f"type=bind,src={cli},dst=/usr/local/bin/codex,readonly"]
                code_host = cli.with_name("codex-code-mode-host")
                if code_host.is_file():
                    args += ["--mount", f"type=bind,src={code_host},dst=/usr/local/bin/codex-code-mode-host,readonly"]
                # Only the existing proxy route is forwarded. In particular, no
                # host exec-server endpoint, thread/session IDs or socket mounts.
                for name in ("HTTPS_PROXY", "HTTP_PROXY", "NO_PROXY"):
                    if name in os.environ:
                        args += ["--env", name]
                if os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY"):
                    from urllib.parse import urlsplit
                    route = urlsplit(os.environ.get("HTTPS_PROXY") or os.environ["HTTP_PROXY"])
                    if route.hostname:
                        args += ["--add-host", f"{route.hostname}:{socket.gethostbyname(route.hostname)}"]
                cert_name = os.environ.get("CODEX_PROXY_CERT")
                if cert_name and Path(cert_name).is_file():
                    args += ["--mount", f"type=bind,src={cert_name},dst=/etc/ssl/certs/platform.pem,readonly",
                             "--env", "SSL_CERT_FILE=/etc/ssl/certs/platform.pem"]
                prompt = ("Use a local file tool to read /input/visible.txt and check that "
                          "/workspace/AI-SDLC does not exist. Reply with only those results. "
                          "Do not read authentication files or use network tools.")
                container_name = "visual-cli-check-" + uuid.uuid4().hex
                args += ["--name", container_name, image, "codex", "--no-daemon", "exec", "--ephemeral",
                         "--ignore-user-config", "--skip-git-repo-check", "--sandbox", "read-only",
                         "-C", "/input", "--json", prompt]
                try:
                    result = subprocess.run(args, text=True, capture_output=True, stdin=subprocess.DEVNULL, timeout=120)
                    # Whitelisted diagnostic categories only, no raw output or credentials.
                    diagnostics = result.stdout + result.stderr
                    errors = []
                    if "401" in diagnostics or "access token could not be refreshed" in diagnostics:
                        errors.append("authentication_rejected")
                    if "451" in diagnostics:
                        errors.append("auxiliary_service_rejected")
                    if "Code Mode is unavailable" in diagnostics:
                        errors.append("code_mode_unavailable")
                    report["model_smoke"] = {
                        "status": "cli_finished" if result.returncode == 0 else "failed",
                        "exit_code": result.returncode,
                        "diagnostic_categories": errors,
                        "code_mode_host_mounted": code_host.is_file(),
                        "network": "Docker bridge, existing proxy; not egress isolated",
                        "note": "A zero exit code alone does not prove local tool execution; this is not a benchmark.",
                    }
                except subprocess.TimeoutExpired:
                    report["model_smoke"] = {"status": "timeout", "benchmark_answers": 0}
                finally:
                    # A timed-out Docker client can leave its container running.
                    subprocess.run(docker + ["rm", "--force", container_name],
                                   text=True, capture_output=True, timeout=15)
    options.result.parent.mkdir(parents=True, exist_ok=True)
    options.result.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
