# SDD 工具链的借鉴与复用

核查日期：2026-09-24。目标是评估与本项目方法的适配，不安装、不执行这些上游流程，也不据此宣称效率改善。读取官方主干 README、实际模板、skill、schema 与 workflow；以下链接固定到所读版本。

**简要判断：都值得借鉴，复用对象各不相同。** 以下是结合本项目目标作出的设计建议，不是四家已提供的集成方案，也不是实际使用效果排名。

| 项目 | 最值得取用 | 原样采用前要调整 |
| --- | --- | --- |
| Trellis | 长期知识、任务与会话分层；按任务和角色加载上下文；实现发现回写规格 | 多次人工确认、固定文档展开、平台 hook 差异 |
| Spec Kit | 重要问题优先澄清；spec/plan/tasks 一致性；实现后 converge；可恢复定制流程 | 默认产物与 gate、重复文档、Lean 的人工停点 |
| OpenSpec | 当前规格与本次变更差量；按依赖生成产物；同步和归档 | 提案后强制再次请求实施；归档/文件存在不等于验收 |
| Superpowers | 可视化方案比较；连续执行；TDD/调试/审查；用压力场景验证 skill | 多次设计批准、过细计划、额外审查成本、临时执行记录的长期保存 |

用户于 2026-09-24 明确复用优先级：相同或相近能力采用 mattpocock/skills，其他项目先用于参考和补缺。因此本表是机制调查，不是多框架组合方案，也不要求从四项中选一个。当前只核查源码，没有安装、移植或运行这些工作流。

## Spec Kit：规格到实现的一致性，以及可裁剪的流程

版本：`github/spec-kit@25d43a9482af998dc932142d0398794635a3a5e8`，提交时间 `2026-09-24T01:35:39Z`；MIT。

