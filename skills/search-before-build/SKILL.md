---
name: search-before-build
description: "Research-before-coding workflow: search npm/PyPI, MCP servers, skills, and GitHub for existing tools before writing custom code, then adopt, extend, borrow, or build. Research directly or delegate focused questions as needed. Use when starting a feature, choosing a technology or architecture, adding a dependency or integration, or about to write a utility that may already exist."
license: MIT
metadata:
  origin: ECC
---

# /search-before-build — Research Before You Code

Systematizes the "search for existing solutions before implementing" workflow.

## Trigger

Use this skill when:
- Starting a new feature that likely has existing solutions
- Adding a dependency or integration
- The user asks "add X functionality" and you're about to write code
- Before creating a new utility, helper, or abstraction
- Choosing a technology stack or architecture

Skip routine fixes, mechanical edits, and ordinary use of an adopted tool. For the tasks above, briefly check GitHub and official ecosystems even when local code already works; external designs may reduce maintenance or offer a better approach.

## Workflow

```
┌─────────────────────────────────────────────┐
│  0. CHANNEL CHECKS (as needed)              │
│     Check a channel when using it;          │
│     report unavailable coverage honestly    │
├─────────────────────────────────────────────┤
│  1. NEED ANALYSIS                           │
│     Define what functionality is needed      │
│     Identify language/framework constraints  │
├─────────────────────────────────────────────┤
│  2. SEARCH (delegate when useful)          │
│     ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│     │  npm /   │ │  MCP /   │ │  GitHub / │  │
│     │  PyPI    │ │  Skills  │ │  Web      │  │
│     └──────────┘ └──────────┘ └──────────┘  │
├─────────────────────────────────────────────┤
│  3. EVALUATE                                │
│     Assess candidates (functionality, maint,│
│     community, docs, license, deps)         │
├─────────────────────────────────────────────┤
│  4. DECIDE                                  │
│     ┌─────────┐  ┌──────────┐  ┌─────────┐  │
│     │  Adopt  │  │  Extend  │  │  Build   │  │
│     │ as-is   │  │  /Wrap   │  │  Custom  │  │
│     └─────────┘  └──────────┘  └─────────┘  │
├─────────────────────────────────────────────┤
│  5. IMPLEMENT                               │
│     Install package / Configure MCP /       │
│     Write minimal custom code               │
└─────────────────────────────────────────────┘
```

## Decision Matrix

| Signal | Action |
|--------|--------|
| Exact match, well-maintained, MIT/Apache | **Adopt** — install and use directly |
| Partial match, good foundation | **Extend** — install + write thin wrapper |
| Complementary tools needed for the current requirements | **Compose** — combine only the parts needed |
| Useful design, unsuitable dependency | **Borrow** — understand and adapt the relevant mechanism; check its license before copying code |
| Nothing suitable found | **Build** — write custom, but informed by research |

Prefer the smallest solution that meets the current requirements. Compare adoption
and integration costs with extending what already exists. Add a component when
it resolves a concrete gap; useful discoveries can remain references without
becoming dependencies or a future roadmap.

## How to Use

### Step 0: Tool Availability (as needed)

This is agent guidance, not an executable setup script. Check availability when
you need a relevant channel, rather than running every check before research.

| Channel | Check | If missing |
|---------|-------|------------|
| Repository search | `rg --files` and targeted `rg` queries | State that only visible files were inspected |
| Package registry | Query the relevant registry through the web or an available package manager | Use official project docs and state any coverage gap |
| GitHub | Public web/API search, or an available `gh` CLI | Use official project sources and state any coverage gap |
| MCP/docs tools | Available tool list | Fall back to official docs/web search |
| Skills directory | `ls ~/.claude/skills ~/.codex/skills` where applicable | Say no local skill catalog was available |

### Quick Mode (inline)

Before writing a utility or adding functionality, mentally run through:

0. Does this already exist in the repo, standard library, or platform? → `rg` through relevant modules/tests and inspect built-in capabilities first
1. Is this a common problem? → Search npm/PyPI
2. For agent/tool integration, is there an MCP for this? → Check available integrations and search
3. For an agent workflow, is there a skill for this? → Check the available skill catalog
4. Is there a GitHub implementation/template? → Run GitHub code search for maintained OSS before writing net-new code

### Full Mode (focused research)

Research directly by default. When there are separable questions and delegation
is available and authorized, assign focused research to a subagent. For example:

