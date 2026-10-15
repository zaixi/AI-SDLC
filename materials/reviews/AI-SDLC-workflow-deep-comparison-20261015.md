# 从真实痛点重审八套 AI 研发方案

核对日期：2026-10-15。依据：[用户痛点与需求](../../docs/project-intent.md)。本轮沿用上一轮固定提交，深入读取流程、评审、知识记录与接续规则；结论变化来自阅读深度，不是版本更新。本文修正 [初步比较](AI-SDLC-workflow-candidates-20261015.md) 的选型建议。

这是源码和指令的静态比较，不是生成评测、安装验证或实际性能排名。文中“要求”“提供”指规则明确写出；“能否做到”仍需真实任务验证。没有调用候选中的子代理、安装命令或自动化流程。

## 先纠正上次判断

1. **不应先把主候选收窄为 Matt、Superpowers、OpenSpec。** 用户的核心痛点是存量系统理解、设计原因和评审；pstack 恰有完整的 how/why/blast-radius 路线，Addy 有约束及验证机制，都应参与核心能力比较。
2. **不能把 OpenSpec 的“面向存量项目”直接推成“更会理解存量系统”。** 它主要组织变更意图、契约和状态；追查没有留下来的设计动机是另一件事。
3. **不能把 gstack 缩成浏览器 QA，也不能仅因 Spec Kit 文档多而降级。** 前者有契约、迁移和防止削弱检查的专项评审；后者明确支持存量小变更和实现后的契约收敛。
4. **不能把“有入口”“会路由”“自动执行完整流程”混为一谈。** Matt 的 ask-matt 是路由说明；pstack 的 poteto-mode 是执行模式；Superpowers 通过启动约定触发流程；OpenSpec/Spec Kit 则提供多个阶段入口。它们减少用户操作的方式和程度不同。

## 以什么标准比较

重要性先看用户问题，而不是项目名气或功能数量：

- **理解**：没有成套文档时，如何给人建立系统结构、运行关系和边界的认识？
- **意图**：如何找到或询问设计原因；如何区分记录中的事实与代理的推断？
- **评审**：测试绿了之后，还如何发现需求偏差、设计约束破坏和变更影响？给人什么证据与决定点？
- **延续**：换 Agent、会话或机器后，留下什么；是否需要重做研究或复制知识？
- **采用成本**：跨 Agent 的工具适配、Gerrit 接入、人工操作、文档维护与上游更新成本。

“少文档”不等于“只看代码”。需求契约与设计理由不能靠现状代码证明。临时实现计划可以较详细，但不应因此永久复制成一套代码结构 Wiki。

## 机制与缺口对照

| 方案 | 真正对应本项目的机制 | 原版仍留下的缺口 | 本轮定位 |
|---|---|---|---|
| Matt | 讨论时校准领域语言和代码现状；按需留下极短 ADR；规格与工程标准分轴评审 | 评审入口没有强制按变更检索全部相关 ADR；缺少规格时 Spec 轴跳过；已有长篇零散记录不自动变成人可理解的总览 | 延续当前实践、捕获新决策的候选基础 |
| pstack | how 建立系统认识，why 多来源追查原因并分级证据，blast-radius 验证关键前提，interrogate 裁决评审结果 | Cursor 工具和模型路由耦合；多来源与多模型成本；查明原因后未自动形成跨客户端的长期知识库 | **与核心痛点最直接对应的方法候选**，应进入核心比较 |
| Addy | 约束访谈、CONSTRAINTS.md、按成本放置检查、检测门槛被削弱；评审要求实验检查测试有效性；ADR 记 why | 执行工具需按语言与项目配置；机械约束覆盖不了全部设计理由；默认质量指标不能直接照搬 | **质量标准落地的核心候选**，不是仅可有可无的补丁 |
| Superpowers | 自动触发、设计批准、计划执行、任务评审、最终评审、执行裁决台账与恢复 | 对历史动机没有同等明确的来源调查流程；强触发/多轮执行需匹配任务；局部台账不是长期设计知识 | 当主要瓶颈是执行偏离、未验证就报完成时优先 |
| OpenSpec | 增量规格、变更设计与任务；verify 查覆盖、正确性、设计一致性；归档和规范同步 | 依赖契约/设计中已有的信息；核验是 advisory，不是强制 CI，也不会从无记录中找出真实动机 | 变更契约与持久状态候选，不能等同完整理解/评审体系 |
| Spec Kit | constitution 约束；analyze 查规格/计划/任务一致性；converge 查实现缺口并追加可追溯任务 | 明确以已有规格/计划/任务作为意图来源；默认多文档的维护需要决定；不能把生成了收敛任务等同验证通过 | 团队需要更明确契约和治理时的实质候选，不因“重”预先排除 |
| gstack | 工程方案与风险审查、API/迁移专项检查、检查门槛完整性、规划完成核对，以及运行/浏览器验证 | 工具运行时较多；跨宿主能力分档；GitHub PR、发布路径要适配 Gerrit；未自动知道隐性设计约束 | 评审和交付体系候选，适用范围比上次描述更广 |
| Ponytail | 列齐必要影响面，复用现有能力，最小完整修改，保留必要校验和已知限制 | 没有完整的意图追查、契约管理与接续流程；与已有简化规则重复 | 辅助纪律；现在没有理由再默认叠加 |

