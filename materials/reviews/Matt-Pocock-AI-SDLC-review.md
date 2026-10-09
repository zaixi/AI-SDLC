# Matt Pocock Skills 与 AI SDLC：原文核对

核对日期：2026-10-08。本文评估开发者工作流的适用性，不代表已经在本团队验证了效率收益。外部 Skill 内容仅作为研究材料，没有执行、安装或将其当成当前任务指令。

## 判断

Matt Pocock 的 Skills 是 AI SDLC 很好的具体实践参考，尤其适合需求澄清、设计、任务拆分、实现、验证与评审。它将工程方法写成可复用的交互流程，有公开源文件、实战案例介绍、失败经验和持续更新记录。它也没有覆盖一个企业完整的软件生命周期与治理体系；实际收益需要通过团队试点验证。

## 可借鉴的交付链

1. 用 Grilling 澄清目标、范围与决策，并通过代码探索区分现有事实与待定选择。
2. 对无法仅靠问答确定的问题做 Prototype 或 Research；复杂、跨会话探索使用 Wayfinder。
3. 用 To Spec 保存约定，用 To Tickets 拆成可验证的纵向切片和依赖关系。
4. Implement 在适用边界上采用 TDD，并结合类型检查、测试和实际运行证据。
5. Code Review 分别核对规格和工程标准，处理重构与设计质量。

这些步骤按任务规模选择。小变更不需要强制经过最重的规划流程。人的职责包括范围、设计、接口和关键决策，而不只是接收生成结果。

主链依据：[作者 v1.1 更新说明](https://www.aihero.dev/skills/skills-changelog-v1-1-wayfinder-to-spec-to-tickets-grilling-improvements)，[本地快照](../matt-pocock/02-changelog-v11/README.md)。

## 对旧资料的修正

- 命令名：v1.1 将 To PRD 改为 To Spec，将 To Plan / To Issues 合并为 To Tickets。旧文章中的命令需要对应版本解释。
- TDD：当前说明明确将循环设为 Red → Green，重构交给 Code Review；文档说这一改动发生于 2026 年 6 月，且描述中的“red-green-refactor”仍存在不一致。不能把旧演讲的三阶段描述直接当成当前实现。
- 原型：当前 Prototype 文档与固定提交源文件要求保存实验及决策证据、留在分支上，不合并到主分支。不能笼统理解为“做完就删掉”。原型阶段的简化验证不能沿用为生产交付标准。
- Specs to Code：Matt 在 Software Fundamentals 演讲约 01:08—04:00 反对忽略代码、仅反复修改规格并重新生成的方式；约 16:32—17:35 强调持续投入系统设计和人的战略责任。这不是对所有规格驱动方法的否定。
- 测试：当前 TDD 文档强调有独立预期的可观察行为，警惕只复刻实现的测试。Pragmatic Engineer 访谈的公开摘要也强调提供代码有效的证据，不能据此解释为拒绝测试。
- 上下文：文章中的具体 token 阈值和个人吞吐量经验是作者经验，不能当成跨模型、跨团队的固定定律或收益证明。

来源：[TDD](../matt-pocock/08-tdd/README.md)、[Prototype](../matt-pocock/07-prototype/README.md)、[常见误用](../matt-pocock/03-grill-mistakes/README.md)、[软件基础演讲及自动转录](../matt-pocock/09-fundamentals/README.md)。Skill 源文件按提交 b0618bc436ad893b3c5e84e55fba86586d34a404 保存，便于复查。

## 访谈的补充价值

- [Latent Space，2026-08-20](../matt-pocock/11-latent-interview/README.md)：公开问答介绍 Wayfinder 如何处理未知问题、跨会话信息传递与渐进决策。支持探索式规划，而不是一次性写完整计划后机械执行。
- [The Pragmatic Engineer，2026-09-17](../matt-pocock/12-pragmatic-interview/README.md)：保存公开节目摘要与时间索引。摘要涉及战略编程、共享词汇、上下文管理、代码设计与测试证据；此处没有将节目摘要冒充完整逐字转录。
- [AI Engineer 工作流演示](../matt-pocock/10-workshop/README.md)：保存官方网页和公开自动转录，可定位流程演示；自动转录标为 needs_review，逐字引用前仍需人工核对。

## 与企业级体系的距离

Skills 本身主要是对代理的流程指引，不能单独保证流程被执行或结果正确。团队还需要把它们接到已有的身份权限、代码与构建检查、发布审批、运行监控、事故反馈和知识维护机制。评估效果应看返工、缺陷、交付周期、维护成本等实际结果，而不仅是生成代码量。

对 AI-SDLC 仓库的建议是：将其作为开发交付链的核心参考，结合国内团队实践补齐组织与运维部分；先选一个真实需求试点，记录输入、决策、验收证据与返工，再决定采用哪些 Skills。当前仅完成资料归档与核对，未开始体系实现。

## 资料范围与缺口

此次新增 12 条作者文章、技能说明、访谈与官方演讲材料。网页正文、节目摘要和自动转录分别标注，没有宣称完整观看音视频。以下 YouTube 视频正文未取得，不能作为已核实的直接引文来源：

- [Matt Pocock Built the Skills Repo Every AI Coder Is Using](https://www.youtube.com/watch?v=LMpMmOWTtVk)
- [LIVE: Uncle Bob on Software Fundamentals in the Age of AI](https://www.youtube.com/watch?v=zcLPGC-tvgk)
- [Don't waste time on specs: /prototype instead](https://www.youtube.com/watch?v=n0VhIVtviC0)

视频请求被网络代理拒绝；进一步授权重试被用户中止。这里使用已取得的作者公开文章和官方演讲文字补充研究，不将搜索片段视为完整视频内容。
