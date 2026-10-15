# 统一视觉 Skill：0.5.0

用户授权以原 `visual-explanation_2` 替换 0.4.2，合并为一个正式目录，便于后续使用与验证。

| 原位置 | 当前用途与位置 |
|---|---|
| `skills/visual-explanation/`（0.4.2） | 完整归档到 [history/visual-explanation-0.4.2](https://github.com/zaixi/AI-SDLC/tree/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/history/visual-explanation-0.4.2) |
| `skills/visual-explanation_2/` | 完整归档到 [history/visual-explanation_2](https://github.com/zaixi/AI-SDLC/tree/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/history/visual-explanation_2)，含原评测、依赖、快照与交接 |
| 原 `_2` 的运行文件 | 统一为 [skills/visual-explanation](../../../skills/visual-explanation/)，版本 0.5.0 |

正式名称与调用提示均为 `visual-explanation`。主文件只改 frontmatter 名称、许可证与版本元数据，图解正文与原 `_2` 逐字一致；许可证原样保留。未新增绘图规则、未安装后端、未修改用户机器上的安装。

两个旧目录的文件字节和符号链接目标按 [archive-manifest.json](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-15-consolidation/archive-manifest.json) 核对，原始评测没有重写。归档整体搬迁，保持内部相对目录结构；历史主文件只存在于评测区，不再位于可安装 Skill 目录。

迁移前完整仓库状态固定于 [3fa6b40](https://github.com/zaixi/AI-SDLC/tree/3fa6b407ad4a628b76bc92835cb8ef02add9635c)。旧文档中依赖原路径的链接，可在该提交下查看。归档中的历史目录名和旧本机路径不代表当前安装。

验证结果见 [validation.json](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-15-consolidation/validation.json)。本次验证唯一活动入口、YAML 与调用提示、正文一致性、完整归档和当前文档链接；未重新采样模型答案，也没有执行客户端原生发现测试。既有五类任务比较仍是正文行为证据，不能冒充本次新名称调用结果。