```
Agent(subagent_type="general-purpose", prompt="
  Research existing tools for: [DESCRIPTION]
  Resolve this decision-relevant question: [QUESTION]
  Language/framework: [LANG]
  Constraints: [ANY]

  Search: GitHub and the relevant official ecosystem; MCP/skills when applicable
  Return: Recommendation, decisive sources, and unresolved questions
")
```

Older Claude Code docs may call this `Task(...)`; use the current agent/subagent
tool name exposed by the active harness. Reuse returned evidence; recheck
decisive gaps or contradictions instead of repeating the whole search.

### Evaluate and stop

Deepen research only for candidates that could change the choice. For a promising
candidate, distinguish native support from a documented extension or composition
with existing code. Check the integration path before treating a missing native
feature as a reason to reject it.

Verify the assumptions that decide the recommendation against official docs or
source/tests for the relevant version. A proposed adapter is still custom work;
mark unverified feasibility as uncertain. If runnable integration code is part
of the deliverable, check the actual API rather than inferring it from examples
for a related layer.

Once a path meets the requirements and the decisive tradeoffs are supported,
move to delivery. Further research should answer a named question that could
change that choice; if it cannot be resolved within the available budget,
deliver a conditional recommendation and the specific check still needed.

### Deliver

Lead with the recommended solution, why it fits, what remains custom, and any
uncertainty that could change the choice. Include decisive sources and tradeoffs
at the depth the task needs; keep the search history out of the deliverable.
Continue implementation when requested; for a design-only task, describe the
integration boundary without expanding into speculative implementation code.

## Search Shortcuts by Category

### Development Tooling
- Linting → `eslint`, `ruff`, `textlint`, `markdownlint`
- Formatting → `prettier`, `black`, `gofmt`
- Testing → `jest`, `pytest`, `go test`
- Pre-commit → `husky`, `lint-staged`, `pre-commit`

### AI/LLM Integration
- Claude SDK → Context7 for latest docs
- Prompt management → Check MCP servers
- Document processing → `unstructured`, `pdfplumber`, `mammoth`

### Data & APIs
- HTTP clients → `httpx` (Python), `ky`/`undici` (Node)
- Validation → `zod` (TS), `pydantic` (Python)
- Database → Check for MCP servers first

### Content & Publishing
- Markdown processing → `remark`, `unified`, `markdown-it`
- Image optimization → `sharp`, `imagemin`

## Integration Points

These integrations are optional when the named agents or skill are available.
Otherwise perform the relevant research directly.

### With planner agent
Before Phase 1 (Architecture Review), the planner uses the research results:
- Researcher identifies available tools
- Planner incorporates them into the implementation plan
- Avoids "reinventing the wheel" in the plan

### With architect agent
The architect can request focused research for:
- Technology stack decisions
- Integration pattern discovery
- Existing reference architectures

### With iterative-retrieval skill
Use progressive discovery when a decision-relevant question remains unresolved:
- Discover candidates through relevant channels
- Inspect the promising candidates
- Check the compatibility that determines the choice

Stop under the criteria above; these are not mandatory research rounds.

## Examples

Illustrative searches, not verified current recommendations; confirm the
capabilities and versions relevant to the actual task.

### Example 1: "Add dead link checking"
```
Need: Check markdown files for broken links
Search: npm "markdown dead link checker"
Found: textlint-rule-no-dead-link (score: 9/10)
Action: ADOPT — npm install textlint-rule-no-dead-link
Result: Zero custom code, battle-tested solution
```

### Example 2: "Add HTTP client wrapper"
```
Need: Resilient HTTP client with retries and timeout handling
Search: npm "http client retry", PyPI "httpx retry"
Found: got (Node) with retry plugin, httpx (Python) with built-in retry
Action: ADOPT — use got/httpx directly with retry config
Result: Zero custom code, production-proven libraries
```

### Example 3: "Add config file linter"
```
Need: Validate project config files against a schema
Search: npm "config linter schema", "json schema validator cli"
Found: ajv-cli (score: 8/10)
Action: ADOPT + EXTEND — install ajv-cli, write project-specific schema
Result: 1 package + 1 schema file, no custom validation logic
```

## Anti-Patterns

- **Jumping to code**: Writing a utility without checking if one exists
- **Ignoring relevant integrations**: Missing an existing MCP capability when the task is agent/tool integration
- **Silent skipping**: Reporting "nothing found" when a search channel was unavailable
- **Over-customizing**: Wrapping a library so heavily it loses its benefits
- **Dependency bloat**: Installing a massive package for one small feature
