# 视觉 Skill 评测入口

原始材料已移出当前工作区，完整内容保留在固定提交；保存方式与下载说明见 [评测存储说明](../README.md)。

当前只维护 [visual-explanation 0.5.0](../../skills/visual-explanation/README.md)。2026-10-15 统一采用原 `_2` 正文，调用名为 `$visual-explanation`。

## 当前依据

- [0.4.2 与原 `_2`：去重、复杂总览](2026-10-14-v2-v042/comparison.md)
- [增补三例：趋势、实例、SVG 修改](2026-10-15-v2-expanded/comparison.md)
- [目录合并与验证](2026-10-15-consolidation/README.md)

这些比较覆盖五种任务，使用相同模型、独立会话和同等两轮图片反馈，限制与原始记录见各轮 README。没有将其他模型的结果合并成胜率，也没有证明可选绘图后端的原生接入。

## 历史材料

- [原 0.4.2 目录](https://github.com/zaixi/AI-SDLC/tree/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/history/visual-explanation-0.4.2)
- [原 `_2` 目录、冻结记录和原始评测](https://github.com/zaixi/AI-SDLC/tree/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/history/visual-explanation_2)
- [另一 Agent 的 16 题与补测汇总](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/history/visual-explanation_2/evaluation/2026-10-14-grok47-failed-retry-2/all-cases.md)
- [原 `_2` 的历史交接](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/history/visual-explanation_2/evaluation/maintenance/2026-10-14-v2-freeze/HANDOFF.md)

归档中的名称、本机安装路径、版本描述和脚本绝对路径保留当时记录，不是当前安装指令。合并时归档整体搬迁且文件与符号链接未改写；这份完整归档现保存在固定提交中，其内部相对结构保留。涉及旧仓库位置的链接可按 [合并映射](2026-10-15-consolidation/README.md) 或原提交查看。

## 新一轮验证

1. 以 `skills/visual-explanation/` 的运行文件为唯一当前源，固定版本与哈希。
2. 依据用户当次问题选择案例、模型、比较组和次数；不默认重跑全部历史题库。
3. 在本目录新建有日期的报告；隔离生成输入，原始输出及实际画面保存在仓库外，报告记录可用归档位置。
4. 分别报告理解效果、忠实性、交付与成本，标明未验证部分。不要用入口校验或渲染成功代替质量判断。

仅更新名称和元数据时，先验证正文一致性及安装结构；是否实测生成或客户端调用取决于实际改动和用户授权。
