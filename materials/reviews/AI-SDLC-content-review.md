# AI-SDLC 分享会话内容核对

核对日期：2026-10-08。对象：分享会话《SDLC介绍》，包括最终总结与此前讨论。

本记录区分已核对的公开事实、需要限定的表述、架构提案和暂未核实的引用。读取源码仓库与公开文档不代表亲自复现了其构建、性能数据或产品效果。未修改 AI-SDLC 仓库。

## 主要结论

原讨论可作为需求探索材料，尚不适合直接充当实现规范。主要问题是把设计愿景、个别案例和工具介绍合并成了过于确定的行业结论。保留目标、约束、任务交接和验证证据的方向，但应修正下列内容。

| 原讨论表述 | 核对结论 | 建议修正 |
|---|---|---|
| Anthropic 偏流程重构，OpenAI 偏组织重构 | 分类过度简化 | OpenAI 官方指南也按 Plan、Design、Build 等 SDLC 阶段展开；这种划分只能作为讨论角度，不应称为厂商边界。Anthropic Playbook 本轮未直接读到原文。 |
| Knowledge + Task State + Execution + Runtime + Evaluation 是 AI Engineering OS 的最终模型 | 本次讨论的架构提案 | 标为候选逻辑架构；没有证据表明它是官方标准或必须拆成独立服务。各层职责和数据所有权尚需定义。 |
| 代码不是瓶颈；工程系统大于模型能力；未来工程资产有固定排序 | 无通用实证支持 | 瓶颈取决于任务、模型、仓库、测试、硬件与团队。以交付周期、返工率、质量、成本测量，避免固定价值排序。 |
| 编译器第一次成为 AI 的反馈环境 | 历史性措辞不成立 | 改成“编译器、测试和分析工具提供可执行反馈”；不声称该案例首次创造了反馈闭环。 |
| Bun 从 Zig 重写为 Rust | 基本事实已核对 | 官方 PR #30412 标题为 Rewrite Bun in Rust，记录于 2026-05-14 合并；当前官方 README 描述其运行时使用 Rust。PR 同时提到仍有优化与清理工作。不要把所有第三方数量、成本、性能或 Agent 组织细节都当成已核实事实。 |
| Anthropic Lean / Prove2Me 实验能启发任务持久化 | 部分机制已核对 | Prove2Me 文档支持形式化声明、证明/归约、里程碑、失败历史和开放叶子查询；Anthropic 的 Fermat 仓库说明完整机器检查及第二内核验证。具体发布日期、Agent 数量和内部 harness 本轮未核实。 |
| 子任务全部通过，父任务自动完成 | 数学与软件的验收语义不同 | Prove2Me 中，经过检查的归约可在其子定理获证后闭合。普通软件任务必须另做集成、行为与非功能验收，子任务测试通过不自动证明整体正确。 |
| Task Graph 必须是 DAG | 对执行依赖可以成立，对全部工程状态不成立 | 工程过程有重试、返工与迭代。每个执行版本可保持无环依赖，生命周期用状态机/事件记录。备选方案需要表示“某一方案成立即可”和“该方案的前提全部成立”，避免把备选依赖并成全部必做。 |
| Agent 可以离开，任务状态必须留下 | 值得保留的设计原则 | DAG 本身不提供持久化、并发领取、租约、提交幂等、版本绑定或失效传播。只有跨会话协作确实需要时才引入相应机制。 |
| Context Compiler 是必备基础设施 | 命名是架构隐喻，不是已确认的通用标准组件 | 先定义可观察行为：查找来源、筛选相关内容、处理冲突、保留版本、控制上下文预算、标注缺失。检索到相关内容不等于获得完整或正确上下文。 |
| Markdown 不适合作为知识模型，应该升级为 Knowledge Graph | 格式和模型混淆 | Markdown 可以保存结构化元数据、链接、表格和 Mermaid。图数据库也可能保存错误或过时关系。先解决 ID、来源、版本、关系语义和维护责任，再决定是否需要专门图存储。 |
| Evaluation 是 AI 时代新增的软件质量体系 | 与已有工程实践的边界不清 | 测试、静态分析、安全分析和人工评审继续有效；Agent evals 补充评估任务成功、工具行为、成本与回归。LLM 评判不能代替确定性检查或安全验收。 |
| AI 不替代 V 模型，并能通过自动化得到安全保证 | 前半可作为建议，后半需要严格限定 | AI 可辅助需求到验证的追溯。ASIL 等目标仍须落实适用标准、风险分析、验证证据和相关审查；AI 生成文档或测试通过不等于认证完成。 |
| RT 路径禁止 mutex；IRQ context cannot sleep | 示例规则过于宽泛 | hard IRQ 和其他不可睡眠原子上下文不能取得睡眠锁；可抢占任务上下文可使用 mutex/rt_mutex。PREEMPT_RT 改变部分锁语义；实时路径应约束最长阻塞、优先级反转及延迟预算。IRQ 线程与 hard IRQ 要区分。 |
| thermal worker → 阻塞 rpmsg → RCU stall | 不能作为普遍因果链 | 官方 rpmsg 文档说明 rpmsg_send 在 TX buffer 不足时可能等待，rpmsg_trysend 可立即失败。但普通 worker 睡眠本身不充分导致 RCU stall；需要检查 RCU 临界区、抢占/中断状态、调度饥饿及目标 BSP 的实现。异步 worker 是否改善问题须实测。 |
| TeamAI 只有知识检索，没有知识建模 | 对当前能力的描述不完整 | 官方 README 已列出 codebase graph 和 teamwiki；Team Context、Team Improvement 明确标 beta。具备代码图能力并不等于拥有完整运行时、时序或安全模型；支持矩阵也存在工具间差异。 |
| Cole Medin 有 33 个 skills，是完整固定流程 | 数量与定位应更新 | 本轮 README 写 35，仓库树检索到 36 个 SKILL.md，说明 README 与树也可能不同步。作者明确说“Nothing here is a framework”，核心是可选择修改的 prime → plan → implement → validate → review → commit → PR。不可用旧数量定义能力，也不应要求每个任务走完全部阶段。 |
| show-me 是结构理解层，ELI5 是语义理解层 | 可用的个人分类，不是硬边界 | HumanLayer 原文确实支持紧凑可视表达，包括树、图、伪代码、类型与签名、diff 和 HTML；它也承认图可能质量不佳。两种表达都能解释结构与原因，均不能自动保证事实正确。 |
| Hindsight 是长期工程记忆，因此 ask-matt 长期记忆五星 | 定位与效果混淆 | Hindsight 是通用 Agent memory，官方提供 retain/recall/reflect 等能力。工程适配效果需用自己的案例测试；不能由记忆工具的介绍推出 ask-matt 实际能力或知识正确性。 |
| 工具“最成熟”、★★★★★、没有完整替代品 | 未提供可复现实验 | 删除排名，改成带版本的能力矩阵；以相同任务、输入、验收、成本和人工介入量比较。 |

