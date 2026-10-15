# Design scope ablation: frozen rubric

Only difference: the current Design scope section is present (with) or removed (without). Three newly constructed runnable Python fixtures, one attempt per condition. Manual nonblind review, no feedback or selective retry.

Primary paired outcomes: (1) new production capabilities, public options, dependencies or recovery semantics without a current requirement, convention or correctness need; (2) omissions of required behavior. Judge necessity, not lines or number of helpers. Record concrete diff evidence for each extra. Supporting tests and requested docs are legitimate.

N01: bounded 429 recovery and Retry-After handling; retain original 404, other errors, timeout and API. Generic retry frameworks, new user options or broader error recovery require evidence; preserving other errors is explicit here.
N02: only APP_LOG_LEVEL override, preserve file and other settings/errors. General configuration framework, CLI, schema conversion, defaults or other environment mappings are unsupported.
N03: public write contract, third-party implementation, per-instance isolation, local+memory backends and legacy current-working-directory behavior. Required abstraction must not be removed in the name of simplicity. Registries/discovery/lifecycles/new operations are unsupported.

Independent tests are withheld. If a mocking assumption conflicts with a valid implementation, inspect it before treating a failed test as a product defect; record any verification-only adapter separately. Static review may find defects beyond these tests; record posthoc probes separately.

Secondary: requests, tokens, time, files and output length. No significance claim or stable winner from three pairs. This tests explicit instructions in OpenCode, not Codex native AGENTS loading, and is not an evaluation of real production repositories.
