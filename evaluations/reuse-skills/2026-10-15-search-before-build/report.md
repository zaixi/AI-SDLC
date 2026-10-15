# search-first 与修改版：五题重新对照

修改版保留了外部发现，并减少了部分研究开销：本轮五题全部交付，原版四题交付、附件题超时。但修改版没有展示出全面的质量优势，执行器题成本反而更高，接入错误与过度设计仍在。

比较的是 ECC search-first 冻结原文与以它为基础修订的 search-before-build。两组都是本轮新跑，每题一次，OpenCode 1.14.28 + deepseek-flash/high，相同隔离与预算。没有把旧轮失败混入本轮成绩，也没有无 Skill 基线。方法见 [README](README.md)，[原始产出对照页](/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-search-before-build-182253/gallery.html)。

## 逐题结果

| Case | 原版 search-first | 修改版 search-before-build | 判断 |
|---|---|---|---|
| R01 复用 CSV | 59.89 秒；9,585 输出 token；正确复用，留下新增测试；做渠道预检、研究 lone-CR 边界 | 24.99 秒；2,339 token；正确复用，以临时脚本验证；省去渠道预检 | 两组独立行为检查通过；修改版更简洁，原版留下可复跑的新增测试 |
| R02 目录打包 | 53.28 秒；6,859 token；搜索包与系统工具，采用标准库 | 56.40 秒；7,586 token；搜索 PyPI 并验证 zip/make_archive 的符号链接行为，采用标准库 | 两组行为检查通过；修改版没有降低此题成本 |
| R03 链接检查选型 | 146.57 秒；29,312 token；两个研究子 agent，选 lychee | 90.29 秒；11,773 token；直接调研多个候选，选 lychee | 修改版较快收束，选择与主要需求保留；两份 CI 示例都有缓存更新缺陷 |
| A01 评测执行器 | 99.23 秒；14,235 token；保留内核、借鉴 Inspect，建议配置组件 | 139.19 秒；25,177 token；提出条件性接入 Inspect + inspect_swe，借鉴 Harbor | 两份均完成；修改版发现和组合讨论更具体，但有 API 接入错误，并非更轻或更可靠 |
| A02 附件发布 | 600.01 秒超时；34,080 token；未生成 design.md | 505.95 秒；26,737 token；Releases 主通道，可选镜像，交付设计 | 修改版完成度较好；仍研究过长，增加附件仓与多清单，下载校验不闭合 |

R01/R02 的四个产出均通过旧轮独立检查，覆盖 CSV 转义、空输入、生成器、Unicode，以及递归打包、相对路径、符号链接、输出在源目录内和覆盖已有输出。检查在隔离环境执行，不修改产出。结果见 [behavior-checks.json](behavior-checks.json)。R01 两组只修改了获准实现的原有 export.py；原版另新增 tests/test_export.py。其余题的 supplied 文件未被修改。

## 主动发现有没有保留

保留了。修改版 R02 查询 PyPI 候选，R03 查找并比较 lychee、linkinator、htmltest 等，A01 找到 Inspect SWE 的 OpenCode 集成与 Harbor 的相关设计，A02 比较 Releases、OCI、DVC、Zenodo 等。它没有退化成“已有本地代码就直接结束”。

但不是每一条指令都得到执行：R02 有外部包查询，却没有观察到明确的 GitHub 搜索；R01 直接复用本地实现，没有外搜。这对小型适配任务可能合理，但不能声称“每道题都按新增要求查了 GitHub”。研究价值应看是否影响选择，不能靠渠道数量判分。

A01 原版本轮也找到了 Inspect SWE/OpenCode，因此这不是修改版独有的发现。区别在于修改版进一步提出保留隔离内核、适配框架编排层，并指出持久 sandbox 与现有 bwrap 进程模型之间的工程缺口。原版倾向保留自研并借鉴桥接设计。两条路线都有讨论价值，采用更多外部组件不自动得高分。

## 研究是否更容易收束

部分改善。本轮修改版没有调用 task 子 agent；原版 R03 委派两个研究任务，A02 也进行了委派，最终仍卡在研究阶段。修改版在 R01/R03 的调用与输出用量明显下降。

A02 仍是反例：修改版已表示资料足够，之后又检查公开仓库树与 materials 的来源约定，最后用约 506 秒交付。它确实找到可借鉴的清单先例，但最终方案仍扩展到独立附件仓、多份清单、扫描工具与可选镜像。停止规则没有稳定转化成最小方案。

原版 A01 本轮 99 秒完成，而旧轮同题曾耗尽请求预算。因此不能把旧轮失败与本轮修改版成功直接相减、宣称已消除失败模式。原版 A02 的停止原因是墙钟超时，不是 48 次请求或输出预算耗尽；公网访问延迟影响两组耗时，不能把全部差值归因于 Skill。

