# 扩展图解比较：更高预算与更多场景

当前状态（2026-10-16，用户确认）：研究记录保留，暂不推进集成、修改正式 skill 或追加测试。恢复研究时先看 [报告中的当前决定](report.md#当前决定2026-10-16用户确认)。

沿用上一轮固定版本的 visual-explanation、Archify、Fireworks 与渲染依赖。OpenCode + deepseek-flash/high，每题每组一次，共 12 次独立会话，不重试，不回传人工评审。题目与评分依据在生成前冻结。

单题预算：1200 秒、96 次模型请求、98304 输出 token（包括 reasoning），单次响应最多 32768。并发 2。上轮分别为 600 秒、48 次、49152 和 16384。

V01 平台总览与故障影响、V02 双站架构沿用上轮；V03 增加简单采购审批，V04 增加数据与决策比较。V04 用于观察适用范围与回退能力：Archify 和 Fireworks 明确不用于统计图，不能把这题单独视作架构绘图能力排名。用户要求 HTML 时也可采用表格等合适表达。

本轮去除生成包内维护 AGENTS.md，以及 visual-explanation 和 mermaid-diagrams 根 README；保留工具的运行脚本、schema、模板及引用。V01 既有内联原文，又实际挂载其引用文件。各组看不到其他组、旧产物、评审标准、全局技能和主会话；仅 visual-explanation 可见它原有的三项可选依赖。预算与隔离同时变化，因此旧轮到新轮不是纯预算消融。

模型只能读文本和操作工具，不能看截图；主 Agent 在生成结束后用浏览器查看输出，不把评语发回模型。评审重视信息准确、理解效率与完整交付；不把轻微几何偏差算成缺陷。一次/格、非盲评，不能推断稳定胜率。

题目见 [cases.json](inputs/cases.json)，标准见 [RUBRIC.md](RUBRIC.md)，固定环境、排除文件与内容哈希见 [protocol.json](protocol.json)，源版本见 [sources.json](sources.json)。完整请求、响应、源码、二进制运行依赖、交付和截图保存在 protocol 的 raw_directory，不进 Git。

## 复跑

使用本轮外部归档目录作为 archive；目标必须不存在：

```bash
python scripts/prepare.py /path/to/this-round-archive /path/to/new-directory
python /path/to/new-directory/scripts/run.py audit
python /path/to/new-directory/scripts/run.py run
python /path/to/new-directory/scripts/metrics.py
python /path/to/new-directory/scripts/render_review.py
```

prepare 验证快照后只复制源码和运行依赖，题目与脚本取本目录，不复制旧输出。宿主依赖沿用上一轮：Linux、bwrap、OpenCode、已有宿主模型中继认证、Node 22、Chromium/Playwright。具体路径在 scripts 中；换机器需调整路径并重新审计。mock audit 不产生真实模型请求。脚本跳过已存在的运行目录，不能用它自动重试未完成题。

结果见 [report.md](report.md)。本轮 12 次已完成并逐份目视评审；原始图及评审截图见外部目录中的 gallery.html。
