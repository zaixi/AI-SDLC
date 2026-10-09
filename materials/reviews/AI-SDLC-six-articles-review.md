# 六篇文章对 AI-SDLC 设计的帮助与限制

日期：2026-10-08。阅读材料为用户上传的六份 PDF，共 63 页。已读取可提取正文，并查看 AAIC 第 3、6 页及领域架构第 1 页中的关键图表。本文沿用此前内容核对的原则：区分作者建议、实践报告、公开实现和可复现效果。

结论：有帮助。最值得吸收的是有证据的决策、可版本化交接、按读者生成评审视图，以及通过阶段退出条件控制流程。六篇文章不构成对某个完整 AI Engineering OS 的效果证明，也不要求立即安装插件或建设多 Agent 平台。

## 逐篇判断

### 1. 在新的研发模式下，如何看懂 AI 写的技术方案？

作者署名志春，AliExpress 技术，2026-09-16；PDF 7 页。

第 1 页描述 AAIC 的领域上下文与 explore/propose/apply/test 流程。第 2–5 页给出一个明确的问题和解决办法：详细执行方案包含大量代码层级信息，协作方需要协议变化、风险、配置和协作事项。因此用 PRD、详细方案和领域模板生成面向不同读者的评审稿，缺失信息标为待确认，合并后检查来源和跨章节一致性。

**值得吸收：**

- 文档的读者和用途应明确；可评审视图是详细方案的派生产物，而不是把所有详细信息删掉。
- 章节注明主要来源；协议、风险、配置、功能列表间做对应检查。
- 评审视图自动生成可以减少重复整理，但必须随源版本更新。

**需要限定：**

- 文中“propose-output 是工程结论唯一可信源”可作为本次转述任务的输入边界，不能推广为整个工程系统的事实权威。需求、接口、代码实际行为和验证结果各有自己的来源；AI 生成方案不会自动成为真实事实。
- 模板适合交易域，不能直接作为 BSP/安全系统的评审模板。技术评审可能必须保留锁、时序、内存、错误路径和测试细节。
- “不含行号引用”是面向合作方的呈现取舍；源证据应保留在详情或附录中，不应永久删除追溯锚点。
- 五个子 Agent 是该团队的实现选择。PDF 提供示例和使用情况跟踪的描述，没有足够的前后对照数据证明五个 Agent 比单 Agent 更好，或评审耗时降低了多少。

**对本项目：**引入一个源版本绑定的 Review View，先用一个 Agent 生成并校验；评审意见回到源决策修订，再刷新视图。show-me/ELI5 可以帮助呈现，但无法替代按读者筛选信息与来源验证。

### 2. 第八篇：主交付链：Grilling → Spec → Tickets → Implement → Code Review

FutureCraft AI，2026-10-01；PDF 6 页。

第 1–4 页把流程解释为不同的退出条件，而非单向瀑布；Ticket 应尽量形成可独立验证的行为切片，发现前提错误应回到相应阶段。第 4–5 页给出简短交付记录：输入、测试接口、变化、验证和下一步。第 5 页明确 LedgerLoop 是演示性虚构案例。

**值得吸收：**任务 ready 的依据、真实阻塞依赖、交付记录，以及 Standards/Spec 两个审查维度分开呈现。它把我们之前的 Task Contract 和 Task Graph 从概念变成了可操作记录。

**需要限定：**

- 虚构例子没有证明吞吐、质量或成本改善。
- “一票一会话”是控制上下文和范围的策略，不是必须如此；当前原始仓库还提供 implement-spec，支持在一个集成分支按 ready frontier 并行实施。
- 竖向切片适合许多功能增量；广泛机械重构、硬件 bring-up 和联动迁移可能需要预先重构、兼容扩展/收缩或集成任务。原始 to-tickets 已明确 wide refactor 的例外。
- “每类风险都有处理位置”只能理解为设计目的，不是流程能保证所有风险被发现。

**对本项目：**保留精简阶段与回退规则，并允许功能、缺陷、实验和重构采用不同路线。

### 3. domain-architecture-skills：让 AI 先建模、再选架构、最后写代码

了不起的 Java，2026-09-04；PDF 7 页。

第 2–4 页区分领域意义、架构边界、框架落地与交接，并保留 confirmed/inferred/proposed；只有真正依赖未决问题的工作暂停。第 5 页明确简单 CRUD 不应强制完整 DDD。

**值得吸收：**事实与提案分类、依赖范围内的阻塞、最小规划就绪增量、保持专业分析所有权，以及 Handoff 中保留证据、假设、开放项与下一位责任人。

**当前原始实现补充：**

- GitHub API 显示仓库现归于 huahill/domain-architecture-skills；PDF 中 xfoundries 的安装示例不应照抄。
- 当前提供五个入口，新增 using-vadmin；文章中的四入口描述属于较早快照。
- 已有 JSON Schema、校验/修订辅助工具、summary/full Markdown 投影，交接含身份、revision、结果引用、依赖范围内的 blockers 与失效记录。
- 文档明确：数据库持久化、并发协调、分布式恢复和自动 resume 不在当前这代契约范围内。结构化交接不等于完整任务引擎。
- 被接受的 inferred/proposed 可以作为明确获接受的假设用于规划；其原始状态仍不变为 confirmed。批准采用某个假设不等于实证证明它正确。