## 1. 存量系统难理解：pstack 为什么应提高优先级

**how 明确产出人的系统认识。** 它不是只把代码摘要交给另一 Agent：简单问题由一个 explainer 处理，复杂问题分 2–4 个角度调查后综合，输出 Overview、Key Concepts、How It Works、Where Things Live、Gotchas；多组件交互应配 Mermaid/ASCII 图。输出面向接手子系统的工程师，既要求具体文件和函数，也要求合并重复并检查相互矛盾的发现。[P1] [P7]

**why 明确拒绝“代码这样写，所以作者一定这样想”。** 它从 git/blame/历史 PR 建立锚点，再按可用来源检查任务、设计文档、聊天、运行观测等证据。epistemics 明确区分直接记录、支持证据、推断和未知；缺少原因时应说不知道。如果是为修改做准备，还把调查转成 Preserve / Change / Avoid / Risk 约束。[P2] [P3]

这直接对应用户“代码和 ADR 都在，却不懂架构边界与原因”的问题。visual-explanation 可以改善表达，但它不会代替 how/why 获取关系和历史证据。

**代价同样具体。** how 即使简单路径也要求子代理；why 倾向覆盖全部可用证据类别，不是读一份 PR 就停。工具契约使用 Cursor Task、readonly 模式和 pstack-models.mdc，并有特定模型默认值；gh 获取 PR 的部分也不能原样当作 Gerrit。取出 SKILL.md 不等于完成迁移。

因此，方法匹配度高不代表整包最容易采用。若要跨 Agent 且少量自建，必须先证明一条官方/现有移植路径能承载 how/why 和评审工具，再判断是否值得整包用。第三方移植能降低成本，但本轮没有验证其与原版的行为等价性。

## 2. 设计理由怎么留下：Matt 的优势比“轻量”更具体

Matt 的 domain-modeling 在讨论中校准词义、用具体场景澄清边界、核对人的陈述与代码，再及时记录。ADR 默认只有标题和 **1–3 句背景、决定、原因**；只在难逆转、缺上下文会意外、有真实取舍时提出，按需建文件。[M2]

这意味着此前遇到“长篇 ADR”的问题，不能直接归结为 Matt 当前模板要求长篇。要核对当时版本、调用方式和实际输出；换框架之前应区分模板问题、模型执行问题与组织/呈现问题。

但记录门槛也有空隙：重要却容易改变的业务约束，不一定满足那三个 ADR 条件。不能把所有知识都塞进 glossary 或强行升级成 ADR；应沿用项目已有规格/规则的位置。

ask-matt 给出了多会话拆票、实现和 handoff 的路线，handoff 明确链接已有资料、不复制，并写到系统临时目录。[M1] [M4] 这是便携交接材料，不是自动共享的持久状态；换机器时仍要处理文件可达性。

**Matt 的采用优势是用户已有实践和较明确的意图记录格式，不是已证明它的完整链最优。** ask-matt 自身标记 user-invoked；上游还区分用户编排入口和模型可调用能力，不能默认一个 ask-matt 就可无人工切换地执行全部阶段。

## 3. 高价值评审：真正需要比较的差别

