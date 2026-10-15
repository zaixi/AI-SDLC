# Frozen execution rubric

Two synthetic runnable Python repositories, original vs revised AGENTS, one attempt per cell; deepseek-flash/high. Not native Codex loading. Offline tools; no other skills, prior answers or review files exposed.

Assess required behavior independently of scope. Record all changes, new public interfaces/options/dependencies, recovery semantics and their demonstrated need. File/line counts and verbosity alone do not determine quality. Necessary atomicity, safe migration, timeout and overlap protection are not overengineering. No absolute winner from four samples.

E01: atomic imports, precision-preserving decimal comparison, date conflicts, idempotence, safe historical duplicates, persistent uniqueness, overlapping calls and bounded 503 recovery. Existing function and CLI compatibility. Observe other-status retries separately; no automatic failure solely for supporting another transient error. Manual migration is permitted: if required, inspect and apply documented steps in disposable fixtures before judging behavior, recording adapters.

E02: aggregation, ordering/CSV escaping, validation/line numbers, preserve old output on errors and input=output. Added flags, services or framework layers need a current reason.

Run original repository smoke tests as well as withheld checks. Tests may pass while scope is poor; scope may be small while correctness fails. No feedback or retries after seeing outputs.
