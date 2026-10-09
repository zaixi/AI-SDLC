# Visual Explanation

把当前内容转换为更容易理解的视觉表达，适用于编程、业务、教学及其他领域。当前版本为 **0.4.0**。

核心文件是 [SKILL.md](SKILL.md)，保留show-me的完整表达主体，加少量选图、忠实表达、可读性和交付规则。

## 目标与范围

输入是当前任务已经提供或读取的内容；输出是图、树、时序、状态、伪代码、diff、SVG或HTML，以及必要的简短说明。

本Skill负责选择表达形式、保留原意、控制信息密度并检查图的显示。不独立研究内容、核实现有系统、作领域决策、安排验证任务或制定知识保存策略。这些工作由调用它的任务负责；本Skill按调用者要求展示或保存。

按需读取[视图选择指引](references/view-guide.md)与[图形约定示例](references/diagram-patterns.md)。复杂内容可展开局部视图，不要求用户记住图种，也不按研发阶段套用固定图集。

## 接入与交付

- 将本目录安装到客户端支持的Skill位置，保留references。它不绑定某个Agent，也不依赖安装特定绘图包。
- 上层入口可使用指针：**需要用视觉表达帮助理解当前内容时，使用visual-explanation。**
- 未设置仅允许用户手动触发的标志；实际发现、自动匹配和调用方式由客户端决定。
- 默认会话展示；需要文件时保留可编辑源，按当前任务要求交付。未渲染验证时如实说明，不将语法通过当作布局或内容正确性证明。

当前版本没有重新做独立生成比较或客户端安装/调用测试；本次是目标和职责范围修订，不宣称质量已经提升。后续需要生成比较时，每组默认2～3份独立输出。

## 来源与更新

复用[Humanlayer show-me固定提交](https://github.com/humanlayer/skills/blob/ca7c8088db69e315a8b2deea43820270457f8f3c/plugins/show-me/skills/show-me/SKILL.md)的完整正文，保留[上游原文件](references/show-me.upstream.md)和[MIT许可证](LICENSE)。更新时比较固定原文件，独立评估上游元数据与本地补充，避免覆盖客户端调用设置；尚无自动拉取上游机制。

可按需使用环境中已有的mermaid-diagrams等能力。用户指定的[来源与测试快照](../../evaluations/visual-skills/2026-10-09-isolated/README.md)已归档，但没有验证自动委托或客户端兼容性。

## 历史记录

0.3.x曾混入工程流程与知识管理要求，已从当前指引移除。历史版本、原始输出和结论保留在[evaluations](../../evaluations/visual-skills/)；这些比较针对旧版本，不代表0.4.0的效果。

- [旧版工程解释说明](../../evaluations/visual-skills/history/engineering-skill-readme.md)
- [旧版实验设计及示例入口](../../evaluations/visual-skills/history/refinement.md)