| 机制 | 它让评审具体多做什么 | 仍需人或外部证据解决什么 |
|---|---|---|
| Matt Standards + Spec | 分开报告违反工程标准和违反需求；跳过工具已强制的机械检查；明确缺规格时跳过 Spec | 相关设计理由是否被放入可发现的依据；两轴结论不自动回答应接受哪项产品取舍 [M3] |
| pstack blast-radius | 查超出调用图的格式、依赖版本、下游影响；找“安全成立所依赖的关键事实”，运行真实代码验证 | 没有访问真实环境就不能证明真实环境成立；未知原意仍需人确认 [P4] |
| pstack interrogate | 先确认意图，多模型同题独立评审，再归为 Act on / Consider / Noted / Dismissed，保留分歧 | 多模型一致不是事实证明，最终还要核验证据；它明确不自动应用修复 [P5] |
| Addy review | 先看测试，实际翻转一个新增条件并运行，检查测试是否捕获；再看正确性、架构、安全等 | 变异要在隔离副本并恢复；一次变异不代表测试完备；约束阈值仍需项目负责人认可 [A2] |
| Addy constraints | 将已有规则与约定写成项目质量条款，检查阈值降低、测试删除/跳过、检查抑制、新例外 | 安装/配置和挂钩实际完成后才有自动检查；写了 CONSTRAINTS.md 本身不会阻止违规 [A1] |
| OpenSpec verify | 检查需求实现、场景覆盖、设计决定遵循；缺证据标 Not verified | advisory；设计不符给 warning，允许建议改实现或修设计，不能替人决定是否改变原取舍 [O2] |
| Spec Kit analyze / converge | analyze 把违反 constitution 的项列为 Critical；converge 以原意逐项查实现并生成缺口任务 | analyze 是文档一致性分析；converge 的缺口任务仍要实现/测试，未写下的原意不在其“sole source of intent”中 [K2] [K3] |
| gstack 专项评审 | API 老客户端兼容、迁移回滚/锁/混合版本；Gate Integrity 识别并审阅检查被放松的 diff | 专项检查依赖版本和业务判断；目录被扫描不等于 finding，工具标记不等于缺陷成立 [G2] [G3] [G4] |

**高价值问题不会仅凭“多一个 reviewer”自动出现。** 它需要把正确的设计约束带到评审、检查真实影响、保留可复核证据，并明确哪些取舍仍由人决定。上述方案各自提供了其中一部分，不能把“有 review Skill”视为同等能力。

Superpowers 的 reviewer 还要求审查规格没有枚举、但合理用户会期待的行为，并列出曾放弃判断的内容；比只机械对规格更强，但也可能扩大范围，必须区分合理兼容性与未经要求的新功能。[S3] 当前执行流程有 inline 路径和局部裁决台账，不应概括成“必须每步都开子代理/等人批准”。[S2]

## 4. 背景留存：谁能接续，谁会生成另一堆文档

| 方案 | 本轮读到的主要记录 | 对用户的意义与负担 |
|---|---|---|
| Matt | 术语、简短 ADR、规格/任务；临时 handoff 引用已有内容 | 长期意图较精简，但临时交接需要可达性；聚合视图仍须按需生成 |
| pstack | 调查引用、会话轨迹、分支、任务与决策 checkpoint；session-pickup 读前序轨迹并验证继承结论 | 同一环境接续路径明确；Cursor transcript 不天然跨 Agent/机器，调查报告也不自动变成长期决策记录 [P6] |
| OpenSpec | 能力规格与每次变更 proposal/design/tasks，增量同步和归档 | 有明确的仓库内状态，可跨客户端读取；仍需决定哪些旧设计保留、哪些视图按需生成 [O1] [O3] |
| Spec Kit | constitution、feature spec/plan/tasks 及研究/模型/契约等；官方让团队选择历史冻结、活契约或回流更新 | 没有要求先把全仓库反向写成规格；产物生命周期必须选清，否则容易重复 [K1] |
| Superpowers | 设计、计划、执行 ledger 与 review package | 有助执行恢复；当前流程最终评审完成后清理该 plan workspace，不能把执行台账当永久决策库 [S2] |
| Addy | 遵从既有 ADR 目录/格式；CONSTRAINTS.md；需求/计划和上下文材料 | 适合把原因及质量条款保存到既有位置，但调用链是否每次都读到仍需验证 [A1] [A3] |
| gstack | context-save 保存 Summary / Decisions Made / Remaining Work / Notes 等 checkpoint 到状态目录 | 有接续工具，但工具管理的状态目录并不等于已提交到团队知识库 [G5] |
| Ponytail | 主要为代码修改纪律与 shortcut 限制说明 | 不能承担项目背景、设计原因与任务状态管理 [T1] |

