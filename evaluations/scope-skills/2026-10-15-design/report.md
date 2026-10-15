# 三个 Skill、现有 AGENTS.md 与无约束基线的设计对照

这轮测试中，`boring-engineering` 和 `karpathy-guidelines` 都减少了无 skill 基线里的预留扩展设计，并保留了明确要求的可靠性和第三方扩展能力。两者没有足够证据分出稳定优劣。微软 `yagni` 也约束了功能范围，但它引用的工作流程带入了 backlog、任务分片和额外确认，不适合原样作为这个仓库的轻量通用约束。

随后加入现有 `~/.codex/AGENTS.md`：CSV 题保持了较小范围，账单题和 SDK 题仍增加了未要求的参数或能力。本次补测没有显示它能完全替代两个推荐 skill，也不能据单次样本判断它普遍更差。

这是 **deepseek-flash 上的 3 道设计题 × 5 组、每题每组一次，共 15 份方案**。前四组是原批次，AGENTS.md 是后续补测；不是多模型结论，也没有验证完整实现或长期维护成本。

## 测试方式

- 对照组：无约束基线、boring-engineering、karpathy-guidelines、microsoft/agentic-loops 的 yagni、现有全局 AGENTS.md。
- 三题：内部工具 CSV 导出；每日账单导入的原子性与重跑；明确要求第三方后端的存储 SDK。
- 题目、评分规则在生成前固定；无反馈修订。每个请求使用相同的中性系统消息，只提供本题和本组 skill。
- 模型为 `deepseek-flash`，`reasoning_effort=high`，每次最多 32768 completion tokens，流式调用，两个并发请求。未设置 temperature 或 seed，使用服务端默认值。
- 全文注入各组文件，无工具、无其他组答案。除第五组显式提供的 AGENTS.md 外，不加载宿主全局规则。测试的是指令内容，不是客户端自动触发 skill 或原生加载 AGENTS.md 的能力。
- 主执行者依据[预先固定的评分规则](RUBRIC.md)人工评审；非独立盲评。

[完整题目](inputs/cases.json) · [协议、固定提交与 SHA-256](protocol.json) · [脚本](scripts/run.py) · [复测说明](README.md)

第五组使用[补测协议](global-agents/protocol.json)与[补测脚本](scripts/run_agents.py)，保留原题、原评分、原模型参数。AGENTS.md 全文快照的 SHA-256 为 `c7b15c9b8a6f76e04ad8ce9b8a85c0df15c3ac33b0af6de2947e3680606ad9e6`。为保持注入条件可比，仍使用前四组相同的 user-message 文件包装；没有将其提升为 system 消息，也没有叠加任何被测 skill。

## 逐题结果

每格为“范围克制 / 需求完整”，各 0–4 分。明确排除的能力不扣分；必要的事务、接口和验证不会因为增加代码而扣分。分数用于说明本次判断，不表示统计显著性。

| 题目 | 无 skill | boring-engineering | karpathy-guidelines | yagni | 现有 AGENTS.md |
|---|---:|---:|---:|---:|---:|
| D01 CSV 导出 | 2 / 4 | 4 / 4 | 4 / 4 | 3 / 4 | 4 / 4 |
| D02 账单导入 | 3 / 4 | 4 / 4 | 4 / 4 | 4 / 3 | 2 / 3 |
| D03 存储 SDK | 2 / 4 | 4 / 4 | 4 / 4 | 3 / 4 | 3 / 4 |

“需求完整 4 分”表示本题的必要设计要点得到处理，不等于方案所有技术细节都已经实现或验证正确。

### D01：未来需求会不会进入本次设计

无 skill 基线没有引入队列或报表框架，但新增了通用 CSV 模块、独立业务映射层及格式化函数注入，并明确用未来 XLSX、邮件作为拆分理由：

> 这样以后要 XLSX 或邮件附件，可以复用 `buildOrderExportRows`，不用重写字段映射。

它还建议在仓库层没有上限时给导出增加 5000 条硬限制。题目给的是当前数据规模，并没有要求新增截断规则。前瞻分层与额外限制共同构成范围扣分。[原回答](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-design-formal/runs/D01-none/answer.md)

`boring-engineering` 使用现有路由、查询和模块内 CSV 函数；`karpathy-guidelines` 把 CSV 逻辑放入一个小模块。后者的独立模块便于测试，不因单独建文件就判为过度抽象。两组都保留了权限、筛选、转义、公式防护及 Excel 验证。[boring-engineering 回答](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-design-formal/runs/D01-boring-engineering/answer.md) · [karpathy-guidelines 回答](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-design-formal/runs/D01-karpathy-guidelines/answer.md)

`yagni` 的功能方案也较小，但新增了明确的执行任务：

> T7：把 XLSX 等三项记入 `docs/backlog.md`。

用户只让设计当前 CSV 功能，没有要求维护 backlog。这是流程上的多做；不是把“列出不做事项”本身当作问题。[原回答第 120 行](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-design-formal/runs/D01-yagni/answer.md:120)