**对本项目：**这是最直接的 Handoff Contract 参考，但其主要目标是业务后端，Java/Kotlin 指导较深。我们可以采用证据与交接机制；BSP 仍需单独的运行时、IRQ、锁、时序、硬件与故障模型，不能直接套用订单聚合、CQRS 或框架模板。

### 4. AI Native 研发体系建设与落地手册

雷鹏，数据智谷，2026-08-20；PDF 29 页。

第 4 页给出逻辑层和对象定义；第 7 页提出存量系统使用 Current Truth + Spec Delta；第 10–11 页主张从单 Agent 和确定性工具起步；第 13–15 页定义 Context Pack、知识/记忆区别和先 Git + Markdown 后专用记忆层；第 18–20 页建议任务、流程、业务层评测与试点；第 24–25 页提供模板。

**值得吸收：**

- 先有协议和真实任务再平台化。
- 权威知识与经验记忆分开：记忆需要来源、作用域、有效期、被替代关系和纠正机制。
- Context Pack 含事实、假设、冲突、引用及版本，而不是只增加上下文长度。
- 对存量系统保存增量变更，不反复重写全部架构文档。
- 同时衡量质量、周期、人工投入与每个成功任务的总成本；失败回归用例比技能数量更有意义。

**需要限定：**

- 这是作者给出的实施参考，不是标准认证，也未给出足够的试点数据证明整套七层体系的效果。
- Registry、网关、委员会、门户和专用记忆服务不应变为小项目的启动前提。
- 三条真实需求可证明流程能运行，不能单独支持“统计显著改善”。需要任务难度、样本量、模型/流程版本和人工投入的可比设计。
- “相同输入”不能保证相同 Agent 输出；可重放证据不等于完全确定性的行为重放。
- 首页提出 30 天内完成至少 3 个真实需求；路线图第 20 页将这一目标放在第 31–60 天。时间承诺并不一致，应当作为试点计划建议重新制定。
- 测试必须有独立判据；Review Agent 的独立会话并不消除同模型、同上下文或同错误 Spec 带来的共同盲区。

**对本项目：**借用 Context Pack、变更 Delta、交付证据与评测模板，暂不建设完整组织平台。

### 5. 总结篇：mattpocock/skills 全系列回顾与速查合集

共渡时艰，2026-08-19；PDF 6 页。

第 2–4 页整理按问题/阶段选技能及 user-invoked/model-invoked 边界；第 6 页强调可裁剪、工具不是信仰。

**值得吸收：**把技能当可组合工程纪律；共享词汇、及时反馈与按任务选路线比固定命令串更重要。

**版本限制：**当前原始仓库已将主要术语文件从 CONTEXT.md 改成 GLOSSARY.md，多个上下文可用 GLOSSARY-MAP.md。当前公开树未找到 batch-grill-me 和 resolving-merge-conflicts 两个同名 SKILL.md，loop-me 位于 in-progress。这不能证明历史文章错误，但说明速查清单不是稳定 API。安装命令也已变化，使用时必须核对原始 README 与平台版本。

当前公开 ask-matt 自我定义为技能/流程路由器。将其升级为个人 Engineering OS 是我们的设想，不是这个技能已经具备的全部产品能力。用户自己的改造版需要另行检查。

**对本项目：**作为方法索引，不作为无需核对的安装和运行规范。

### 6. 技术一把手用 Matt Pocock Skills 提升团队效率

物理知识点，2026-08-19；PDF 8 页。

第 2–5 页以术语、测试、双轴 Review 和调试机制讨论团队应用；第 6–7 页建议小范围试点、记录前后差异并按反馈调整。

**值得吸收：**从反复发生的团队问题挑选两三项纪律，保留可比较基线；测试期望来自 Spec/已知样例等独立来源，避免用被测实现重复算出预期。

**具体纠正：**

- 第 2 页将“拒绝在紧密反馈闭环前提出假设”放在 grill-with-docs 介绍中；当前该纪律属于 diagnosing-bugs，不是 grill-with-docs 的直接定义。
- 第 3 页“每个术语有且只有一个含义”应限定在对应上下文。跨领域相同词可以有不同含义，映射和所有权要显式记录；当前原始技能已有多上下文的 glossary 布局。
- 第 3 页 deletion test 的概述不够精确。原始 codebase-design 要看删除后复杂度是否重新散落在调用者；复杂度只是没消失，不能说明被删模块一定设计良好。
- 第 4 页“同一个 Bug 不会出现两次”不是回归测试的保证；只对被覆盖场景和已运行验证提供保护。
- 第 5 页把“建反馈闭环”简化为“先建测试再看代码”，并建议打回无法复现的报告。实际故障仍需收集证据，间歇性问题、硬件故障和线上事故不能因此拒收。当前原始调试技能也支持请求、CLI、trace replay、fuzz、差分及人工辅助反馈，而不只限单元测试。
- 第 6 页“两个小时有答案”和 review 轮数 3.2→1.5 是建议/示例，不能当成本团队已实现的效果。
- “永远不 abort 合并”“原型没有测试/错误处理”等不能作为通用组织约束。必须保留恢复路径，并为实验选择足以回答问题的判据；原型结果不能直接认定为可交付实现。