关键不是谁生成的 Markdown 最少，而是谁能让“已确认意图”和“当前状态”有清楚的归属、更新条件和读取入口，避免下次只看到过期副本。

## 5. 用同一件事看差别（纸面推演，未运行模型）

构造一个小变更：给已有任务系统加通知重试。代码目前在超时时不重做主任务；历史记录可能说明“主任务副作用不可重复”。测试全部通过，但候选实现把通知失败改成整个任务重跑。此例只用于解释能力边界，不是用户已经选定的真实项目或测试成绩。

- **pstack** 的 how/why 会要求追踪现有行为和原因证据，blast-radius 再验证重跑能否重复副作用。它最直接覆盖“改之前理解”和“改之后的影响”；若历史证据不存在，why 应报告未知，不能编造理由。
- **Matt** 可在澄清时把该限制确认进规格或决策；Spec reviewer 再检查是否违背。若限制没有进入规格/标准，且无显式相关 ADR 检索要求，不能保证它会主动恢复这条历史原因。
- **OpenSpec / Spec Kit** 若契约已写“仅重试通知”，就有明确的偏离检查入口；如果只写“失败可重试”，这些流程会面对同样的歧义。它们组织并核对已明确的意图，不能从规范文件结构本身得到缺失的事实。
- **Addy** 的测试变异和验证审查可能发现“整任务重跑仍然绿”的测试盲区；如果已有“不得重复业务副作用”的项目约束，则还能检查它。阈值和覆盖率本身证明不了该语义。
- **Superpowers / gstack** 有边界、正确性和风险审查的入口，可能发现重试影响；能否稳定抓住此问题取决于得到的上下文和实际证据，不能仅凭角色名保证。
- **Ponytail** 倾向最小完整改动，但代码更少并不证明重试语义正确。

这个例子说明为何“状态保存”“执行纪律”和“恢复设计原意”要分别核对：三者都重要，互不替代。

## 6. 现在可以作什么判断

**方法匹配度上，pstack 应与 Matt 一起优先看。** 前者强在调查现状、追查原意和影响证据，后者强在与人形成明确语言、记录新决策并组织后续工作。它们是不同起点，不是当前已经证明哪一个整体更好。

**采用成本上，暂不建议切换整套主框架。** 用户已在用 Matt，pstack 原版有具体 Cursor 耦合；先核对现成移植是否覆盖所需工具与语义，再算更换成本，比因单入口看起来完整就迁移更可靠。现有 Matt 也不能直接宣称满足全部跨 Agent 自动执行要求。

**Addy 与 gstack 应按质量缺口评估。** 若真正的问题是 Agent 自写检查、自降标准、测试没测到关键行为，Addy 的约束/变异检查和 gstack 的 Gate Integrity 比再加一层流程更对题。只采用已经存在且填补缺口的机制，避免重复 reviewer 和门槛。

**OpenSpec 与 Spec Kit 应按契约/状态缺口评估。** 若跨会话丢的是“已批准行为、当前变更状态、设计决定与实现之间的关系”，它们有直接价值；若主要是“不理解无文档老系统为何这样做”，先引入它们不会自行产生缺失的理解。两者都有多客户端路径；Spec Kit 也明确支持存量小变更，不应只比较 OpenSpec。[K1] [K4] [O3]

Superpowers 是值得保留的执行流程对照；Ponytail 暂不新增，因为已有范围控制研究未证明继续叠加规则有稳定收益。这不是认定 Ponytail 无效，而是目前没有新增需求证明其接入成本值得。

**下一步最有区分度的是一条真实存量变更，而不是再跑一个从零写应用的题。** 给各候选相同的仓库、已有约束与修改目标，分别观察：是否查明旧行为及理由、是否给出人能懂的影响解释、是否抓住违反约束但测试仍绿的变更、是否能在新会话接续。先明确采用配置与可访问工具，才比较实际产出；不把工具缺失、上下文差异或默认输出格式差异当作 Skill 质量差距。每个配置保留少量独立样本，遵循用户此前次数要求。

