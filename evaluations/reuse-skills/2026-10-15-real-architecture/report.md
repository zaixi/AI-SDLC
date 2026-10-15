# 三个 Skill 的真实架构题实测

这轮没有稳定的质量胜者。citypaul 的 evaluate-existing-solutions 最擅长组织决策，Ai-Eastern 的 reuse-before-build 核查实现更深入；search-first 在一题中最快交付，在另一题中耗尽预算却没交付。三者都出现了“调研很多、关键判断仍不准确”的问题。

两道题来自当前仓库：评测执行器如何复用现成框架，以及原始评测材料如何存储与发布。OpenCode 1.14.28 + deepseek-flash/high，每题每组一次，共六次。相同隔离和预算，无重跑、无无-Skill组；方法见 [README](README.md)，[原始输出对照页](/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-real-architecture-173335/gallery.html)。

## 结果与成本

| Case | search-first | Ai-Eastern reuse-before-build | citypaul evaluate-existing-solutions |
|---|---|---|---|
| A01 评测执行器 | **未完成**；48 次请求耗尽，没有 design.md；265 秒 / 47,740 输出 token | 完成；保留内核、配置化、借鉴 Inspect；485 秒 / 27,776 token | 完成；保留内核、配置化，以小型验证决定是否迁移 Inspect；185 秒 / 24,470 token |
| A02 附件存储与发布 | 完成；Releases + 清单，可选 Zenodo；136 秒 / 18,084 token | 完成；同一主方案，增加证明与详细发布流程；166 秒 / 23,736 token | 完成；同一主方案，扩展现有清单，明确触发条件；340 秒 / 22,400 token |
| 两题输出 token 合计 | 65,824 | 51,512 | 46,870 |
| 实际模型请求合计 | 59 | 45 | 36 |
| 累计输入 token | 2,928,080 | 2,532,380 | 1,487,474 |
| 已完成设计的字符数 | A02：13,866 | A01：19,069；A02：17,973 | A01：17,786；A02：16,060 |

上述 token 包含研究子 agent 和压缩，不只是交付正文。search-first A01 调用 3 个 task，wire 中可识别的工具返回包括 86 次 webfetch、40 次 bash，耗尽 48 次模型请求预算。它留下了研究过程，但不能把过程当成完成方案。没有因这个失败追加预算或重测。

## A01：保留现有内核合理，但排除外部方案的证据不足

Ai-Eastern 和 citypaul 都抓住了真正痛点：当前运行内核已可用，重复脚本与实验配置混杂才是维护负担。两者均建议一个版本化内核加声明式 profile，保留沙箱、主机 relay、原始记录和任务阶段，避免直接重写成服务平台。citypaul 对迁移验证、职责、回退与重新评估条件组织得更清楚；Ai-Eastern 读了 Inspect 固定版本源码，识别出桥接过程可能变换请求字段，提出保留原始 wire 记录，证据更具体。

但两者都有关键缺口：

