# 三个复用/选型 Skill：真实架构问题

结果见 [report.md](report.md)，运行前的判据见 [RUBRIC.md](RUBRIC.md)。每题每组一次，无重跑、无无-Skill基线。不是实现/部署验收。

## 输入与环境

- A01：用本仓库真实执行脚本，决定后续评测执行器应采用现成框架、组合接入，还是整理现有实现。代码仅替换主机用户名与实验条件名称；补充已有批次与视觉反馈的事实背景。
- A02：根据真实存储政策、清理历史与本地未发布产物，设计按单轮下载、来源/哈希核对和复现路径。删除报告索引链接，避免主动提供旧评测结论。
- 完整题目和 supplied 文件保存在 [inputs/cases.json](inputs/cases.json)，来源与变换哈希见 [inputs/provenance.json](inputs/provenance.json)。判据在生成前固定，未提供给被测模型。
- OpenCode 1.14.28 + deepseek-flash，high；上下文 131,072；单请求输出上限 16,384；每会话 600 秒、48 次实际模型请求、49,152 输出 token。并发 2，固定种子打乱每题条件顺序。
- 每次独立 bubblewrap HOME/work/input；只提供当前 Skill 包、该题材料与相同工具。主机仓库、AGENTS、其他已装 Skill、其他组输出与评审文件不可见。API 凭据仅由主机 relay 使用。所有组开放公网，网络不是隔离边界；可读取公开仓库与网页，不能宣称完全无外部信息污染。
- 实际工具：bash/read/glob/grep/edit/write/task/webfetch，无原生搜索工具。Skill 要求的子 agent 可通过 task 使用，调用成本计入；并非关闭子 agent 的简化测试。
- 三组均显式读取 SKILL.md，提供该包内 references/assets；未安装其提到的其他工作流 Skill。本轮不进入实现阶段，也不测试自动触发。

## 版本与成本

[sources.json](sources.json) 记录每个 Skill 文件的 URL、哈希与大小。前两组复用上一轮冻结内容，URL 是移动分支，哈希才是本轮内容身份；citypaul 固定 commit。完整快照在本地原始目录，未复制进报告仓库。

[metrics.json](metrics.json) 的输出 token 和累计输入 token 来自服务端 usage，包含子 agent 与上下文压缩；输入累计包含反复发送的上下文，不能当作唯一信息量或直接当账单。`request_count` 包含本地模拟的标题请求及被预算拒绝的请求；`model_requests` 才是实际转发数量。工具统计包含失败工具返回，不代表全部成功。exit=0 或有文字不等于完成，以 design.md 与内容审阅为准。

耗时含公开网页请求、失败重试和模型响应，不能从单次墙钟差异推出稳定速度。未记录到模型上游错误文件；外部网站的失败/限流仍发生。所有 supplied 文件逐字比对未被修改。只做静态设计核对，没有安装候选、上传材料或执行方案中的发布命令。

## 原始材料与复跑

本轮完整原始目录：`/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-real-architecture-173335`。含六组 work、最终设计、事件、请求/usage、隔离审计、完整 Skill 快照与 [对照页](/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-real-architecture-173335/gallery.html)。这是本机持久目录，尚未公共归档；外部读者不能通过本地链接下载。

保留脚本为实际运行副本。复跑应创建新的仓库外目录，复制 scripts、inputs，并恢复 snapshots/<condition>/；按 sources.json 校验每个文件，移动 URL 内容不匹配时不能冒充原版。需要 Linux、bwrap、Python、Node 与同版本 OpenCode。relay_base.py 的 BINARY 和 provider() 依赖本机 OpenCode 的 llmproxy 配置，须在目标机器私下适配，禁止输出凭据。随后依次运行：

```bash
python scripts/run.py audit
python scripts/run.py probe --model deepseek-flash
python scripts/run.py run --model deepseek-flash
python scripts/summarize.py
python scripts/gallery.py
```

不要在当前正式目录复跑；执行器会跳过已存在目录，不会自动修复失败题。模型别名与公网内容可能变化，因此不能保证逐字复现。

protocol.json 保留运行前 frozen_hashes，并单列最终脚本哈希。运行后只完善 summarize/gallery 的指标与显示；生成脚本、题目、判据没有后改。仓库中的 RUBRIC.md 对应原始 review/rubric.md。