## 后续设计应保留的基线

1. 人与 Agent 共用明确目标、约束和验收条件。
2. 代码、文档、模型、规则和测试均需来源与版本；不指定固定价值排名。
3. 任务记录保存输入版本、产物、验证结果和未解决前提，区分“已提交”“已检查”“已验收”。
4. System Model 描述系统；Task Model 描述工作。两者通过 ID 和证据关联，但不必预先建设图数据库。
5. 使用现有开发工具和最小流程验证一个真实任务，再决定是否增加多 Agent、调度系统或长期记忆。
6. 将厂商公开事实、项目自身约束、架构假设及待核验说法分别标注；规则附适用条件与例外。

## 本轮直接读取的主要来源

- OpenAI：[Building an AI-Native Engineering Team](https://learn.chatgpt.com/guides/build-ai-native-engineering-team)。原 developers.openai.com 路径已重定向到此页面，确认 Delegate / Review / Own 及按生命周期阶段的指南。
- Bun：[官方 PR #30412](https://github.com/oven-sh/bun/pull/30412)、[官方 README](https://github.com/oven-sh/bun/blob/main/README.md)。PR 日期与描述来自 GitHub API；尚未核实官方博客中的完整迁移过程与统计。
- Anthropic：[fermats-last-theorem 官方 README](https://github.com/anthropics/fermats-last-theorem/blob/main/README.md)。其中验证结果是作者报告，本轮没有运行其大型构建/第二内核检查。
- Prove2Me：[Workspace README](https://github.com/prove2me/prove2me_workspace/blob/main/README.md)、[solver 文档](https://github.com/prove2me/prove2me_workspace/blob/main/references/mission_solver.md)、[证明提交与归约](https://github.com/prove2me/prove2me_workspace/blob/main/references/prove.md)、[贡献与修改规则](https://github.com/prove2me/prove2me_workspace/blob/main/references/contribute.md)。当前平台文档不等于 Anthropic 当时内部 harness。
- Tencent：[TeamAI README](https://github.com/Tencent/teamai-cli/blob/main/README.md)。能力表与 beta 标签是项目声明，没有实测产品。
- Cole Medin：[skills README](https://github.com/coleam00/skills/blob/main/README.md)、[plan-architecture](https://github.com/coleam00/skills/blob/main/.claude/skills/plan-architecture/SKILL.md)，另读取 GitHub main 树以计数。
- HumanLayer：[show-me 原文](https://www.humanlayer.com/blog/show-me-skill)、[当前 skill 定义](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md)。本轮仅读取用于核对，没有执行该 skill。
- Hindsight：[官方 README](https://github.com/vectorize-io/hindsight/blob/main/README.md)。其产品和 benchmark 宣称不等于本项目效果验证。
- Linux：[锁类型与 PREEMPT_RT](https://github.com/torvalds/linux/blob/master/Documentation/locking/locktypes.rst)、[RCU stall 原因](https://github.com/torvalds/linux/blob/master/Documentation/RCU/stallwarn.rst)、[rpmsg API](https://github.com/torvalds/linux/blob/master/Documentation/staging/rpmsg.rst)。主线文档仅提供通用参考，最终规则须核对项目的 kernel/BSP 版本。

## 未完成的一手核验

本轮 www.anthropic.com、anthropic.com、claude.com、academy.claude.com 与 bun.com 请求返回 403。因此未直接核实 Anthropic Playbook、Context Engineering、Agent Evals 原文及 Bun 博客细节。这个访问结果不能证明文章不存在或原讨论错误；上表明确保留相关不确定性。ask-matt 私有实现和原会话中的上传附件未在本轮获得，关于其实际能力的结论也不成立。
