# Design scope 单段删除对照

[报告](report.md) · [题目和代码夹具](inputs/cases.json) · [两组规则全文](inputs/rules.json) · [冻结判据](RUBRIC.md) · [检查结果与变更摘要](results.json)

比较当前完整 AGENTS.md（with）与只删除 `### Design scope` 段的版本（without）。逐字核对确认除此之外没有差异。三个新构造的 Python 3.11 可运行夹具，每题每组一次；不是生产仓库任务，也没有重复抽样。

OpenCode 1.14.28 + deepseek-flash/high；每会话 600 秒、48 模型请求、49,152 输出 token，上下文 131,072、单请求输出 16,384，并发 2。条件顺序按题目固定随机化。Linux bwrap 离线命名空间，仅通过 host model relay 访问模型。每组显式读取 `/input/AGENTS.md`，六次均观察到读取；不测试 Codex 原生加载机制。其他宿主规则、Skill、旧答案和独立检查不可见。

原始目录：`/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-ablation-195732`。完整输入输出、请求、usage、隔离审计和 diff 仅在本机，尚未公共归档。规则、生成脚本、题目和独立检查在生成前冻结；没有反馈、选择性重试或输出修复。

## 复跑

```bash
python scripts/prepare.py /tmp/design-scope-ablation-next
cd /tmp/design-scope-ablation-next
python scripts/run.py audit
python scripts/run.py probe --model deepseek-flash
python scripts/run.py run --model deepseek-flash
python scripts/verify.py
```

目标目录须不存在。prepare.py 从 rules.json 恢复规则快照，不依赖本机旧文件；run.py 拒绝覆盖已有会话，verify.py 跳过已记录项。Linux 需要 bwrap、Python、OpenCode；脚本中的 OpenCode 路径及 llmproxy provider 使用本机配置，换机器需私下适配，不要输出凭据。模型别名可能变化，不保证逐字复现。

独立检查与仓库测试在只读产出挂载、离线沙箱内执行。测试未反馈给被测 agent；没有修改生成产物。完整计量包含推理和压缩，输入累计含重复上下文，没有换算费用。

本轮未修改全局 AGENTS.md，没有提交或 push。后续若继续评估，保留这轮作为回归证据；新一轮应明确选择真实任务、其他模型或重复采样，而不是把每个观察都追加为规则。
