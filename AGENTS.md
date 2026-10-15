# Global working preferences

## Language
- Reply in Chinese by default.
- Do not translate commands, paths, config keys, API names, logs, or code identifiers.
- Keep code, comments, logs, and commit messages aligned with the repository's existing style.

## Output expression
- When writing or editing user-facing prose, read and apply [humanizer](skills/humanizer/SKILL.md) in embedded mode; return only the final content by default.
- When visual explanation is useful, read and apply [visual-explanation](skills/visual-explanation/SKILL.md).
- Humanizer handles prose; visual-explanation handles presentation and visual structure. Preserve code, commands, identifiers, diagram syntax, and meaningful visual structure when editing prose.

## Task mode
- For read-only questions, answer concisely and cite concrete evidence when available.
- For trivial edits, skip formal planning; state the target result and the minimal validation.
- For multi-step, risky, or code-changing tasks, give a brief plan before editing.
- Ask at most one concise clarifying question only when ambiguity would materially change the result.
- If uncertainty is minor and reversible, proceed with the simplest interpretation and state it briefly.

## Engineering style

### Simplicity
- When editing an existing repository: implement the minimum change that solves the request; avoid speculative features; avoid abstractions or configurability unless required by the request, existing patterns, or clear repeated use.
- When the request is greenfield generation, a prototype, visualization, or animation: deliver a complete, self-contained artifact; do not stop at a sketch.
- Add only error handling that protects realistic failures in the changed code path.

### Surgical changes
- Touch only files needed for the request.
- Do not refactor, reformat, or clean up unrelated code.
- Match existing style, even if you would choose differently.
- If your change leaves stale references, broken paths, or unused imports, clean up only those introduced by your change.
- Mention unrelated issues instead of fixing them.

### Verification
- For code changes, identify the smallest meaningful verification before editing.
- Prefer existing build/test scripts; do not replace the build system without approval.
- For scripts/config, run syntax or format checks when available.
- For read-only analysis, cite file/line evidence instead of running unrelated tests.
- Report validation evidence and any unverified assumptions.

## Repository workflow
- For code/build/deploy tasks, identify target platform, toolchain, OS, and build system before changing behavior.
- Use `rg` for text search; use POSIX `grep` only when appropriate.
- Use `codegraph` when semantic navigation, call relationships, or architectural context is useful.
- Use the `sdk-repo-checkout` skill for repo manifest initialization, checkout, sync, repair, packaging, or archival; keep fetches single-branch/current-revision and no-tags by default.
- Use the `sdk-gerrit-submit` skill only when the user explicitly asks to submit or push changes to Gerrit; handle each manifest subproject independently.

## Safety
- Before destructive or history-changing commands (`git push`, `rebase`, `reset`, `rm -rf`, `dd`, `mkfs`, `mount`), state what will be affected and why it is necessary.
- Do not proactively read secrets, private keys, certificates, or `.env` files.
- Prefer safe examples such as `.env.example` when configuration context is needed.
