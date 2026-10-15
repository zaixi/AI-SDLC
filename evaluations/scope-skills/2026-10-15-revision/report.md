# AGENTS.md 设计范围规则修改与实测

已在 `~/.codex/AGENTS.md` 的 Engineering style 下新增六条 Design scope 规则，其他内容未改。实测显示部分约束生效，但**没有达到稳定限制多做且不漏做的要求**。本轮不据此宣称规则有效，也没有继续叠加未经测试的新规则。

## 改动与对照

新增规则要求 agent 在提出新增能力、配置、接口、抽象、依赖或恢复分支之前，确认其当前必要性；优先用现有测试手段，不为测试增设生产接口；保留必要正确性、安全性和扩展点；不自动创建范围外任务；需求和必要验证覆盖后停止设计。

三组均重新运行，不复用上一轮回答：

1. 原版 AGENTS.md。
2. 修订版 AGENTS.md。
3. 原版 AGENTS.md + 固定版本 boring-engineering 及其四份参考文件。

每组五题、每题一次，共 15 个独立请求。前三题沿用原题；新增 webhook 验签与重放保护、一次性 JSONL 汇总。新题是本轮人工构造的案例，不来自真实仓库，也不是独立评测者提供的隐藏题。

模型 `deepseek-flash`，推理 `high`，每请求最多 32768 completion tokens，流式、并发 2；题目内各组顺序固定随机化。所有输入、规则和评分标准在生成前冻结，无反馈、无重试，15 份均非空且 `finish_reason=stop`。

各组全文以相同 user-message 文件包装注入，没有加载其他宿主指令、工具、其他组答案或评分规则。**这是指令内容对照，不是 Codex 原生执行测试。**

[题目](inputs/cases.json) · [评分标准](RUBRIC.md) · [协议及文件哈希](protocol.json) · [运行脚本](scripts/run.py)

## 逐题评审

每格为“范围克制 / 需求完整”，各 0–4 分；沿用前轮定义。人工非盲评，不合成总分或统计胜率。

| 题目 | 原版 | 修订版 | 原版 + boring-engineering |
|---|---:|---:|---:|
| D01 CSV 导出 | 4 / 4 | 4 / 4 | 4 / 4 |
| D02 账单导入 | 2 / 4 | 3 / 2 | 3 / 3 |
| D03 存储 SDK | 3 / 3 | 3 / 4 | 4 / 4 |
| D04 Webhook | 3 / 4 | 4 / 4 | 3 / 3 |
| D05 一次性日志汇总 | 4 / 4 | 4 / 4 | 4 / 4 |

完整性分数表示本题设计要点的覆盖和可实施性，不是编译、功能或安全验收。没有给表述更短或单独使用函数代替类的方案额外加分。

### 生效的约束

**账单题不再为测试增加 CLI。** 原版新增 `--file PATH` 用于离线验证和人工补救；修订版明确使用内部测试钩子，不新增生产 CLI。修订版仍保留有限重试、事务、唯一索引及并发处理。[原版第 77 行](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D02-original/answer.md:77) · [修订版第 174 行](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D02-revised/answer.md:174)

**Webhook 新题减少了额外分支。** 原版在事件表增加 payload 哈希，并建议同 ID 不同 body 时返回 409 和告警，以“成本极低”为理由；修订版只保留 event ID、处理时间和事务去重，没有增加该分支，仍覆盖原始字节验签、时间窗、并发与中断。[原版第 90 行](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D04-original/answer.md:90) · [修订版回答](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D04-revised/answer.md)

CSV 和一次性日志题中，原版本身也保持了较小范围。三组都没有把它们做成插件系统、通用报表或持续运行服务；不能把这些结果都归功于新增规则。

### 没有生效，以及新增的正确性问题

**重试扩张仍然发生。** 修订版把已知的 503 故障扩展到 500、502、504 和多类网络失败，还加入抖动。原版和叠加 skill 组也扩张了重试范围。新增规则没有稳定阻止“更可靠所以顺手加上”的设计。[修订版第 88 行](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D02-revised/answer.md:88)

**修订版擅自确定金额精度，违反核心需求。** 它使用 `quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` 比较金额，题目没有规定两位小数。这会把不同金额静默归为一致。例如实际运行其表达式，`10.001` 与 `10.004` 均变成 `10.00`，可能跳过本应失败的冲突，因此 D02 完整性为 2 分。[修订版第 111 行](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D02-revised/answer.md:111)

