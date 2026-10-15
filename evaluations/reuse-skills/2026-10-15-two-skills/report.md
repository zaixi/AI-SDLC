# search-first 与 Ai-Eastern reuse-before-build：三题实测

本轮没有稳定的质量胜者。Ai-Eastern 在本地任务上较能及时停止搜索，总成本较低；search-first 搜索更广，但外部选型触发子 agent 后发生重复复核与上下文压缩。两组外部推荐都有接入缺陷，不能把调研深度等同于交付可靠性。

OpenCode 1.14.28 + deepseek-flash，high，每题每组一次，共六次；没有无 Skill 组、没有重跑。所有会话正常结束。方法与限制见 [README](README.md)；[原始对照页](/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-two-skills-170821/gallery.html)。

## 逐题结果

| Case | search-first | Ai-Eastern reuse-before-build | 判断 |
|---|---|---|---|
| R01 仓库已有 CSV 实现 | 25.30 秒 / 2,973 输出 token；复用 encode_rows，行为检查通过；临时验证，未保存新增测试 | 26.82 秒 / 3,119 输出 token；复用同一函数，行为检查通过；在现有测试文件补五项覆盖 | 功能相当；Ai-Eastern 留下可重复的回归测试。search-first 做了无必要的 pip/gh/skill 目录预检 |
| R02 标准库目录打包 | 47.92 秒 / 7,336 输出 token；行为检查通过；仍搜索 PyPI/GitHub；额外增加压缩等级选项，保存验证脚本 | 40.94 秒 / 5,556 输出 token；行为检查通过；直接用标准库；但报告虚构 offline/no-deps 约束 | 实现均满足题目；Ai-Eastern 搜索较节制，但理由不准确；search-first 的研究与扩展偏多 |
| R03 文档链接检查选型 | 329.47 秒 / 32,166 输出 token；推荐 lychee；调用研究子 agent，主 agent 再查竞品；没有排除本地 file 链接，但缓存 key 不利于同一提交长期重复运行 | 200.48 秒 / 20,954 输出 token；推荐 lychee；固定版本读取源码/测试/许可证；使用每次运行的新缓存 key，但示例把 file 链接整体排除 | search-first 保留了主要检查范围，Ai-Eastern 有更严重的需求冲突；两份示例均需修正，未实际运行 CI |

## 关键证据

### R01：复用能力没有拉开差距

两组均使用现有 inventory/tabular.py 的 encode_rows，而非重新手写 CSV。评审器检查了空输入、生成器、字段/行顺序、Unicode、逗号、引号、嵌入换行与原有测试，全部通过。Ai-Eastern 在原文件添加五个测试；search-first 通过一次性脚本验证，原测试仍为一个。

- [search-first 实现](/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-two-skills-170821/runs/R01-search-first/work/inventory/export.py)
- [Ai-Eastern 实现](/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-two-skills-170821/runs/R01-reuse-before-build/work/inventory/export.py)
- [独立行为检查](behavior-checks.json)

### R02：停止搜索与事实准确性分别评分

search-first 在可用标准库足以满足任务时，仍查 PyPI 与 GitHub 小工具；没有安装第三方依赖，但加入了题目未要求的压缩等级选项。Ai-Eastern 没有外部搜索，却在最终记录中写下 `local constraints (offline, no deps) rule them out`。本轮已开放网络，题目仅说明没有已安装依赖，没有禁止新增依赖；这个推断没有依据。选对了标准库不能抵消理由中的错误。

两组独立检查均覆盖目录递归、相对 ZIP 路径、Unicode、文件和目录符号链接、输出在源目录内，以及覆盖已有输出。

- [search-first 输出](/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-two-skills-170821/runs/R02-search-first/final.md)
- [Ai-Eastern 输出](/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-two-skills-170821/runs/R02-reuse-before-build/final.md)

### R03：最终配置比研究篇幅更重要

Ai-Eastern 的推荐文件第 6 节在 `.lycheeignore` 中加入 `^file:`。本地相对链接会解析为 file URI，且同版本过滤器对 URI 应用排除正则，因此这条配置会跳过本题明确要求的相对文件链接。结论来自静态源码和上游测试核对，不声称运行过 lychee 或 GitHub Actions。

证据：[同版本 URI 排除实现](https://github.com/lycheeverse/lychee/blob/lychee-v0.24.2/lychee-lib/src/filter/mod.rs)、[本地路径解析与忽略规则测试](https://github.com/lycheeverse/lychee/blob/lychee-v0.24.2/lychee-bin/tests/cli.rs)、[原始推荐](/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-two-skills-170821/runs/R03-reuse-before-build/work/recommendation.md)。其正文虽写 v2.9.0，workflow 使用的是移动标签 @v2，固定版本证据与实际接入也不完全一致。

search-first 的示例没有 `^file:`，保留本地链接检查。但 cache key 使用 github.sha，同一提交的周期运行无法覆盖已有不可变缓存，过期结果会反复恢复，更新后的缓存无法写回该 key。它能在新提交上建立缓存，并非完全没有缓存功能。Ai-Eastern 使用 github.run_id + restore-keys，对此处理更好。证据：[actions/cache v4 官方更新缓存说明](https://github.com/actions/cache/blob/v4/tips-and-workarounds.md#update-a-cache)、[search-first 原始推荐](/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-two-skills-170821/runs/R03-search-first/work/recommendation.md)。

两份推荐文件分别 12,245 与 11,889 字符（含代码与链接），均明显超过“最小接入示例”所需的篇幅。search-first 展开七个候选并重复说明选型；Ai-Eastern 详细列举源码、决策收据与未核实项。未运行实际 CI，因此没有把任一份标为端到端验证通过。

## 成本

| 合计（三题） | search-first | Ai-Eastern |
|---|---:|---:|
| 墙钟秒数（逐题相加） | 402.69 | 268.24 |
| 实际模型请求 | 40 | 35 |
| 服务报告输出 token | 42,475 | 29,629 |
| 累计输入 token | 1,399,688 | 760,375 |

search-first 本轮总耗时约为 Ai-Eastern 的 1.50 倍，输出 token 约 1.43 倍。联网延迟不受控，且每题一次，不能视为稳定性能倍数。累计输入包含重复上下文，不能当作唯一信息量或实际账单；未估算费用。

R03 search-first 的子 agent、主 agent、上下文压缩请求均计入成本，观察到的模型都为 deepseek-flash，reasoning_effort 均为 high。该题接近 32,768 输出 token 会话上限，但正常交付，没有触发预算终止；未静默换模型。工具与原始指标见 [metrics.json](metrics.json)。

## 对选择的影响

- 如果优先日常开发与成本控制，Ai-Eastern 仍是更值得继续观察的候选：本地优先与停止规则在这两道实现题中体现出来。但不能因为有证据规则，就默认最终设计可靠。
- search-first 的宽搜索和委派确实执行了；这次没有转化成压倒性的质量优势，还出现标准库题过度搜索、研究后重复复核。
- 当前不建议叠加两套完整流程，也没有证据支持直接宣布任何一个“更强”。下一轮若继续，应优先验证发现未知工具的收益与最终接入正确性，而不是继续增加基础检查清单。

这里只测了一个模型、三个不同任务各一次、显式加载，且无无-Skill 对照。结果只能描述本轮行为，不能证明相对无 Skill 的提升，也不能区分每个缺陷究竟来自模型、提示词还是两者交互。
