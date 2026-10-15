# 设计范围规则：实际实现对照

[报告](report.md) · [原题与代码夹具](inputs/cases.json) · [两组规则全文](inputs/rules.json) · [预先冻结的判据](RUBRIC.md) · [独立检查](inputs/checks.py)

两题、两组、每格一次。OpenCode 1.14.28 + deepseek-flash/high；每会话 600 秒、48 模型请求、49,152 输出 token，上下文 131,072、单请求输出 16,384，并发 2。题目改编自前轮 D02/D05，是人工可运行夹具，不是未见真实业务仓库。

原始目录：`/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-execution-194317`。包含快照、请求/usage、事件、完整产出与 diff，目前仅本机可用。仓库保留可复跑的输入和脚本，不含原始请求上下文。

Linux bwrap 隔离 HOME/work/input，网络命名空间离线，仅经 Unix socket host relay 调模型。每组显式读取 `/input/AGENTS.md`，不是 Codex 原生指令加载。无其他宿主 Skill、规则、旧答案或验收测试。账户配置由 host 私下从 OpenCode provider 获取，不暴露给被测 agent。provider 和 OpenCode 路径仍采用本机配置，跨机器须适配 scripts/relay_base.py，勿打印凭据。

## 复跑

先准备一个不存在的仓库外目录：

```bash
python scripts/prepare.py /tmp/scope-execution-next
cd /tmp/scope-execution-next
python scripts/run.py audit
python scripts/run.py probe --model deepseek-flash
python scripts/run.py run --model deepseek-flash
python scripts/verify.py
```

prepare.py 从 Git 中的 rules.json 恢复两组规则，不依赖本机旧快照。已有运行不覆盖、不自动重试；verify.py 只验证尚未记录的完成项。要重做验证，应使用新的评测目录，保留旧结果。

`diagnose.py` 是阅读本轮代码后新增的定向反例，需单独运行 `python scripts/diagnose.py`，不属于生成前冻结的验收集。若下一轮把这些反例纳入正式验收，应在生成前明确记录；它们仍是回归题，不是隐藏新题。

独立检查在离线、只读产出挂载中运行。验收运行不修复产出，也没有把失败反馈给模型。汇总按实际 provider usage，包含推理与压缩；输入含重复上下文，未折算计费。计量和所有检查输出见 results.json，后验反例见 diagnostics.json。

本轮没有修改全局 AGENTS.md、安装新 Skill 或提交/push。下一步保留当前规则使用，若评估专门 Skill，应补充明确要求扩展接口的实现题，检验是否因追求简单而漏做。
