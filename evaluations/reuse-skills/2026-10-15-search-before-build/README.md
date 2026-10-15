# search-first 与 search-before-build

本轮重新运行原版与修改版，五题每组一次，共十次。模型为 OpenCode 1.14.28 + deepseek-flash/high。旧轮结果不混入本轮统计，无无-Skill基线。审阅不是盲评。

题目沿用前两轮：R01 复用 CSV、R02 标准库打包、R03 文档链接选型、A01 评测执行器、A02 附件发布。完整输入见 inputs/cases.json，运行前判据见 RUBRIC.md。两组均显式读取当前包 SKILL.md；原版使用前轮冻结的 ECC search-first，修改版使用本轮修订后的仓库文件。完整快照和哈希在原始目录与 protocol.json。

每会话上限 600 秒、48 次模型请求、49,152 输出 token，单请求 16,384，context 131,072，并发 2。这轮 R01–R03 的预算比旧轮宽，两组预算相同。使用 bwrap 隔离 HOME/work/input，主机仓库、其他已装 Skill、旧答案、评审标准不可见；公网对两组开放，外部内容与网络延迟不可控。没有提供完整 ECC 的专用 researcher/planner/architect，普通 task 子 agent 可用；这评估的是 Skill 单独使用的表现。

原始目录：`/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-search-before-build-182253`。包含输出、请求/usage、事件、快照与隔离审计。此目录仅本机可用，尚未公共归档。gallery.html 将输出转义为文本展示，不执行模型生成内容。

生成脚本沿用上一轮，仅换条件与运行顺序种子。R01/R02 使用旧轮独立行为检查，在只读挂载产出的离线沙箱执行。设计题只静态核对，不安装候选或发布材料。服务 usage 含子 agent 和压缩；输入累计含重复上下文。标题请求本地模拟，不计实际模型请求。工具失败也计入工具调用数。

复跑须使用新的仓库外目录，复制 scripts/inputs，恢复 snapshots/search-first 与 snapshots/search-before-build 并校验哈希。Linux 需要 bwrap、Python、Node 及同版本 OpenCode。relay_base.py 的 BINARY 与 provider() 使用本机 OpenCode llmproxy 配置，跨机器须私下适配，不能打印凭据。依次运行：

```bash
python scripts/run.py audit
python scripts/run.py probe --model deepseek-flash
python scripts/run.py run --model deepseek-flash
python scripts/summarize.py
python scripts/verify.py
python scripts/gallery.py
```

已有运行目录不会被覆盖或自动重试。protocol.json 保留生成前哈希；后处理适配与最终脚本哈希单独记录。模型别名和公开网络内容可能变化，不承诺逐字复现。
