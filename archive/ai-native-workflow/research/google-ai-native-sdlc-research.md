# Google / DORA AI-native SDLC 研究

截至 2026-09-21，已实际阅读 Google、Google Cloud、Google Research、Google Developers 和 DORA 的一手页面；DORA 2024/2025、AI Capabilities Model 与 2026 ROI 报告已下载官方 PDF 并读取相关正文/方法章节。这里记录可迁移的工程机制，不把 Google 的产品设计或调查相关性直接当作普遍因果结论。

## 结论先行

Google 资料对通用方法新增的约束可以归纳为五点：

1. **用小批量、频繁提交和可回滚控制 AI 生成速度**。速度与稳定性必须分别观测；生成量增加不能替代集成、回退和生产验证。
2. **把验证设计成生产系统的一部分**。作者侧早反馈、结构化/确定性检查、独立分诊和跨变更检查应组合使用；不能把最后一次人工 review 当作唯一质量机制。
3. **把上下文、数据和系统状态作为工程基础设施**。agent 需要可访问且有权限边界的代码、文档、依赖图、威胁模型、运行反馈和历史决定；否则只会更快地产生返工。
4. **交付给人的是可验证 artifact 和差异，而不是原始日志**。图、计划、截图、演示、测试结果和已知限制应从同一工作状态生成，并允许异步评论后继续执行。
5. **按意图和风险改变交互深度**。同一人在探索、集成、加速和学习时需要的控制面不同；方法应提供从高层结果到代码/证据的连续下钻，并对低技能或高影响任务默认更强护栏。

这些补充与当前 `ai-native-workflow` 的“持续系统模型—可验收增量—授权内自主执行—证据交付”相容；但它们要求把回滚/小批量、验证基础设施、上下文平台和结果度量写成工程内核，而不只是 agent 执行层的选项。

## 逐篇证据

### 1. DORA 2024 Accelerate State of DevOps Report