## 质量上的具体问题

**R03：两份 CI 都不能持续更新同一提交的缓存。** 两组 key 都使用 github.sha；周期运行同一提交时，会命中不可变缓存，更新后的结果无法写回同一个 key。原版即使用单独的 save 步骤也没有解决 key 不变的问题。官方 [actions/cache 更新缓存说明](https://github.com/actions/cache/blob/v4/tips-and-workarounds.md#update-a-cache) 要求新 key 才能保存更新。两组都保留了本地链接检查，未出现旧轮 Ai-Eastern 排除 file 链接的错误；没有实际执行这些 CI。

**A01：修改版的发现有效，API 示例却不准确。** Inspect SWE 确有 [OpenCode 集成](https://meridianlabs-ai.github.io/inspect_swe/opencode.html)，但设计把 `forward_generation_config=True` 传给 `inspect_swe.opencode()`；当前 [opencode 公开签名](https://meridianlabs-ai.github.io/inspect_swe/reference/#opencode) 没有该参数，它属于 [agent bridge 层](https://inspect.aisi.org.uk/agent-bridge.html#generation-config)。这需要修改适配器或选择合适接入方式，不能照该示例直接调用。

修改版还反复称 Inspect 没有内建 mock model，但上游已有 [mockllm provider](https://github.com/UKGovernmentBEIS/inspect_ai/blob/main/src/inspect_ai/model/_providers/mockllm.py)。这不证明它能直接替代现有隔离审计，却足以说明“没有 mock model”的判断过满。它引用 relay_base 旧的 65,536 token 审计断言，也没有准确区分被 run.py 覆盖的当前路径。

原版则把恢复运行条件写成“只补跑缺 result.json 的任务”，而实际入口跳过所有已存在 run 目录；并引入 Hydra/OmegaConf、SDK、LiteLLM 等可选演进，使简单配置痛点扩展成多个组件选择。两组都过早排除 promptfoo，没有认真比较 [外部脚本 provider](https://www.promptfoo.dev/docs/providers/custom-script/) 与现有沙箱组合的路径。

**A02：修改版的维护负担与校验流程仍需修正。** 推荐默认新建附件仓，虽然给出沿用主仓的较小方案，却没有证明分仓收益足以抵消维护成本。下载命令只取 raw-requests.tar.zst 与 SHA256SUMS，后者定义为所有附件的清单，因此直接 `sha256sum -c` 会因其他附件缺失失败。应下载相应附件或限定校验集合。

它还将不可变 Release 描述为“发布后不可撤、只能删除非 immutable release”。官方 [不可变发布说明](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases) 区分锁定附件与删除整个 Release，并明确讨论删除 immutable release 后的 tag 行为。这种过强断言会影响保留策略。设计提出人工复核是有益的，但不能以“发布后绝不可撤”的错误前提解释它。

这些都是静态核对结果；本轮没有安装第三方候选、运行迁移、上传附件或修改真实基础设施。

## 成本与表达

| 五题合计 | 原版 | 修改版 |
|---|---:|---:|
| 交付目标文件 | 4/5 | 5/5 |
| 实际模型请求 | 94 | 62 |
| 服务报告输出 token | 94,071 | 73,612 |
| 累计输入 token | 3,363,763 | 2,226,268 |
| 逐题墙钟相加 | 958.98 秒 | 816.82 秒 |

修改版本轮输出 token 约少 21.7%，请求约少 34.0%。统计包含子 agent、压缩与失败题消耗；累计输入包括重复上下文，未折算费用。并发为 2，逐题墙钟之和不是整个批次实际等待时长。完整指标见 [metrics.json](metrics.json)。

交付文字没有变得更精练。R03 原版/修改版分别为 12,245/13,033 字符，A01 为 13,238/17,515 字符；修改版 A02 为 19,182 字符。修改版 R03 主要用英文，也没有贴合本轮中文请求的表达习惯。不能把减少中间推理 token 等同于减少用户阅读负担。

## 本轮判断

这版值得保留为继续使用的候选：主动发现仍在，五题均交付，部分研究成本下降。但尚不足以认定它比原版全面更好，尤其不能宣称方案准确性或简洁性提高。

本轮结束后没有根据错误继续修改 Skill。先保留版本与证据；后续若调整，应围绕方案如何收束到当前任务、关键接入假设如何核对，而不是为本次每个错误各加一条规则。

限制：单模型、每题一次、非盲评、无无-Skill基线；未提供完整 ECC 专用 agent 配置。只能比较这次单独加载两个 Skill 的表现，不能推出稳定胜率或 ECC 整套系统的优劣。
