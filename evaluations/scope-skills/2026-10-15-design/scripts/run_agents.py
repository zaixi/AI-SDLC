"""Add the current global AGENTS.md as one content-only comparison condition."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
import argparse
import copy
import json

import run as core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-root", required=True, type=Path)
    args = parser.parse_args()
    root = core.ROOT
    report = root / "global-agents"
    if (report / "protocol.json").exists():
        raise RuntimeError("Existing condition must not be overwritten")
    parent = json.loads((root / "protocol.json").read_text())
    for rel, digest in parent["frozen_hashes"].items():
        assert core.sha((root / rel).read_bytes()) == digest, rel
    raw = args.raw_root.resolve()
    raw.mkdir(parents=True, exist_ok=False)
    source = Path.home() / ".codex/AGENTS.md"
    data = source.read_bytes()
    snapshot = raw / "snapshots/global-agents/AGENTS.md"
    snapshot.parent.mkdir(parents=True)
    snapshot.write_bytes(data)
    cases = {c["id"]: c for c in json.loads((root / "inputs/cases.json").read_text())["cases"]}
    protocol = copy.deepcopy(parent)
    for key in ["initial_attempt", "budget_calibration", "generation_script_sha256", "post_run_script_change"]:
        protocol.pop(key, None)
    protocol.update(
        created_utc=datetime.now(timezone.utc).isoformat(),
        parent_protocol="../protocol.json",
        raw_root=str(raw),
        sources={"global-agents": {"source_path": str(source), "files": [{"path": "AGENTS.md", "sha256": core.sha(data)}]}},
        jobs=[{"id": case + "-global-agents", "condition": "global-agents", "case": case} for case in cases],
        activation="AGENTS.md text injected with the same user-message skill-file wrapper as prior conditions; no native Codex loading",
        references="Only the current global AGENTS.md; referenced workflow skills are not loaded",
        comparison="Later supplementary batch; earlier 12 cells retained unchanged, no combined skill plus AGENTS condition",
        frozen_hashes={"../" + p: core.sha((root / p).read_bytes()) for p in ["inputs/cases.json", "RUBRIC.md", "scripts/run.py", "scripts/run_agents.py"]},
    )
    core.save(report / "protocol.json", protocol)
    core.save(raw / "protocol.json", protocol)
    opts = core.provider()
    with ThreadPoolExecutor(max_workers=protocol["concurrency"]) as pool:
        futures = [pool.submit(core.execute, job, protocol, opts, cases) for job in protocol["jobs"]]
        results = [f.result() for f in as_completed(futures)]
    core.save(raw / "results.json", sorted(results, key=lambda r: r["id"]))


if __name__ == "__main__":
    main()