- **来源/日期/性质**：[DORA Research: 2024](https://dora.dev/research/2024/dora-report/)，2024-10-22（[发布公告](https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report)）；研究报告。已读[官方 PDF](https://dora.dev/research/2024/dora-report/2024-dora-accelerate-state-of-devops-report.pdf)正文 pp.39–40。
- **实际机制**：报告指出 AI 采用与个人生产力、流动和满意度提升同时出现，但其调查模型还显示交付吞吐和稳定性下降；页面明确强调小批量、健壮测试、用户中心和稳定优先级。速度与稳定性应分开度量，不能以“AI 让人更快”推导“系统交付更好”。
- **对方法的启示**：把变更粒度、测试和回退作为自主执行的默认安全网；交付证据至少覆盖行为正确性和变更稳定性。
- **局限**：这是组织调查与统计关联，不能证明 AI 直接造成某个百分比变化，也不能把报告中的估计当作任何团队的预测值。

### 2. DORA 2025 State of AI-assisted Software Development

- **来源/日期/性质**：[DORA Research: 2025](https://dora.dev/research/2025/dora-report/)；Google 对报告的说明发表于 2025-09-23（[Google 介绍](https://blog.google/innovation-and-ai/technology/developers-tools/dora-report-2025/)）；大样本研究。已读[官方 PDF](https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf) pp.80–82、123。
- **实际机制**：近 5,000 名技术从业者的调查将 AI 描述为组织系统的放大器；报告从单一采用率转向团队 archetype、信任、用户价值和系统条件。Google 页面报告 90% 采用、超过 80% 感知生产力提升、59% 感知代码质量改善，同时仍有 30% 对输出只有少量或没有信任。
- **对方法的启示**：成功标准必须是用户价值、稳定交付和可验证结果的组合，不能用代码行数、token 或接受率代替；工作委托要带上现有系统上下文和失败后的恢复路径。
- **局限**：主要是自报观察数据。方法章节使用 DAG 与 Bayesian 模型，但 p.123 明确将结果解释为考虑观察数据局限的 principled comparisons；数字和实践组合不能直接转化为普遍因果律。

### 3. DORA AI Capabilities Model

- **来源/日期/性质**：[DORA AI Capabilities Model](https://dora.dev/ai/capabilities-model/report/)，最后更新 2025-11-25；[Google Cloud 介绍](https://cloud.google.com/blog/products/ai-machine-learning/introducing-doras-inaugural-ai-capabilities-model)发表于 2025-09-23；研究转实践建议。已读[官方 PDF](https://services.google.com/fh/files/misc/2025_dora_ai_capabilities_model.pdf)的版本控制、增量和能力评估章节。
- **实际机制**：七项放大 AI 效果的组织能力是：清晰且传达一致的 AI 立场、健康数据生态、AI 可访问的内部数据、强版本控制、小批量、用户中心和高质量内部平台。报告说明候选能力来自 78 次深度访谈、文献/专家观点，并在近 5,000 人调查中评估子集。
- **对方法的启示**：在 agent 运行协议之外建立“上下文与平台就绪度”检查；明确允许的工具/数据边界；所有增量保留频繁提交、回滚点和可追溯证据；先确认用户结果，再让 agent 加速实现。
- **局限**：模型是能力框架，不是必须按七项逐阶段执行的 playbook；关联结果不能证明某一能力在不同组织中必然产生相同收益。

### 4. DORA《Balancing AI tensions: Moving from AI adoption to effective SDLC use》

- **来源/日期/性质**：[DORA Insight](https://dora.dev/insights/balancing-ai-tensions/)发表于 2026-03-10；Google 工程师开放回答的主题分析。
- **实际机制**：对 2025 年第三季度 1,110 名 Google 工程师的开放回答，研究归纳代码生成、信息检索、代码评审、测试等使用点，以及 verification overhead、幻觉、知识限制、技术债和 prototype-to-production gap。建议把作者侧反馈前置、使用有上下文的 review agents、坚持小批量，并重新思考传统异步 review 的目的。
- **对方法的启示**：设计证据链时显式记录“验证税”；将自动检查放在生成过程和作者侧，给 reviewer 可读的差异与风险摘要；把原型验证和生产准备分开计量，不能用原型完成时间推断交付时间。
- **局限**：样本是 Google 内部工程师的开放回答，作者明确提醒受提问顺序影响；主题频率是信号，不是总体比例或因果估计。

### 5. Google Research《AI in software engineering at Google: Progress and the path ahead》

- **来源/日期/性质**：[Google Research](https://www.research.google/blog/ai-in-software-engineering-at-google-progress-and-the-path-ahead/)发表于 2024-06-06；内部工程工具实践与产品化方法。
- **实际机制**：Google 以“技术可行性×预期影响”排序，快速迭代并同时监测生产力、满意度和用户体验；利用跨 IDE、代码评审、构建、bug 管理和规划的高质量活动数据训练/改进；观察到无缝嵌入现有工作流比要求用户记住触发功能更易推广，在线 A/B 和直接用户研究比离线代理指标更接近真实价值。文章还将更大规模的诊断到修复视为需要更广泛 benchmark 的方向。
- **对方法的启示**：workflow 不应要求人手动推进每个命令；上下文和反馈应来自实际工程活动；评估要覆盖任务结果、交互成本和真实用户价值，而非只看代码生成准确率。
- **局限**：这是 Google 内部工具的经验，接受率、字符比例等指标不可移植为通用生产力指标；文章谈的是 AI 辅助工具演进，不是完整自治 SDLC 的实证。

### 6. Google Antigravity agent-first development platform

- **来源/日期/性质**：[Build with Google Antigravity](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)发表于 2025-11-20；产品实践/交互建议。
- **实际机制**：将 Editor View 与异步 Agent Manager 分开；agent 跨 editor、terminal、browser 规划、执行和验证；用 Artifacts（任务列表、实现计划、截图、浏览器录屏、walkthrough）替代人阅读 raw tool logs，并支持直接在 artifact 上评论而不强制停止执行；知识库保存可复用上下文。
- **对方法的启示**：统一入口应以可快速判断的 artifact、变更和证据为首屏，日志只做按需展开；异步反馈应能作用于仍在执行的任务；“一个人离开后继续”需要状态与观察面，而不只是更长 prompt。
- **局限**：这是产品团队的功能主张和演示案例，不证明 artifact 一定改善工程结果；界面、browser 工具和 Manager Surface 不是通用方法的必要组件。

### 7. Google Conductor：从命令式 SDD 到自然对话

- **来源/日期/性质**：[Evolving Spec-Driven Development: Conductor Now Supports Antigravity](https://developers.googleblog.com/evolving-spec-driven-development-conductor-now-supports-antigravity/)发表于 2026-07-16；Google Developers 的工具实践。
- **实际机制**：把项目认知从临时聊天移入版本控制的 Markdown `spec.md`、`plan.md` 等持久 artifact；2026 版本从严格命令序列转向自然对话，同时让 agent 自动更新 context 和计划状态，并保持跨工具的项目架构、规则、目标和 track。
- **对方法的启示**：应保留持久、可版本化的系统模型和计划状态，但不把命令顺序当作软件工程本体；自然对话负责降低输入负担，状态记录负责可恢复和跨 agent 连续性。
- **局限**：文章给出的是产品成功率比较和产品叙述，没有公开完整实验设计；`spec.md/plan.md` 文件形式不是所有项目都需要，必须允许小任务使用更小的状态表达。

### 8. DORA《The ROI of AI-assisted Software Development》

- **来源/日期/性质**：[DORA 官方入口](https://dora.dev/ai/roi/report/)，页面更新于 2026-04-22；[官方 PDF](https://services.google.com/fh/files/misc/dora-roi-of-ai-assisted-software-development-2026.pdf)版本 2026.1；研究综合与投资估算框架。
- **实际机制**：要求建立采用前基线，把价值拆为有效工程能力、交付速度/稳定性与用户体验；成本同时包含工具/基础设施、训练、迁移期学习成本和验证负担。净节省时间要扣除验证税，释放的是可重新投入的能力，不能自动等同于现金节省或裁员。样例计算明确允许按本地情况替换假设。
- **对方法的启示**：workflow 自身也要有基线、成本与结果回放；人少参与或 agent 长跑仅是过程现象，必须验证净周期、返工、稳定性及真实可用结果是否改善。
- **局限**：这是有假设的估算与建议，J-curve 和样例 ROI 不是对每个团队的收益预测；“未来指数增长”图示不能作为已证实结论。

### 9. Google Cloud《Using AI agents to secure Google infrastructure》

- **来源/日期/性质**：[Google Cloud](https://cloud.google.com/blog/topics/systems/using-ai-agents-to-secure-google-infrastructure/)发表于 2026-09-18；Google 内部安全 SDLC 实践。
- **实际机制**：每次变更的 pre-submit agent scan 与 nightly post-submit 跨变更 scan 并行；扫描、规则、上下文和分诊 harness 分离；局部 threat model 依赖 live code metadata 与依赖调用图；快速扫描结果由使用 AST、call graph 和安全规则的 triage agent 结构化确认，再由 bug-fix agent 根据漏洞证明提出符合标准的修复。
- **对方法的启示**：质量与安全检查应按反馈时延和覆盖面分层：快速局部检查、确定性/结构化证明、独立或夜间组合检查；agent 不应同时控制生成、评判和放宽规则；修复 agent 生成的补丁仍需进入原变更的可审查路径。
- **局限**：Google 的规模、代码库和安全专用 harness 很特殊；文中高精度、误报率和“每月防止漏洞”数字是该系统的内部结果，不能外推到一般项目。

### 10. DORA《Understanding builder intent in the AI era》

- **来源/日期/性质**：[DORA Insight](https://dora.dev/insights/builder-mindset/)发表于 2025-10-17；混合方法研究与设计框架。
- **实际机制**：用 Founder、Optimizer、Accelerator、Learner 四种随任务变化的 mindset 描述目标、风险、技术熟练度和所需控制深度；建议高抽象层与代码/证据层之间可以无缝下钻，并对高委托信任场景提供默认安全护栏。文章强调“假设任何人都在构建生产系统”。
- **对方法的启示**：不要用固定角色或固定审批次数设计流程；一次工作中可根据目标（探索、集成、加速、学习）切换摘要深度、控制权和验证要求。统一评审入口应既能看结果，也能回到代码、运行和证据。
- **局限**：mindset 是设计框架，不是 SDLC 阶段或经过因果验证的组织分类；生产标准和护栏仍必须按具体风险定义。

## 对 `ai-native-workflow` 的明确增补

1. **把“小批量与明确恢复策略”提升为增量设计规则**：尽可能使增量独立验证、尽早进入版本控制并保存恢复点；存在不可逆迁移时预先设计前向恢复和相应授权；并行 agent 合并后必须有组合检查。
2. **把“证据”分成三层**：生成/作者侧快速反馈；确定性或结构化验证；跨变更、运行环境和真实用户价值的独立验证。单次 agent 自检不能充当独立判断。
3. **建立上下文可用性门槛**：工作契约不仅规定结果和权限，还要声明 agent 可访问的系统模型、内部数据、依赖图、规则、历史决策和运行反馈；缺少上下文时限制自治范围。
4. **重新定义评审入口**：首屏展示目标、用户行为、系统图、差异、风险、测试/运行证据和已知限制；raw logs、完整计划和细粒度调用仅按需展开，artifact 评论不会自动等同于放行。
5. **建立结果和流程的反馈指标**：同时观察用户/产品结果、交付吞吐、稳定性、验证成本、返工和 agent/人交互负担；禁止用 token、代码行数或单一接受率作为生产力代理。

## 与现有方法的边界

这些资料支持“系统先可理解、增量可验证、agent 可异步运行、人的判断集中到目标和异常”的方向，但不支持把 SDLC 固定成若干阶段、把 `spec.md` 或某个 Manager UI 作为必需品，或把企业内部的调查数字当成通用收益保证。Claude/OpenAI 的文章可与这里的能力和证据机制交叉验证；三家资料共同指向的是**可观察的系统、可回滚的增量、内建的验证和按风险分配的人机责任**，而不是一个供应商专属流水线。

## 读过但不作为主要论据的补充

- [Introducing Google Antigravity 2.0](https://www.antigravity.google/blog/introducing-google-antigravity-2)，2026-05-19：异步任务、动态子 agent、hooks、project 权限与 scheduled tasks 是执行层实现参考，不证明多 agent 或无人中途提问普遍更好。
- [Finding balance in the era of tokenmaxxing](https://dora.dev/insights/finding-balance-in-the-era-of-tokenmaxxing/)，2026-06-02：DORA 对以 token 消耗量衡量生产力提出批评；采用率与活动指标可辅助理解使用，不能替代结果。
- [Working in small batches](https://dora.dev/capabilities/working-in-small-batches/)，页面更新于 2025-12-08：可审查和可验证的批量比单次代码产出更关键，不能拆小后又积压到一次大测试/大发布。具体按小时或天划分、API-first 等例子不应变成通用方法的固定要求。
