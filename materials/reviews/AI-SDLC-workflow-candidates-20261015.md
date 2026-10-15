# AI 原生研发候选：Matt 之外的七条线索

> 后续修正：本轮初筛对 pstack、Addy、gstack 与 Spec Kit 的判断不够深入。请优先读 [按真实痛点重做的机制比较](AI-SDLC-workflow-deep-comparison-20261015.md)；本页保留初筛过程，不作为当前排序结论。

核对日期：2026-10-15。依据是 [项目痛点与需求](../../docs/project-intent.md)。本轮读取官方 README、选定的 Skill/模板和接入文档，未安装、执行或做模型对照；下列适配判断是建议，不是采用决定。

## 当前判断

不能继续把“Matt 最适合”视为已完成的选型。Matt、Superpowers、OpenSpec 都值得进入主方案比较；Addy 与 pstack 有直接针对约束、理解和高价值评审的能力。不同项目承担的职责不完全相同，不宜用一个总排名代替选择，也不宜默认组合安装。

| 候选及身份 | 核对到的能力 | 与本项目的适配判断 | 需要验证的代价或缺口 |
|---|---|---|---|
| [Matt Pocock Skills](https://github.com/mattpocock/skills) | 可组合工程 Skill，领域建模、澄清、规格、任务、实现、评审；有 ask-matt 等入口 | 保留为主候选，尤其是设计意图和领域语言 | 单入口是否覆盖所需路径、人工介入及客户端工具差异；不能把“任意模型”理解为所有客户端全面兼容 |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | 面向存量及新项目；变更 proposal、specs、design、tasks；探索、提出、实施、核验、归档；可配置工作流 | 优先核对“变更意图与状态如何延续”，可能比再写交接体系省事 | 默认规范库与变更记录的维护负担；不能自动证明实现正确，也不能恢复未记录的设计原因 |
| [Superpowers](https://github.com/obra/superpowers) | 自动识别相关 Skill；讨论设计、计划、TDD、调试、实施和评审；官方有多客户端安装说明 | 优先核对“一个入口之后自动选择流程”，值得与 Matt 并列比较 | 触发要求强，设计批准、计划、子代理、worktree 等流程需匹配任务；避免把小修复也流程化 |
| [Spec Kit](https://github.com/github/spec-kit) | 结构化规格开发与项目原则；规划、任务、实施、收敛；也有按需 bug/idea assessment 扩展 | 需要明确验收契约、团队规格治理时值得比较，并非仅能做新项目 | 默认文档产物较多，需验证是否重复记录代码可查内容；当前支持定制与扩展，不能简单贴上“固定瀑布流”标签 |
| [gstack](https://github.com/garrytan/gstack) | 多角色规划与审查、浏览器 QA、工程评审、发布、autoplan 等 | 产品/Web 的规划和实际体验验证值得借鉴 | Claude Code 为官方 full 档，Codex/OpenCode 等为 experimental；安全钩子和外部模型评审依赖不同，不适合直接视为所有 Agent 等价的主框架 |
| [Addy Osmani agent-skills](https://github.com/addyosmani/agent-skills) | 从规格到交付的 Skill 与入口；约束驱动开发、质量评审、ADR、上下文、分步实现 | 特别值得检查约束执行及防止降低质量门槛，ADR 原则也与“记录为什么”一致 | 不同客户端的命令和自动接入有差异；多条生命周期命令并不天然等于一个统一入口；默认指标要按项目调整 |
| [Lauren Tan 的 pstack](https://github.com/cursor/plugins/tree/main/pstack) | poteto-mode 选择 playbook，再调用 how、why、architect、blast-radius、interrogate 等；涵盖调查、实现和接续 | 单入口、系统理解、设计原因和基于运行证据的变更评审都高度相关，不能仅列为一般参考 | 原版是 Cursor 插件，涉及 Cursor 工具、模式、模型路由与多代理；第三方 Codex 等移植不等于原作者已验证跨平台 |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | 最小完整改动、优先现有实现与标准库、少抽象、必要验证；多客户端接入 | 是控制实现膨胀的辅助纪律，不是完整主研发流程 | 与现有 Simplicity、Surgical changes 及 search-before-build 有交集；没有新证据时不再默认叠加范围规则 |

“Addy Osmani”是作者名，本次按 agent-skills 核对；他另有 web-quality-skills，不是同一个仓库。Ponytail 按上述项目识别，若用户指另一仓库需要调整。pstack 的原始来源在 cursor/plugins/pstack，搜索得到的多个独立 pstack 仓库多为移植，不混作同一版本。

## 三个会改变选型的问题

### 单入口：谁负责选择下一步

- Superpowers 的 using-superpowers 会要求先检查并调用相关 Skill，README 描述为自动触发。其原文有“即使只有 1% 可能适用也调用”的强约束；用户指令优先，但实际开销和误触发需要测。
- pstack 的 poteto-mode 本身就是主入口，选择 playbook 后按步骤调用其他能力；原版标记 `disable-model-invocation: true`，通常需用户开启该模式，持久化方式由 Cursor 提供。它实现了“记一个入口”，不等于无需任何启用操作。
- OpenSpec 的 explore/propose/apply/archive 是生命周期入口。Codex、Qoder、Zed 等命令形式不同；共享一套产物不等于已替用户统一所有动作。可以研究小型路由接入，但目前没有验证这项定制工作量。
- Addy 有 using-agent-skills 路由以及 /spec、/plan、/build 等命令，`/build auto` 能在批准后衔接规划和实施；是否满足整条链单入口仍需核对。

### 保存什么：规范契约与代码镜像不同

用户反对的是重复维护代码可恢复的信息，不是反对所有规格与 Markdown。描述“应该具备的行为”和验收条件，即使代码中有实现，也可能是有价值的独立契约。

OpenSpec 默认把现有能力规格与增量变更分开，设计模板包括背景、目标/非目标、决定、风险/取舍、迁移和开放问题，适合评估意图延续。但必须明确哪些记录是规范、哪些只是临时实施材料，避免全部转成长期知识库。

Spec Kit 的计划模板含 research.md、data-model.md、quickstart.md、contracts/、tasks.md，以及技术上下文和目录结构。它可定制，但默认产物对本项目可能偏多，需要用真实存量变更比较必要性，不能只按文件数否定。

Superpowers 也默认保存设计和实施计划。其 README 对计划描述较重，但当前 writing-plans 原文强调明确接口、测试与已定选择，不能仅凭 README 的“完整代码”概括所有计划输出。

Addy 的 documentation-and-adrs 明确记录 why、约束与取舍，避免记录显而易见的代码，并优先遵守仓库已有 ADR 约定；这与本项目要求直接相符。

### 评审什么：通过测试之外的判断

Addy 的 constraint-driven-development 会先读取已有项目事实，再确认质量维度、阈值和执行方式，形成 CONSTRAINTS.md，并关注删除测试、跳过测试、降低阈值和抑制检查等绕过。阈值和覆盖率不自动代表正确性，已有约束也不必重新访谈。

pstack 的 blast-radius 明确说“列调用者不是任务”，要求检查 diff 之外的真实影响，包括依赖版本、数据格式和下游边界，再运行代码验证关键前提。architect 会先 how/why 理解现有结构；多模型候选与合成会增加成本，且默认未必等人工确认。这些步骤需要与用户的决策权限和任务预算匹配。

gstack 的浏览器 QA 对用户体验和实际可运行系统有价值，但不能据此推断适配 Kernel/BSP 或 Gerrit 评审。GitHub PR 导向的发布流程也需要单独评估。

以上机制是可借鉴的具体能力，不证明其评审能替代人工，也不证明它们已覆盖本项目特有的设计约束。

## 建议的下一步

先缩小到“选主流程”与“补关键能力”两个问题，不先安装组合包：

1. 用同一个存量项目变更比较 Matt、Superpowers、OpenSpec 的完整使用路径：人需要输入什么、决定什么、维护什么，Agent 如何接续和证明完成。三者职责有差异，按同一需求核对，不能强制相同阶段数。
2. 在这条任务上检查 Addy 的约束机制与 pstack 的理解/影响分析是否填补真实缺口；若主方案已能完成，不另加工具。
3. Spec Kit 保留为规格治理候选；若试点需要其结构化契约能力，则与 OpenSpec 对照，不能现在就排除。gstack 按真实项目是否需要浏览器 QA 决定是否进一步深入。Ponytail 暂不默认引入。

目前尚无真实项目试点和同期模型对照，不能断言任何方案是最佳。也不默认把 OpenSpec+Superpowers+Matt 全部组合；它们的澄清、计划、状态和评审可能重复或冲突。需要组合时先明确每项产物与决策由谁负责，保留独立更新路径。

## 来源与可复核范围

固定提交、读取文件与 SHA-256 见 [来源索引](../references/workflow-candidates-20261015/sources.json)。原始文档下载保留在本轮环境的 /tmp 中，不作为持久公共附件；Git 只提交本报告和轻量索引。固定提交链接是复查原文的入口，不依赖该临时目录。

- [OpenSpec 支持工具](https://github.com/Fission-AI/OpenSpec/blob/f80d860fc510ba4f51180c8ddde35b91b32de657/docs/supported-tools.md)：明确列 Codex、Claude、OpenCode、Qoder、Zed Agent 的交付形式。
- [OpenSpec 默认工作流](https://github.com/Fission-AI/OpenSpec/blob/f80d860fc510ba4f51180c8ddde35b91b32de657/schemas/spec-driven/schema.yaml) 与 [设计模板](https://github.com/Fission-AI/OpenSpec/blob/f80d860fc510ba4f51180c8ddde35b91b32de657/schemas/spec-driven/templates/design.md)。
- [Superpowers 自动路由](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/using-superpowers/SKILL.md)、[设计](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/brainstorming/SKILL.md) 与 [计划](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/writing-plans/SKILL.md)。
- [Spec Kit 入口](https://github.com/github/spec-kit/blob/3238fa9285694dc539aeb9829b337bfd6aed7317/README.md) 与 [计划模板](https://github.com/github/spec-kit/blob/3238fa9285694dc539aeb9829b337bfd6aed7317/templates/plan-template.md)。
- [gstack 平台支持分档](https://github.com/garrytan/gstack/blob/47d639abffa882b8cbb641d7d1dedf08ecada9ec/README.md#other-ai-agents)：档位是作者的测试声明，本轮没有复现。
- [Addy 约束驱动开发](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/constraint-driven-development/SKILL.md) 与 [ADR](https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/documentation-and-adrs/SKILL.md)。
- [pstack 主入口](https://github.com/cursor/plugins/blob/e5136d82418d2db3165ea1050d17577cd618cc05/pstack/skills/poteto-mode/SKILL.md)、[影响分析](https://github.com/cursor/plugins/blob/e5136d82418d2db3165ea1050d17577cd618cc05/pstack/skills/blast-radius/SKILL.md) 与 [架构工作流](https://github.com/cursor/plugins/blob/e5136d82418d2db3165ea1050d17577cd618cc05/pstack/skills/architect/SKILL.md)。
- [Ponytail 主 Skill](https://github.com/DietrichGebert/ponytail/blob/84740e3d344b69b4a133201fa519eb37a62a2b2a/skills/ponytail/SKILL.md)。

本次候选均公开提供 MIT 许可；pstack 依据其子目录 LICENSE，不能从 monorepo 根元数据无许可证推出子项目无许可。许可和依赖仍需在实际引入的具体文件上核对。