**对本项目：**吸收试点与测量方法，删除绝对承诺和不适合真实故障处理的硬规则。

## 对此前讨论的五项实质调整

1. **从先确定 OS 分层，转向先确定工程记录与交接协议。** 最小实体是来源/证据、决策、Spec、任务、Handoff、验证和评审视图；暂不按这些名字拆独立服务。
2. **把状态分成三类。** 内容认知状态（观察/推断/提案）、阶段就绪状态（可用/缺输入/不适用）、运行状态（未执行/执行中/失败/已验证）不能混用。格式通过、方案获接受、测试通过和最终交付各是不同事件。
3. **同一工程产物可有多个有来源的视图。** AI/研发详情、合作方摘要、测试关注点和架构图从版本化源记录派生；评审意见修改源决定后再生成，避免多个文档各自独立漂移。
4. **按任务与风险裁剪流程。** 澄清只询问不能从已有资料获取且阻塞下一步的决定；对无关未决问题保留记录。简单变更可以短流程；复杂业务分析、BSP 调试和高风险改动各有专门检查。
5. **以一个真实任务证明机制有效。** 先完成事实查找、变更规格、实施/验证与交接；让接手者仅靠记录理解结果。之后才比较多 Agent 是否降低周期、人工成本或漏检。可恢复任务状态、结构化交接和多 Agent 是三个独立能力。

## 建议的最小设计轮廓

```text
现有需求/代码/接口/运行证据
          ↓
Context Pack（来源、版本、事实、冲突、未知项）
          ↓
领域/系统分析 + 架构取舍（按任务需要）
          ↓
Handoff（决策、假设、阻塞范围、下一位责任人）
          ↓
Spec / Delta → 可验证任务 → 实施与验证
                                  ↓
                Standards Review + Spec Review
                                  ↓
                    交付记录 + 必要的知识修订

源产物 ──→ 面向不同读者的评审视图
新证据 ──→ 修订受影响的源产物与下游结果
```

此图是本次评阅提出的候选流程，不是六篇文章或厂商共同发布的标准。最小实现可使用 Git、Markdown/YAML/JSON 和已有测试工具；根据真实需求再加数据库和调度器。

对于 Linux BSP / Safety / Robot，System Profile 至少要能够表达对应版本和配置、执行上下文、线程/IRQ、锁与阻塞、状态转换、故障响应和时间预算。哪些字段必须存在取决于该任务；采用领域词汇不等于采用业务后端的 DDD 战术模式。

## 本轮原始来源快照

除了 PDF，本轮直接读取了原始仓库 README、树与对应技能定义。仅用于核对，没有安装或执行这些技能，也没有修改 AI-SDLC 仓库。

- Matt Pocock：commit `b0618bc436ad893b3c5e84e55fba86586d34a404`。
  - [README](https://github.com/mattpocock/skills/blob/b0618bc436ad893b3c5e84e55fba86586d34a404/README.md)
  - [ask-matt](https://github.com/mattpocock/skills/blob/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/engineering/ask-matt/SKILL.md)
  - [domain-modeling](https://github.com/mattpocock/skills/blob/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/engineering/domain-modeling/SKILL.md)
  - [code-review](https://github.com/mattpocock/skills/blob/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/engineering/code-review/SKILL.md)
  - [diagnosing-bugs](https://github.com/mattpocock/skills/blob/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/engineering/diagnosing-bugs/SKILL.md)
  - [to-tickets](https://github.com/mattpocock/skills/blob/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/engineering/to-tickets/SKILL.md)
- Domain Architecture：commit `7b9fcde7359d65b688fdfe735ea32d1dd786d959`；GitHub API 确认当前仓库为 huahill/domain-architecture-skills。
  - [README](https://github.com/huahill/domain-architecture-skills/blob/7b9fcde7359d65b688fdfe735ea32d1dd786d959/README.md)
  - [Handoff Contract](https://github.com/huahill/domain-architecture-skills/blob/7b9fcde7359d65b688fdfe735ea32d1dd786d959/skills/domain-architecture-workflow/references/handoff-contract.md)
  - [JSON Schema](https://github.com/huahill/domain-architecture-skills/blob/7b9fcde7359d65b688fdfe735ea32d1dd786d959/schemas/domain-architecture-handoff.schema.json)

这些源码能确认项目声明和流程定义，不能单独证明使用效果。AAIC 属于文章作者的实践报告；本轮没有获得其私有实现、看板数据或受控比较，故保留效果证据限制。