**它是什么。** CLI 加模板、agent 指令和流程引擎。核心对象是项目原则 constitution，以及每项功能的 spec、plan、tasks。当前核心流程已是 specify → plan → tasks → implement → converge；bug 修复和 idea assessment 是可选扩展的独立入口，不要求每次从完整 SDD 开始。README 示例使用 Copilot skills 模式的 `/speckit-specify` 等调用；其他宿主语法不同，不能把名称当通用 API。[入口与流程](https://github.com/github/spec-kit/blob/25d43a9482af998dc932142d0398794635a3a5e8/README.md)

**值得借鉴的三个机制：**

- **澄清有价值门槛和数量上限。** clarify 只选会影响实现或验证的重要问题，一次会话最多五问，可提前结束；每个接受的答案更新现有 spec，清除冲突旧说法。适合借鉴“问题影响什么”和及时落盘；其推荐选项与短答格式仍可能造成机械接受，五问也不应变成配额。[clarify](https://github.com/github/spec-kit/blob/25d43a9482af998dc932142d0398794635a3a5e8/templates/commands/clarify.md)
- **检查规格、计划、任务是否互相对应。** analyze 查重复、歧义、遗漏、术语与任务覆盖；converge 在实现后重新核对需求和设计，把缺失、部分完成、冲突、额外实现转成有来源的修复任务，不把任务勾选当证据。两者是 agent 分析规约，不等于确定性证明。[analyze](https://github.com/github/spec-kit/blob/25d43a9482af998dc932142d0398794635a3a5e8/templates/commands/analyze.md)、[converge](https://github.com/github/spec-kit/blob/25d43a9482af998dc932142d0398794635a3a5e8/templates/commands/converge.md)
- **流程可以裁剪和恢复。** 已有 Lean preset、项目模板覆盖和自定义 YAML workflows。workflow 逐步保存状态，支持恢复，不应继续把当前 Spec Kit 简化为“只能手动运行重型流程”。[Lean](https://github.com/github/spec-kit/blob/25d43a9482af998dc932142d0398794635a3a5e8/presets/lean/README.md)、[workflows](https://github.com/github/spec-kit/blob/25d43a9482af998dc932142d0398794635a3a5e8/workflows/README.md)

**原样使用的代价。** 默认 plan 展开研究、数据模型、契约、quickstart 等文件；自带 speckit workflow 固定在 spec 和 plan 后设人工 gate。它们可能增加本项目正在减少的阅读和确认负担。Lean 虽短，其 specify 仍要求人先提供 feature directory，implement 遇失败就停止，不能假定“轻量”自动等于自主持续执行。converge 明确不跟踪 Git 历史，且规约主要核查当前代码，不可代替绑定实际产物和环境的验证结果。[plan 模板](https://github.com/github/spec-kit/blob/25d43a9482af998dc932142d0398794635a3a5e8/templates/plan-template.md)、[自带 workflow](https://github.com/github/spec-kit/blob/25d43a9482af998dc932142d0398794635a3a5e8/workflows/speckit/workflow.yml)、[Lean 指令](https://github.com/github/spec-kit/tree/25d43a9482af998dc932142d0398794635a3a5e8/presets/lean/commands)

**复用判断。** 现在吸收有界澄清、需求与任务关联、实现后回查的方法；以后若选择它作为工具基础，优先从 preset/模板覆盖/custom workflow 适配，而非复制整套默认 gate。CLI、流程引擎和模板不是“子 skill”；生成给宿主的具体 agent 指令才可能作为被调用能力。

## OpenSpec：当前规格、变更差量与持续更新

版本：`Fission-AI/OpenSpec@db2309783547a14e150dbcbfc19120e4028446c3`，提交时间 `2026-09-23T21:33:22Z`；MIT。

**它是什么。** CLI 加产物依赖图、Markdown 模板和实际 skills。`openspec/specs/` 保存当前行为规格；`openspec/changes/<name>/` 保存一次变化的 proposal、规格差量、按需 design 和 tasks，完成后同步规格并归档。代表入口是 `/opsx:explore`、`/opsx:propose`、`/opsx:apply`、`/opsx:archive`；扩展 profile 有 continue、verify 等，Codex 使用 `$openspec-propose` 等形式。[入口及宿主差异](https://github.com/Fission-AI/OpenSpec/blob/db2309783547a14e150dbcbfc19120e4028446c3/README.md)

**最值得借鉴的机制是“有效全貌与本次变化分开，但始终能归并”。** 规格用 ADDED / MODIFIED / REMOVED / RENAMED 表达增量，需求带 WHEN/THEN 场景；design 保存技术决定、原因、备选与风险，避免重复 proposal；每项任务说明怎样验证，各组随工作完成测试和文档，不集中拖到最后。schema 用 `requires` 描述产物依赖，可以定制少量、更合适的产物。[真实 schema](https://github.com/Fission-AI/OpenSpec/blob/db2309783547a14e150dbcbfc19120e4028446c3/schemas/spec-driven/schema.yaml)

这适合我们“下一轮看变化，需要时回到最新整体”的目标。持续行为规格适合作为维护入口；归档中的设计理由仍需从当前模块入口可发现，归档动作本身不能证明接手知识充分。schema 可保存在项目中并版本控制，也可减少文件；自定义 fork 不自动获得上游模板更新。[schema 定制](https://github.com/Fission-AI/OpenSpec/blob/db2309783547a14e150dbcbfc19120e4028446c3/docs-lab/customize/schemas.md)

**必须看清的边界：**

- `status` 的产物 done 主要表示文件存在，不代表内容、实现或验证完成。`verify` 对照任务、需求、场景和设计，区分缺失与未验证；其中正确性仍采用代码搜索和推断、检查测试是否存在，没有普遍要求实际运行并绑定环境与被测快照，不能作为完整交付证据机制。[propose 中的状态说明](https://github.com/Fission-AI/OpenSpec/blob/db2309783547a14e150dbcbfc19120e4028446c3/skills/openspec-propose/SKILL.md)、[verify](https://github.com/Fission-AI/OpenSpec/blob/db2309783547a14e150dbcbfc19120e4028446c3/skills/openspec-verify-change/SKILL.md)
- 当前 propose 明确要求产出方案后停止，即使最初要求已包含实施，也要等新请求。apply 能连续完成任务，但遇错误或阻塞就要求等待指导；这些比本方法“授权持续、局部自主修复、仅阻塞相关工作”更保守，不能原样叠加。[propose](https://github.com/Fission-AI/OpenSpec/blob/db2309783547a14e150dbcbfc19120e4028446c3/skills/openspec-propose/SKILL.md)、[apply](https://github.com/Fission-AI/OpenSpec/blob/db2309783547a14e150dbcbfc19120e4028446c3/skills/openspec-apply-change/SKILL.md)
- archive 负责规格同步与历史收纳，有任务/产物未齐时允许提示后确认继续；“已归档”不是“用户已接受、测试全通过”。本方法仍需分别表达接受、实现、验证和发布状态。[archive](https://github.com/Fission-AI/OpenSpec/blob/db2309783547a14e150dbcbfc19120e4028446c3/skills/openspec-archive-change/SKILL.md)

**复用判断。** 现在吸收当前规格＋变更差量、行为场景、设计理由、产物依赖和及时归并；以后可把 OpenSpec 作为文档与变更管理基础，复用 CLI、适配 schema，并选用具体 skills。它有真实 `SKILL.md`，但其操作依赖 OpenSpec 项目上下文、CLI 与宿主，不能仅复制一段技能文字便声称集成完成。图文审阅与理解质量仍需本项目的呈现规则，不能由新增规格文件替代。

## 对本方法的初步取舍

两者都有可运行资产，不仅是理念；也都不能单独证明人的理解、运行证据和新会话接手已经解决。现阶段借鉴机制、收敛方法，不叠加安装。未来应选择一套主文档与变更基础，保留唯一有效入口；另一套只复用兼容的局部能力，避免维护重复 spec、plan、tasks 和审批链。

## Trellis：让任务获得需要的上下文，并回写工程知识

版本：`mindfold-ai/Trellis@e77ae89f648a78d5859fa2e8ac314655898421a5`，提交时间 `2026-09-11T17:41:36Z`。核查版本的 [LICENSE](https://github.com/mindfold-ai/Trellis/blob/e77ae89f648a78d5859fa2e8ac314655898421a5/LICENSE) 标识 AGPL-3.0；其他三项本次核查版本为 MIT。这里记录版本事实，不预先决定代码复制或分发方式。

**它是什么。** CLI、模板、hooks、任务脚本和 agent 指令组成的开发环境。`.trellis/spec/` 存长期工程约束，`.trellis/tasks/` 存任务需求、设计与状态，`.trellis/workspace/` 存跨会话日志。这个分层比把所有东西写进会话摘要更适合维护；但它不是一份可以直接嵌套调用的单独 skill。[工作流模板](https://github.com/mindfold-ai/Trellis/blob/e77ae89f648a78d5859fa2e8ac314655898421a5/packages/cli/src/templates/trellis/workflow.md)

**最值得借鉴的是按任务和角色提供上下文。** `implement.jsonl` 和 `check.jsonl` 分别列要读取的资料及理由，运行时加载这些文件和任务材料。实际注入代码包含读取预算、截断说明、缺少清单时的提示；不同平台使用 hook 推送或 agent 主动读取，不能假定所有宿主能力相同。把文档写在磁盘上和让接手者读到相关部分，是两项工作。[注入源码](https://github.com/mindfold-ai/Trellis/blob/e77ae89f648a78d5859fa2e8ac314655898421a5/packages/cli/src/templates/shared-hooks/inject-subagent-context.py)

`update-spec` 要求将实现中的设计理由、错误模式、接口契约与测试点回写工程规格；这些机制与我们的知识接力目标很接近。[update-spec](https://github.com/mindfold-ai/Trellis/blob/e77ae89f648a78d5859fa2e8ac314655898421a5/packages/cli/src/templates/common/skills/update-spec.md)

**需要适配的默认行为。** brainstorm 先要求创建任务许可，非平凡任务至少获得一次新的用户回复，最终规划总结后再等明确实施批准；先前的“开始做”不能替代。工作流还要求提交计划确认。复杂任务的固定 PRD/design/implementation plan 和跨层规格结构，也可能增加我们希望减少的产物和审阅负担。[brainstorm](https://github.com/mindfold-ai/Trellis/blob/e77ae89f648a78d5859fa2e8ac314655898421a5/packages/cli/src/templates/common/skills/brainstorm.md)

**复用判断。** 优先借知识分层、任务阅读清单、上下文加载和 update-spec 能力。以后可以用它承载上下文与恢复，也可以只实现这些机制；本次核查未发现主流程对 OpenSpec、Spec Kit 或 Superpowers 的明确互操作协议。把外部资料纳入阅读清单是我们的适配建议，不是已验证的整套集成。branch/commit/PR 元数据和日志有助追溯，但不能自动证明证据完整绑定被测工作区与环境。

## Superpowers：可视化设计与连续执行都有现成机制

版本：`obra/superpowers@5bf4e78011075bcfc0dc295f0724994cd123ee71`，提交时间 `2026-09-19T00:31:35Z`；MIT。它既有可组合 skills，也有启动指令与流程约束；启用整个框架会改变 agent 的默认行为。[using-superpowers](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/using-superpowers/SKILL.md)

**值得优先借用：**

- **视觉比较与反馈。** brainstorming 的 visual companion 能展示方案、图和原型，记录浏览器选择；按问题判断是否需要视觉表达。它比 show-me 的呈现指导多了交互服务，可以作为后续评审界面的参考。使用项目目录时可保留页面，默认建议忽略这些运行文件，因此重要方案与决定仍需提升到版本化资料。[visual companion](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/brainstorming/visual-companion.md)
- **连续执行和局部裁决记录。** 当前 `executing-plans` 明确任务之间不反复询问，用进度账本记录偏离与理由，最后做整体审阅；`subagent-driven-development` 则提供逐任务实现与审阅、限定修复复核范围等机制。两种方式的成本不同，不需要普遍采用更多 agent。[executing-plans](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/executing-plans/SKILL.md)、[subagent-driven-development](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/subagent-driven-development/SKILL.md)
- **完成声明要有实际证据。** verification-before-completion 要求运行检查、读输出和退出状态，不能用自信或下级报告代替核查。task-done 脚本会运行命令并在成功后记录提交范围、命令和结果；但仍不是包含脏工作区、依赖及环境的完整证据绑定。[verification](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/verification-before-completion/SKILL.md)、[task-done](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/executing-plans/scripts/task-done)
- **用行为检验 skill。** writing-skills 把压力场景、无 skill 基线、加入指导后的行为对照用于技能验证。适合借鉴到我们的流程评价，比让 agent 复述规则更有意义；遵从指令仍不等于产品质量提高。[writing-skills](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/writing-skills/SKILL.md)

**需要适配的代价。** brainstorming 虽区分 spike、bounded、architectural，但每条路径都要求新批准，架构路径还逐段确认设计、审阅书面规格、再审阅计划。writing-plans 要求细到文件、完整代码和测试步骤，可能将尚需探索的设计过早固定。执行层的自主裁决也需遵守我们的目标与承诺边界，不应把所有业务歧义都交给 agent 决定。[brainstorming](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/brainstorming/SKILL.md)、[writing-plans](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/writing-plans/SKILL.md)

另一个与接力直接相关的取舍是：SDD 工作目录自带忽略规则，执行指南要求最终清理工作目录，并把裁决汇总到最终回复。借用时应将值得长期保留的理由和验证结果写回工程资产，不能误认为被忽略的账本会自动存在于 Git 历史。[工作目录实现](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/subagent-driven-development/scripts/sdd-workspace)、[执行结束规则](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/executing-plans/SKILL.md#finish)

## 与现有调查的两处事实校正

本轮研究期间，仓库新增了 [Claude 的同类调查](related-work-2026-09-24.md)。保留该原稿，以下用固定版本源码补充，避免基于差异作出错误取舍：

1. **OpenSpec 归档不是删除 proposal/design/tasks。** archive 的实际操作将整个变更目录移动到 archive，当前规格被同步，历史规划产物仍留存。故可说它区分当前规格与历史变更，不能说设计理由“用完即弃”。[archive 源码](https://github.com/Fission-AI/OpenSpec/blob/db2309783547a14e150dbcbfc19120e4028446c3/skills/openspec-archive-change/SKILL.md)
2. **不能概括为这些框架都要求人持续值守、都没有停止条件。** 上述 Superpowers 执行 skill 已明确连续执行和停点，Spec Kit 已有可恢复 workflow。问题在于默认授权/停点是否适合本项目，以及跨步骤资料与质量是否有效，而不是完全没有这类机制。

同理，存在澄清或图文 skill 不等于“少问且理解充分”已被证明。源码能证明机制存在，效果需要实际任务评价；当前主干能力也不等于已发布安装包。本次未做安装、跨框架集成或成效实验。

## 对我们后续设计的建议

按用户明确的优先级，先将所需能力映射到 mattpocock/skills：有相同或相近功能时采用 Matt 的实现，并对照本方法调整默认行为。OpenSpec 的规格差量、Trellis 的上下文与知识回写、Superpowers 的视觉反馈及验证纪律、Spec Kit 的有界澄清与一致性回查，先作为改进现有能力的参考。

仅当 Matt 的能力缺失或适配后仍不能满足目标时，才评估外部补充或最小自建；不预设必须从 OpenSpec 与 Spec Kit 选一个，也不同时启用多套全流程控制。以上替代本报告此前按多个项目拼装的建议；源码事实与局限保持不变。

具体组合要先对齐任务标识、资料位置、状态含义、授权、失败处理和证据范围。这属于后续适配工作，不能靠在总 skill 中依次写四个名字就视为实现。图文可理解性、合理的讨论轮次、证据有效性及真实维护接手仍需端到端验证。
