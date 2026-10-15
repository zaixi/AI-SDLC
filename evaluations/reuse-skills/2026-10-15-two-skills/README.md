# 复用 Skill：search-first 与 reuse-before-build

- [比较报告](report.md)
- [题目与起始文件](inputs/cases.json)
- [运行前固定的评审标准](RUBRIC.md)
- [协议](protocol.json)、[来源与内容哈希](sources.json)、[指标](metrics.json)、[独立行为检查](behavior-checks.json)

原始目录：`/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-two-skills-170821`。含完整生成日志、冻结的运行 Skill 文件与 references、工作区产物和 gallery.html；未发布公共附件。

## 复现

Linux、Python 3、bubblewrap、OpenCode 1.14.28。模型 deepseek-flash，reasoning_effort=high；复用宿主现有 llmproxy provider，凭据仅由宿主 relay 使用，不能提交或挂给模型。运行前核对 scripts/relay_base.py 中 BINARY 路径与 provider 配置方式。

新建仓库外实验目录，复制 scripts/ 与 inputs/，建立 review/，把 RUBRIC.md 复制成 review/rubric.md。从本轮原始目录复制 snapshots/；如重新下载 sources.json 的 URL，必须核对每个 SHA-256，main 变化时不能宣称复现了本轮。这里固定了文件内容，未声称固定 Git commit。

```sh
python3 scripts/run.py audit --model deepseek-flash
python3 scripts/run.py probe --model deepseek-flash
# 查看 audit 和 probe 结果，确认工具、隔离与连通后执行
python3 scripts/run.py run --model deepseek-flash
python3 scripts/verify.py
python3 scripts/summarize.py
python3 scripts/gallery.py
```

每题每组一次，3 题 × 2 组；串行运行防止共享网络下 relay 端口冲突。每个会话独立文件系统、HOME、输入与工作区，公共网络启用；不提供宿主 AGENTS、其他已装 Skill、对照输出或评分标准。两组都有 task/webfetch，原生 websearch 未暴露；网络检索通过网页/命令执行。标题请求由本地 mock 回答，不算模型调用。子 agent 与上下文压缩包含在同一会话预算和指标内。

预算：420 秒、32 次模型请求、32768 输出 token，每请求最多 16384。调研题只做文档/源码检查，不安装运行第三方工具。生成没有重跑；验证器在首次执行时补齐了系统 Python 符号链接所需的 /etc/alternatives 挂载，再检查原封不动的生成文件，未给模型反馈或修补答案。

只测显式调用后的表现，不测自动触发。无无-Skill 对照、每题一次、非盲评、联网内容可能变化，不能推出稳定胜率或因果增益。
