# AI-SDLC

以现成 Skills 为基础，建立便于人和 AI 理解、设计、评审与维护软件的工作方式，少量补充，并保留跟随上游更新的能力。

## 要解决的问题

- 已有代码和零散文档难以形成系统理解，设计理由往往留在人脑中。
- 新功能、新框架需要从设计阶段就便于后续 AI 理解、修改和验证。
- AI 生成与评审环节割裂，人难以判断变更是否遵守需求和约束。
- 代码更新后文档失真，换会话或 Agent 后容易丢失背景。

同时要求跨 Agent 使用、减少冗长输出，并只长期保存代码难以恢复的意图、约束和取舍。完整背景、需求与选择理由见 [项目需求](docs/project-intent.md)。

## 当前方案

**Matt Pocock Skills 是已选定的主流程基础**，承接需求澄清、领域与模块设计、规格和任务、实现、验证及评审。完整流程尚未接入本仓库。

| 能力 | 采用方案 | 作用 |
|---|---|---|
| 主研发流程 | [Matt Pocock Skills](https://github.com/mattpocock/skills) | 根据任务选择工作入口，衔接设计与交付；[使用指南](docs/matt-skills-guide.md) |
| 视觉表达 | [visual-explanation](skills/visual-explanation/README.md) | 用合适的图、树或差异视图帮助理解 |
| 文字表达 | [Humanizer](skills/humanizer/README.md) | 减少套话和重复，保留必要信息 |
| 优先复用 | [search-before-build](skills/search-before-build/SKILL.md) | 新功能、选型和工具开发前先查现成方案；[来源与改动](skills/search-before-build/SOURCES.md) |

三个辅助 Skill 已保存在本仓库，[AGENTS.md](AGENTS.md) 提供按场景使用的工作约定；日常小修复不要求触发搜索。文件自动发现和指令遵循依赖客户端，不代表已安装到全局或完成跨 Agent 调度。

## 从哪里开始

1. 阅读 [Matt Skills 使用指南](docs/matt-skills-guide.md)，了解工作入口、交付路径和辅助能力。
2. 在目标项目中按 [上游安装说明](https://github.com/mattpocock/skills#installation-30-second-setup) 安装 Matt，先运行 `setup-matt-pocock-skills` 配置任务管理和文档位置。
3. 不确定走哪条路线时，用 `ask-matt` 描述目标和困难，让它推荐入口。原版负责导航，后续用户入口仍需主动触发，不是自动执行整条流程。

小而明确的任务可直接实现；需要规格与拆分时，再采用 `to-spec → to-tickets → implement 或 implement-spec`。各 Skill 的详细职责和适用场景只在指南中维护。

## 当前状态与待验证事项

已完成主流程选型和三个辅助 Skill 的接入。Matt 的安装范围、单入口衔接、各客户端适配，以及实际项目中设计理由能否延续到下一次修改和评审，仍需验证。

文档维护补充 Addy 与审阅工具 OpenCodeReview 目前均为候选。现有小样本评测不足以证明文档漏更新已解决；采用状态和依据见 [项目需求](docs/project-intent.md#文档维护补充评估)。

## 背景与依据

- [项目背景、痛点、约束与决定](docs/project-intent.md)
- [人判断什么，证据怎么留](docs/method.md)：设计稿，未在真实任务中试运行
- [研究资料与来源索引](materials/README.md)
- [主流程候选的机制比较](materials/reviews/AI-SDLC-workflow-deep-comparison-20261015.md)
- [评测报告、历史记录与存储约定](evaluations/README.md)