### D02：简化会不会删掉必要的可靠性

四组都保留了有限重试、事务、唯一约束、重跑去重和金额冲突失败。没有一组用“保持简单”作为逐行提交或静默忽略冲突的理由。

`boring-engineering` 用 SQLite `BEGIN IMMEDIATE` 和有限锁等待处理并发，不再加独立文件锁；迁移先停 cron，在事务内检查冲突、备份、去重并建索引。这是减少组件同时保留必要保障的具体例子。[原回答](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-design-formal/runs/D02-boring-engineering/answer.md)

`karpathy-guidelines` 使用文件锁和 TEMP staging 表。staging 表承担批量冲突检查，属于合理替代方案，不仅因为比逐行查询多一张临时表就扣分。回答比基线长，但未发现明显的范围扩张。[原回答](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-design-formal/runs/D02-karpathy-guidelines/answer.md)

无 skill 基线建议增加七项配置，涵盖路径、日期、重试次数、退避和超时。部分参数有现实用途，但把这些全部列为配置，超出了本题固定单机任务所证明的需要，因此记一项轻微多做。未把退出码分类或合理的文件锁算作过度设计。[原回答第 60 行](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-design-formal/runs/D02-none/answer.md:60)

`yagni` 的日常导入方案完整，但迁移中的冲突查询发生在写事务之前，且没有说明迁移期间暂停旧导入任务或在锁内重新检查。若旧脚本继续写入，检查结果与后续去重可能不一致。这里需要补充迁移期停写或事务内检查，需求完整扣一分。[原回答迁移部分](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-design-formal/runs/D02-yagni/answer.md:58)

### D03：明确需要扩展能力时，是否仍然愿意设计接口

四组都给出了公开写入接口、显式传入后端的多实例入口、旧 `archive(input, key)` 兼容入口、本地与 S3 实现，以及用独立包和发布 tarball 检查第三方接入的方案。没有一组因“不要抽象”而拒绝合同要求的扩展点。

无 skill 基线另外增加了 S3 `prefix` 选项，并计划将已有本地写入改为“临时文件 + rename”。题目没有要求这两项；本次应保留旧本地行为，因此记为额外设计。[原回答](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-design-formal/runs/D03-none/answer.md)

`boring-engineering` 明确不加 `prefix`、原子写与插件注册机制；`karpathy-guidelines` 保留现有本地实现，把 AWS 配置交给调用方传入的 `S3Client`。两者的必要接口都没有被删掉。[boring-engineering 回答](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-design-formal/runs/D03-boring-engineering/answer.md) · [karpathy-guidelines 回答](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-design-formal/runs/D03-karpathy-guidelines/answer.md)

`boring-engineering` 仍提出了 `publint`、`@arethetypeswrong/cli`、`aws-sdk-client-mock` 等工具。它们与包边界验证相关，本轮不扣范围分，但采纳时仍应检查现有 TypeScript/Vitest 是否已经够用；这个 skill 并不能保证完全不加工具。

`yagni` 保留必要接口，却在末尾要求：

> 请确认是 feature 工作流还是 worktree 工作流，并给出对应的编号或 `<id>`。

题目没有要求选择这种工作流。它还提出多项待人决定的问题，增加了设计交付的协调负担。[原回答第 144 行](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-design-formal/runs/D03-yagni/answer.md:144)

## 现有 AGENTS.md 的补测证据

CSV 题明确要求“行数据映射放在 handler 里即可，不额外抽层”，并将 XLSX 的抽取推迟到真实需求出现时。保留了权限、筛选、转义、公式防护和验证，也没有新增截断规则。因此范围与完整性均为 4 分。[原回答第 61 行](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-global-agents/runs/D01-global-agents/answer.md:61)

账单题保留了单事务、唯一索引、冲突失败及安全迁移的主要流程，但扩张了多项范围：

- 新增 `--date`、`--db`、`--url`、`--input-file`、`--max-retries`。指定重跑日期有现实需要；为了测试新增生产 CLI 路径和多个配置开关则没有由题目证明必要性。[改动清单](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-global-agents/runs/D02-global-agents/answer.md:19)
- 将已知的 503 重试扩大为 429、500、502、504 及多类网络失败，并加入抖动与相应分类。这些策略未必不合理，但本题没有相应故障证据，也允许失败后人工处理。[重试策略](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-global-agents/runs/D02-global-agents/answer.md:145)
- 额外提供 `--resolve-identical-only` 分支，允许保留金额冲突的重复组后继续迁移，却仍要求创建 `billing_id` 唯一索引。保留重复键与该索引不能同时成立，是多出的分支带来的局部设计矛盾，完整性记 3 分。[原回答第 98 行](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-global-agents/runs/D02-global-agents/answer.md:98)

最后一项用内存 SQLite 做了最小核验：插入两条相同 `billing_id`、不同金额的记录后创建唯一索引，得到 `sqlite3.IntegrityError`。结果保存在补测原始目录的 `migration-check.json`。这只验证该矛盾，没有实现或运行整套迁移方案。