本轮结论是缩小了待验证的问题，未选定安装组合，未证明稳定质量排名。

## 固定版本依据

每个链接均指向与初步比较相同的固定提交。详细文件哈希见 [深读来源索引](../references/workflow-candidates-20261015/deep-sources.json)。下载缓存不入 Git，原文可从链接恢复。

[M1]: https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/ask-matt/SKILL.md
[M2]: https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/domain-modeling/ADR-FORMAT.md
[M3]: https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/code-review/SKILL.md
[M4]: https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/handoff/SKILL.md
[P1]: https://github.com/cursor/plugins/blob/e5136d82418d2db3165ea1050d17577cd618cc05/pstack/skills/how/SKILL.md
[P2]: https://github.com/cursor/plugins/blob/e5136d82418d2db3165ea1050d17577cd618cc05/pstack/skills/why/SKILL.md
[P3]: https://github.com/cursor/plugins/blob/e5136d82418d2db3165ea1050d17577cd618cc05/pstack/skills/why/references/epistemics.md
[P4]: https://github.com/cursor/plugins/blob/e5136d82418d2db3165ea1050d17577cd618cc05/pstack/skills/blast-radius/SKILL.md
[P5]: https://github.com/cursor/plugins/blob/e5136d82418d2db3165ea1050d17577cd618cc05/pstack/skills/interrogate/SKILL.md
[P6]: https://github.com/cursor/plugins/blob/e5136d82418d2db3165ea1050d17577cd618cc05/pstack/skills/poteto-mode/playbooks/session-pickup.md
[P7]: https://github.com/cursor/plugins/blob/e5136d82418d2db3165ea1050d17577cd618cc05/pstack/skills/how/references/explainer-prompt.md
[A1]: https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/constraint-driven-development/SKILL.md
[A2]: https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/code-review-and-quality/SKILL.md
[A3]: https://github.com/addyosmani/agent-skills/blob/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/documentation-and-adrs/SKILL.md
[O1]: https://github.com/Fission-AI/OpenSpec/blob/f80d860fc510ba4f51180c8ddde35b91b32de657/schemas/spec-driven/schema.yaml
[O2]: https://github.com/Fission-AI/OpenSpec/blob/f80d860fc510ba4f51180c8ddde35b91b32de657/skills/openspec-verify-change/SKILL.md
[O3]: https://github.com/Fission-AI/OpenSpec/blob/f80d860fc510ba4f51180c8ddde35b91b32de657/docs/supported-tools.md
[S1]: https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/using-superpowers/SKILL.md
[S2]: https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/subagent-driven-development/SKILL.md
[S3]: https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/requesting-code-review/code-reviewer.md
[K1]: https://github.com/github/spec-kit/blob/3238fa9285694dc539aeb9829b337bfd6aed7317/docs/guides/existing-projects.md
[K2]: https://github.com/github/spec-kit/blob/3238fa9285694dc539aeb9829b337bfd6aed7317/templates/commands/analyze.md
[K3]: https://github.com/github/spec-kit/blob/3238fa9285694dc539aeb9829b337bfd6aed7317/templates/commands/converge.md
[K4]: https://github.com/github/spec-kit/blob/3238fa9285694dc539aeb9829b337bfd6aed7317/docs/reference/integrations.md
[G1]: https://github.com/garrytan/gstack/blob/47d639abffa882b8cbb641d7d1dedf08ecada9ec/README.md
[G2]: https://github.com/garrytan/gstack/blob/47d639abffa882b8cbb641d7d1dedf08ecada9ec/review/gate-integrity.md
[G3]: https://github.com/garrytan/gstack/blob/47d639abffa882b8cbb641d7d1dedf08ecada9ec/review/specialists/api-contract.md
[G4]: https://github.com/garrytan/gstack/blob/47d639abffa882b8cbb641d7d1dedf08ecada9ec/review/specialists/data-migration.md
[G5]: https://github.com/garrytan/gstack/blob/47d639abffa882b8cbb641d7d1dedf08ecada9ec/context-save/SKILL.md
[T1]: https://github.com/DietrichGebert/ponytail/blob/84740e3d344b69b4a133201fa519eb37a62a2b2a/skills/ponytail/SKILL.md

引用键：M = Matt，P = pstack，A = Addy，O = OpenSpec，S = Superpowers，K = Spec Kit，G = gstack，T = Ponytail。
