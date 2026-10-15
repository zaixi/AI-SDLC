"""Compare explicitly supplied skill text on frozen, self-contained design tasks.

Uses the existing OpenCode provider through its configuration command; never
writes authentication to evaluation artifacts. No agent tools or host files are
available to the tested model. Raw requests/results live outside the repository.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import json
import random
import subprocess
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "boring-engineering": ("alvindemesadev/boring-engineering", "main", [
        "SKILL.md", "references/decision-framework.md", "assets/decision-tree.md",
        "examples/bad-abstractions.md", "examples/before-after.md",
    ]),
    "yagni": ("microsoft/agentic-loops", "master", [
        "skills/yagni/SKILL.md", "docs/meta-design.md",
    ]),
    "karpathy-guidelines": ("forrestchang/andrej-karpathy-skills", "main", [
        "skills/karpathy-guidelines/SKILL.md",
    ]),
}


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "AI-SDLC-scope-evaluation"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read()


def prepare(raw, model):
    if (ROOT / "protocol.json").exists():
        raise RuntimeError("Protocol already exists; use a new evaluation directory")
    raw.mkdir(parents=True, exist_ok=True)
    if any(raw.iterdir()):
        raise RuntimeError("Raw directory must be empty")
    sources = {}
    for condition, (repo, branch, files) in SOURCES.items():
        remote = subprocess.run(["git", "ls-remote", "--heads", f"https://github.com/{repo}.git", branch],
                                capture_output=True, text=True, check=True, timeout=60)
        commit = remote.stdout.split()[0]
        records = []
        for rel in files:
            url = f"https://raw.githubusercontent.com/{repo}/{commit}/{rel}"
            content = get(url)
            path = raw / "snapshots" / condition / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            records.append({"path": rel, "url": url, "sha256": sha(content)})
        sources[condition] = {"repo": repo, "commit": commit, "files": records}
    cases = json.loads((ROOT / "inputs/cases.json").read_text())["cases"]
    jobs = []
    for case in cases:
        order = ["none", *SOURCES]
        random.Random("scope-design-20261015-" + case["id"]).shuffle(order)
        jobs.extend({"id": case["id"] + "-" + c, "condition": c, "case": case["id"]} for c in order)
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "model": model, "reasoning_effort": "high", "max_tokens": 32768,
        "repeats": 1, "concurrency": 2, "request_timeout_seconds": 240,
        "stream_wall_limit_seconds": 600,
        "temperature": "provider default; not set", "seed": "not set",
        "execution": "Direct streaming chat/completions through existing OpenCode provider",
        "activation": "Full SKILL.md and listed local text references explicitly supplied in user message",
        "isolation": "Fresh two-message request, neutral system, no tools, no host instructions, no other answers/rubric",
        "references": "Supplied upfront, not on-demand; external design links included for yagni; diagram rules omitted because no diagram is required",
        "review": "Manual nonblind, fixed rubric; no feedback or automatic retries",
        "raw_root": str(raw), "sources": sources, "jobs": jobs,
        "frozen_hashes": {p: sha((ROOT / p).read_bytes()) for p in ["inputs/cases.json", "RUBRIC.md", "scripts/run.py"]},
    }
    save(ROOT / "protocol.json", protocol)
    save(raw / "protocol.json", protocol)
    print(json.dumps({"prepared": len(jobs), "raw_root": str(raw)}, ensure_ascii=False), flush=True)


def provider():
    # Existing repository evaluation mechanism, with all config output suppressed.
    result = subprocess.run([str(Path.home() / ".opencode/bin/opencode"), "debug", "config", "--pure"],
                            cwd="/tmp", capture_output=True, text=True, timeout=45)
    for i, ch in enumerate(result.stdout):
        if ch == "{":
            try:
                value, _ = json.JSONDecoder().raw_decode(result.stdout[i:])
                if isinstance(value, dict) and "provider" in value:
                    return value["provider"]["llmproxy"]["options"]
            except ValueError:
                pass
    raise RuntimeError("Existing provider unavailable; configuration suppressed")


def execute(job, protocol, opts, cases):
    raw = Path(protocol["raw_root"])
    run = raw / "runs" / job["id"]
    run.mkdir(parents=True, exist_ok=False)
    text = ""
    if job["condition"] != "none":
        text = "请在本题中应用以下 skill。其文件及参考资料已提供，无需另行读取。\n"
        for item in protocol["sources"][job["condition"]]["files"]:
            path = raw / "snapshots" / job["condition"] / item["path"]
            assert sha(path.read_bytes()) == item["sha256"]
            text += f"\n<skill-file path={json.dumps(item['path'])}>\n{path.read_text()}\n</skill-file>\n"
    text += "\n当前任务：\n" + cases[job["case"]]["prompt"]
    body = {"model": protocol["model"], "reasoning_effort": protocol["reasoning_effort"],
            "max_tokens": protocol["max_tokens"], "stream": True, "stream_options": {"include_usage": True},
            "messages": [{"role": "system", "content": "You are an assistant. Complete the user task accurately. Respond in Chinese."},
                         {"role": "user", "content": text}]}
    save(run / "request.json", body)
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + opts["apiKey"]}
    headers.update(opts.get("headers", {}))
    request = urllib.request.Request(opts["baseURL"].rstrip("/") + "/chat/completions",
                                     data=json.dumps(body).encode(), headers=headers, method="POST")
    start = time.monotonic()
    summary = dict(job)
    try:
        content, reasoning, usage, finish, model = [], [], {}, None, None
        with urllib.request.urlopen(request, timeout=protocol["request_timeout_seconds"]) as response, (run / "stream.txt").open("wb") as stream:
            for line in response:
                stream.write(line)
                if time.monotonic() - start > 600:
                    raise TimeoutError("Streaming wall limit")
                if not line.startswith(b"data: ") or line.strip() == b"data: [DONE]":
                    continue
                event = json.loads(line[6:])
                model = event.get("model", model)
                usage = event.get("usage") or usage
                for choice in event.get("choices", []):
                    delta = choice.get("delta", {})
                    content.append(delta.get("content") or "")
                    reasoning.append(delta.get("reasoning_content") or "")
                    finish = choice.get("finish_reason") or finish
        value = {"model": model, "usage": usage, "choices": [{"finish_reason": finish,
                 "message": {"content": "".join(content), "reasoning_content": "".join(reasoning)}}]}
        save(run / "response.json", value)
        answer = value["choices"][0]["message"].get("content") or ""
        (run / "answer.md").write_text(answer)
        summary.update(status="ok" if answer else "empty", finish_reason=value["choices"][0].get("finish_reason"),
                       returned_model=value.get("model"), usage=value.get("usage", {}), answer_chars=len(answer),
                       answer_sha256=sha(answer.encode()))
    except Exception as error:
        # Do not serialize exception messages: provider URLs may contain credentials.
        summary.update(status="failed", error_type=type(error).__name__, http_status=getattr(error, "code", None))
    summary["seconds"] = round(time.monotonic() - start, 2)
    save(run / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["prepare", "run"])
    parser.add_argument("--raw-root", type=Path)
    parser.add_argument("--model", default="deepseek-flash")
    args = parser.parse_args()
    if args.mode == "prepare":
        if args.raw_root is None:
            parser.error("prepare requires --raw-root")
        prepare(args.raw_root.resolve(), args.model)
        return
    protocol = json.loads((ROOT / "protocol.json").read_text())
    for rel, digest in protocol["frozen_hashes"].items():
        assert sha((ROOT / rel).read_bytes()) == digest, rel
    cases = {c["id"]: c for c in json.loads((ROOT / "inputs/cases.json").read_text())["cases"]}
    opts = provider()
    with ThreadPoolExecutor(max_workers=protocol["concurrency"]) as pool:
        futures = [pool.submit(execute, job, protocol, opts, cases) for job in protocol["jobs"]]
        results = [f.result() for f in as_completed(futures)]
    save(Path(protocol["raw_root"]) / "results.json", sorted(results, key=lambda r: r["id"]))


if __name__ == "__main__":
    main()