SDK 题满足旧 API、多个实例、公开类型和第三方独立接入要求，但新增了 `prefix?: string` 以及前缀拼接和专门测试，与此前对基线的扣分标准一致，范围记 3 分。没有因使用 class、工厂或必要的后端接口而扣分。[原回答第 56 行](/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-global-agents/runs/D03-global-agents/answer.md:56)

这份 AGENTS.md 已含“避免推测性功能、非必要抽象和可配置性”，但本次账单与 SDK 回答没有稳定执行这些边界。单纯在文件里写出原则，并不保证每个设计元素都会经过必要性判断。

## 篇幅和调用量

原批次 12 份和补测 3 份回答全部非空且以 `finish_reason=stop` 结束，没有正式样本失败或截断。

| 组别 | D01 字符 | D02 字符 | D03 字符 | 平均字符 | 三题输入 token | 三题 completion token |
|---|---:|---:|---:|---:|---:|---:|
| 无 skill | 6184 | 3736 | 8580 | 6167 | 929 | 44093 |
| boring-engineering | 3484 | 4223 | 3556 | 3754 | 14696 | 27324 |
| karpathy-guidelines | 3710 | 5479 | 6040 | 5076 | 2768 | 45036 |
| yagni | 3572 | 3301 | 3992 | 3622 | 7322 | 34412 |
| 现有 AGENTS.md | 5052 | 7946 | 6036 | 6345 | 2873 | 38558 |

字符数包含 Markdown 与示意代码。相比基线，平均篇幅分别减少约 39%、18%、41%。但账单题中 boring-engineering 和 karpathy-guidelines 都比基线更长；yagni 平均最短，却带入了额外工作流。不能用篇幅代替范围评审。

AGENTS.md 平均篇幅比基线多约 3%；CSV 和 SDK 更短，账单更长。篇幅变化同样不能代替范围判断。

原批次报告 **176580 tokens**，补测报告 **41431 tokens**，合计 **218011 tokens**，包含推理输出。供应商的细分 usage 有多次 `text_tokens=0` 而回答非空，因此不使用其推理/正文拆分作结论；总量也只是接口报告值，未独立核账。该数字不含失败和预算校准请求，不能视为本轮完整计费量。

## 运行故障与限制

初始非流式请求中，两次在 240 秒后超时，另两次在诊断时中断。简短健康检查成功；随后流式预检正常返回，但 8192 token 在推理阶段耗尽，没有答案。早期流式请求也中断并排除。正式四组统一使用流式和 32768 token 上限，全部重新运行；没有择优替换某一组答案。原始失败和校准记录的目录保存在 protocol.json。

本轮不能证明 skill 的稳定因果效果：每格只有一次生成，模型有随机性；题目已经明确说明规模、已有能力和未排期需求，基线本身也受到这些边界约束。人工评分存在主观判断，尤其是合理拆分与过度分层之间的边界。

第五组是在看过前四组结果之后补测的，沿用原评分规则，未重跑或替换原答案。它与原批次不是同时随机交错运行，服务端模型版本和运行状态的变化无法完全排除。也没有测试“AGENTS.md + 某个 skill”的叠加效果。

参考文件是提前完整注入的。boring-engineering 带五份文件，yagni 带主文件和 meta-design，karpathy-guidelines 只有主文件。这反映所提供资料包的效果，不能分离主文件与参考资料各自的贡献，也不代表按需加载时的 token 成本。yagni 的流程副作用尤其可能来自 meta-design。

没有完整执行这些方案、编译 SDK、验证 Excel 或运行迁移脚本。除补测中针对唯一索引矛盾的最小 SQL 核验外，需求完整性均是设计审阅判断，不是实现验收结论。

## 选用建议

当前可优先试用 boring-engineering 或 karpathy-guidelines。前者在这轮给出的实现路径较直接，后者更关注已有行为兼容；两者都保留了必要复杂度，不需要同时叠加。

如果采用微软 yagni，建议只提取设计和代码范围规则，先排除与本仓库无关的 meta-design 工作流程；这属于后续定制方案，本轮没有测试定制后的效果。

现有 AGENTS.md 可以继续作为基础约束。本次新增对照没有显示它能完全替代 boring-engineering 或 karpathy-guidelines，但也不支持删掉它、或断言叠加 skill 一定更好。若后续改进，应重点约束设计时新增参数、容错分支和便利功能的必要性；修改后的规则尚未测试。

## 证据保存

正式原始请求、回答、usage 与第三方文件快照保存在本机：`/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-design-formal/`。每份回答的 SHA-256 在该目录的 `results.json`；来源文件哈希和固定提交在本仓库 protocol.json。上述回答链接依赖这台机器，尚未上传为公共附件。

仓库只新增本轮报告、方法、题目、协议和脚本。没有安装这些 skill，也没有修改现有全局规则。

AGENTS.md 补测原始资料位于 `/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-global-agents/`，包含全局文件快照、3 份回答、哈希和最小 SQL 核验结果。它们同样尚未上传为公共附件。