- **过早排除 promptfoo。** 两份设计都以它偏 prompt/provider 为由，认为不能驱动真实 agent 进程，未评估保留现有沙箱、外加执行适配器的组合路径。官方 [Custom Scripts 文档](https://www.promptfoo.dev/docs/providers/custom-script/) 明确允许外部可执行命令作为 provider。这不证明 promptfoo 值得采用，却说明“不能接真实 CLI”不是充分的排除理由。
- **把未知条件推成限制。** Docker 未被题目禁止、也没有证实运行环境可用；应将它作为待验证成本，而非据此默认排除方案。当前 bwrap 实现需要保持的，是隔离性质及可审计性，不必天然要求所有实现细节不变。
- **把历史能力与当前代码混在一起。** Ai-Eastern 明称 R1–R6 均已实际实现，其中包括两轮图片反馈；本题 supplied 脚本并未提供该完整循环，run.py 还覆盖了 relay_base 中旧的 setup/command。citypaul 后文承认反馈实现仍需核实，但前文对现状的断言也偏满。不能只凭文件中存在旧视觉分支就判定当前路径已实现。

因此本题可说 citypaul 的决策结构较好、Ai-Eastern 的实现核查较深，不能说任何一份设计已完成充分选型。Inspect 确有 [sandbox agent bridge](https://inspect.aisi.org.uk/agent-bridge.html)，是否值得迁移仍需比较适配代码与维护责任，而非只列功能表。

原始设计：[Ai-Eastern](/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-real-architecture-173335/runs/A01-reuse-before-build/work/design.md)、[citypaul](/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-real-architecture-173335/runs/A01-evaluate-existing-solutions/work/design.md)。

## A02：选型趋同，迁移细节拉开差异

三者都选了合理的起点：Git 保留轻量方法与清单，Releases 承载单轮附件，Zenodo 仅在 DOI/独立归档需求出现时加入。均区分当前树与历史对象，保留固定提交链接，提出发布前脱敏，没有实际上传或改写历史。GitHub 的 [Releases 文档](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) 与 [不可变发布文档](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases) 支持这条基本路线。

**search-first 的迁移重点最贴近当前缺口。** 它优先选最近一轮尚未公开的批次试点，历史镜像作为可选项。这比先补旧归档更直接。但它展开十类候选、提出多个脚本，篇幅仍偏大；还声称 Release 无内建每文件校验和。当前 [Release assets API](https://docs.github.com/en/rest/releases/assets) 已给出 digest 字段。独立清单依然有价值，理由应是审计、映射和持久记录，而不是平台没有摘要。

**Ai-Eastern 的发布核验细节最多，但步骤有断点。** 它明确 draft → 附件 → publish，并给出 release verify/verify-asset；消费者命令却只下载 ZIP，紧接着执行 `sha256sum -c SHA256SUMS`，没有下载该文件或先解包。数据分类表还将“不要提交完整上下文”推成“不发布（或择要）”，与提供已脱敏原始材料的目标发生偏移，且与前一行发布原始 JSON 的说明不一致。另一个迁移假设是更早的 20-session 批次就在固定历史提交里，题目并未证明这一点。

**citypaul 的决策文档最完整，但不代表迁移更准确。** 它将预算未知标为“零预算”的暂定硬约束；历史迁移把整个 evaluations/ 打成一个包，却称新链接为“单次包”，仍未实现按单轮取得旧材料。同时重点放在历史回填与下一轮，对当前尚未共享的本机结果没有明确处理步骤。对受限材料的存储建议也仍需单独核查服务政策，不能把访问控制等同于允许上传任何敏感内容。

这道题若按“最小方案、先解决当前问题”评，search-first 的完成稿略好；若按来源记录与发布细节评，另外两组各有长处。三份都需要修正后再实施。

原始设计：[search-first](/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-real-architecture-173335/runs/A02-search-first/work/design.md)、[Ai-Eastern](/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-real-architecture-173335/runs/A02-reuse-before-build/work/design.md)、[citypaul](/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-real-architecture-173335/runs/A02-evaluate-existing-solutions/work/design.md)。

## 对 Skill 选择的影响

- **技术选型/架构设计框架：仍倾向 citypaul，但只限结构优势。** 它较自然地组织目标、取舍、反对理由、验证与切换条件，两题均交付且模型用量最低。不过这轮没有证明最终设计质量全面优于 Ai-Eastern；硬约束与迁移细节仍需人工审阅。
- **日常开发中的复用判断：Ai-Eastern 仍值得保留。** 本地优先与明确借用范围有用，源码核查也确实发现具体风险。但核验回执和来源检查容易占据大量输出，不能自动保证需求理解正确。
- **search-first 更适合开放探索，当前不优先作为受限预算下的默认架构流程。** 一题快速交付说明它不是总慢；另一题的多 agent 研究失去收束，实际交付可靠性是本轮最大的短板。

本轮五份完成稿均达约 1.4–1.9 万字符，反复列需求、回执、摘要和候选。对用户“信息密度高、少套话”的偏好，三个原版都不理想。暂不建议叠加三套流程。

这只是单模型、两题各一次的非盲定性评审，没有无-Skill组，不能推导 Skill 相对模型裸跑的增益，或稳定胜率。Ai-Eastern A01 下载源码包的失败等待、citypaul A02 的外网页面请求也影响耗时；这些与模型推理成本分开解释。方法、哈希和原始材料路径已保存，可在下一轮沿用，不能把本次方案当成已实施的仓库架构。
