# Frozen before generation

Each case-condition is run once. No no-skill control. Nonblind review by the author; descriptive results only, not causal or statistical claims.

R01: correct CSV (including commas, quotes, embedded newlines, Unicode, generator and empty input); use or extend existing encode_rows rather than duplicating writer; preserve existing behavior. Verify with hidden behavioral checks.
R02: valid archive; relative paths; Unicode; reject/skip symlinks; exclude destination inside source, including existing destination. Prefer standard library; meaningful verification. No requirement to browse if local facilities suffice.
R03: actual public-source research; fit to Markdown and HTML, local paths, exclusions, caching; correct actionable GitHub Actions example; honest limits. Do not reward evidence volume alone. Distinguish tool capability from what its CI invocation enables; cache persistence matters. No preselected winning tool.

Across cases: task completion and correctness first; useful reuse/adaptation, unnecessary dependencies, search stopping, avoidable blocking, implementation/test quality, report clarity. Count tool actions, requests, wall time, reported input/output tokens and response length separately. HTTP/provider failures are infrastructure, not skill quality.

No own skill refinements. Both full supplied skill packages available. Same model, tools, budgets. Explicit activation, not automatic skill discovery. Public network shared, filesystem/home/context isolated. Same-model OpenCode subagents allowed if exposed; their usage must be included and verified from wire. Three different tasks are not repeated samples of one population.