这个反例已用 Python Decimal 最小复现，结果保存在原始目录 `amount-check.json`。不能据此认定是新增规则导致了错误，但足以说明修改后仍未满足要求。

**SDK 题仍增加未要求的 `prefix`。** 原版和修订版都提供 S3 `prefix` 配置，并增加拼接和测试逻辑；叠加 boring-engineering 组没有增加。三组都保留了明确要求的第三方接口、旧入口与多实例能力。[修订版第 89 行](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D03-revised/answer.md:89) · [叠加组回答](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D03-original-plus-boring/answer.md)

SDK 原版验证步骤还存在局部缺口：消费者只执行 `tsc --noEmit`，随即运行 `dist/run.js`，没有生成该消费者运行产物的步骤，因此完整性记 3 分。修订版明确包含构建 fixture 的步骤。[原版第 298 行](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D03-original/answer.md:298)

### 叠加 skill 也不能保证通过

账单题叠加组在说明中声称比较金额和日期，但伪代码对已有 ID 仅检查金额后就跳过；历史迁移检查又在写事务之前，未说明暂停写入或锁内复查，完整性记 3 分。[金额检查](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D02-original-plus-boring/answer.md:72) · [迁移部分](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D02-original-plus-boring/answer.md:131)

Webhook 题叠加组自行决定“订单不存在也视为已处理并返回 200”，而任务要求给已有处理器增加验签与去重，没有授权改变该业务分支。它可能使未更新订单的事件被标记成功，范围与完整性各记 3 分。[原回答第 48 行](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D04-original-plus-boring/answer.md:48)

## 篇幅与调用量

| 组别 | 五题平均字符 | 输入 token 合计 | completion token 合计 |
|---|---:|---:|---:|
| 原版 | 6179 | 4701 | 58233 |
| 修订版 | 5377 | 5781 | 79360 |
| 原版 + boring-engineering | 3923 | 27681 | 34969 |

修订版平均篇幅缩短约 13%，但 completion token 增加；叠加组平均篇幅缩短约 37%，也仍有设计缺陷。篇幅不作为效果结论。

接口报告总量为 210725 tokens，包含推理。沿用前轮限制：供应商细分 usage 存在正文非空而 text_tokens 为 0 的情况，不使用其推理/正文细分作结论，未核对计费。

## 验收结论与当前状态

预期是“没有无依据的新能力，且必要需求完整”。修订版仍在 D02、D03 纳入无依据的分支或配置，D02 还有已复现的核心正确性错误，**本轮验收未通过**。叠加 skill 也没有全部通过。

全局文件目前保留本次已测试修订；没有安装 boring-engineering，也没有在全局文件中添加自动加载它的规则。原版完整备份在原始目录 `snapshots/original/AGENTS.md`，修订版也有快照，可随时逐字核对和恢复。

后续不宜仅继续追加口号。若要提高执行约束，可以把方案中的新增配置、接口和恢复分支列入明确的验收项，并由需求测试检查关键语义；这是一条尚未实测的后续方向，本轮没有实现，也没有将其包装为已解决。

每格只有一次生成，原版重跑结果也与前轮不同，不能推断稳定因果效果。评分为人工非盲评；两个新题也由同一执行者拟定。完整代码、Excel、TypeScript SDK 和 PostgreSQL 处理器未执行；只有金额规范化反例做了最小运行验证。

## 保存位置

本机原始材料：`/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/`，包含原版和修订版快照、skill 快照、15 份输入输出、usage、回答哈希及金额反例。尚未上传公共附件，下方本地链接依赖本机文件。

| 题目 | 原版回答 | 修订版回答 | 叠加组回答 |
|---|---|---|---|
| D01 | [查看](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D01-original/answer.md) | [查看](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D01-revised/answer.md) | [查看](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D01-original-plus-boring/answer.md) |
| D02 | [查看](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D02-original/answer.md) | [查看](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D02-revised/answer.md) | [查看](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D02-original-plus-boring/answer.md) |
| D03 | [查看](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D03-original/answer.md) | [查看](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D03-revised/answer.md) | [查看](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D03-original-plus-boring/answer.md) |
| D04 | [查看](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D04-original/answer.md) | [查看](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D04-revised/answer.md) | [查看](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D04-original-plus-boring/answer.md) |
| D05 | [查看](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D05-original/answer.md) | [查看](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D05-revised/answer.md) | [查看](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision/runs/D05-original-plus-boring/answer.md) |
