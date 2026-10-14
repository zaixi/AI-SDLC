# visual-explanation_2

用合适的视图帮助人理解文字信息。简单内容就地解释，复杂内容按理解需要展开；适用于软件、业务、教学和其他领域。

本版于 **2026-10-14 冻结**。入口为 [SKILL.md](SKILL.md)，保留 show-me 的表达主体以及按需使用专业工具的选择。冻结时只更新名称和调用提示，没有继续添加绘图规则。

## 使用

运行时文件为 `SKILL.md`、`agents/openai.yaml`、`LICENSE.show-me`。安装时复制这三个文件及其目录结构即可；`evaluation/` 是维护和评测材料，不需要安装或提供给生成模型。

可显式使用 `$visual-explanation_2`；自动选择未被禁用。本会话的 skill 目录已识别该名称，但未另做宿主调用测试。名称按用户要求保留下划线，官方 `quick_validate.py` 的连字符命名检查仍不通过；这是命名例外，不宣称通过全部官方校验。

mermaid-diagrams、diagram-design、answer-me-with-html 都是可选实现能力，具体选择以 SKILL.md 为准。评测中提供的冻结依赖不代表用户环境已安装这些工具。

## 继续迭代

从 [评测与交接入口](evaluation/README.md) 开始：

- [已确定的目标、取舍和当前状态](evaluation/maintenance/2026-10-14-v2-freeze/HANDOFF.md)
- [测试方法与下一轮准备](evaluation/maintenance/2026-10-14-v2-freeze/TESTING.md)
- [以理解效果为准的评审方法](evaluation/maintenance/2026-10-14-v2-freeze/RUBRIC.md)
- [全部 16 题结果](evaluation/2026-10-14-grok47-failed-retry-2/all-cases.md) · [产出画廊](evaluation/2026-10-14-grok47-failed-retry-2/all-cases.html)
- [冻结快照与校验值](evaluation/maintenance/2026-10-14-v2-freeze/manifest.json)

保留三轮当前版本的原始请求/响应、产物和评审证据。各会话的生成缓存、工具副本和更早实验保留原位置，来源与范围见 [SOURCE.json](evaluation/SOURCE.json)。历史记录中的绝对路径是当时的来源记录；浏览结果使用本目录的相对链接，重跑时创建新轮次。

## 来源

本 skill 基于 [HumanLayer show-me](https://github.com/humanlayer/skills/blob/bba9d13ab34f0a87f1cc33df4dd196372393ddfc/plugins/show-me/skills/show-me/SKILL.md)，保留其 [MIT 许可证](LICENSE.show-me)。
