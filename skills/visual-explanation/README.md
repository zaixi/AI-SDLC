# Visual Explanation

统一入口为 **`visual-explanation`，当前版本 0.5.0**。2026-10-15 采用原 `visual-explanation_2` 的冻结正文，替换 0.4.2；只调整名称、版本元数据和调用提示，没有新增或改写绘图规则。

用合适的图、表、树、diff、代码或 HTML 帮助人理解当前内容，领域不限。简单内容就地解释，复杂内容按理解需要展开；内容研究、领域决策和知识管理由调用任务负责。

## 安装与调用

仓库只维护本目录这一份正式视觉 Skill。将本目录安装到客户端支持的 Skill 位置，运行文件为：

```text
visual-explanation/
├── SKILL.md
├── LICENSE.show-me
└── agents/
    └── openai.yaml
```

使用 `$visual-explanation`，或让上层入口在需要视觉表达时选择它。没有设置仅允许手动触发的标志；实际发现和自动匹配取决于客户端。`agents/openai.yaml` 是支持该文件的客户端的可选显示配置，不是其他 Agent 的运行依赖。

已安装旧副本时，用这些运行文件更新 `visual-explanation`，移除旧的 `visual-explanation_2` 安装，避免保留两个入口。本次合并只更新仓库，没有修改其他机器的安装。

mermaid-diagrams、diagram-design、answer-me-with-html 都是可选实现能力，使用条件以 SKILL.md 为准；没有默认安装要求。缺失时使用可用工具或直接生成，不把历史评测中的依赖当作当前环境已安装。

## 验证与后续维护

在仓库根目录运行：

```bash
python scripts/validate_visual_skill.py
```

维护校验需要 Python 3 与 PyYAML，检查唯一视觉入口、名称与目录、版本元数据、调用提示和运行文件引用。它不验证客户端安装、自动发现、扩展调用或实际图解质量。

后续生成评测只读取本目录的运行文件，在 [评测目录](../../evaluations/visual-skills/README.md) 新建轮次。原始输入、回答、图片、日志和历史快照保持原样；维护文档和旧结论不提供给生成模型。

只有实际使用中反复影响理解、且能追溯到指令缺失或冲突的问题，才作为窄修改候选；不把每次小错误追加成通用规则。

## 采用依据与历史

- [两例比较：去重计数与复杂平台总览](../../evaluations/visual-skills/2026-10-14-v2-v042/comparison.md)
- [增补三例：缺失趋势、多实例与局部 SVG 修改](../../evaluations/visual-skills/2026-10-15-v2-expanded/comparison.md)
- [合并记录与完整性验证](../../evaluations/visual-skills/2026-10-15-consolidation/README.md)
- [0.4.2 完整归档](../../evaluations/visual-skills/history/visual-explanation-0.4.2/)
- [原 `_2` 及其三轮原始评测](../../evaluations/visual-skills/history/visual-explanation_2/)

五类任务中，两版关键内容基本相当；原 `_2` 的复杂平台分段图更便于追关系，0.4.2 的单页速查更集中。小样本、外部渲染反馈和未安装可选扩展等限制仍适用。本次没有重新生成答案，正文相同不等于新名称的客户端发现已经验证。

本 Skill 基于 [HumanLayer show-me](https://github.com/humanlayer/skills/blob/bba9d13ab34f0a87f1cc33df4dd196372393ddfc/plugins/show-me/skills/show-me/SKILL.md)，保留其 [MIT 许可证](LICENSE.show-me)。
