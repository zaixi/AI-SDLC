# mattpocock/skills 能力与组合方式核查

核查日期：2026-09-24。对象为作者官方仓库，固定到 [c55ee46073ed923f86ce59a5eb3b6d895095d1b7](https://github.com/mattpocock/skills/commit/c55ee46073ed923f86ce59a5eb3b6d895095d1b7)（提交时间 2026-09-18）。GitHub API 与该提交的 raw 文件实际读取成功；本轮 Web 搜索工具返回 503，因此没有以搜索摘要作为依据。对照本地[方法设计](../METHOD.md)；本报告只调查与建议，不安装、不执行被调查的 skills。

**结论：它已提供许多值得直接借鉴的日常工程实践，我们没有必要重新设计每个动作；但不能据此认定它已经解决本方法的大部分目标。** 动作覆盖与目标达成不同：有没有访谈、规格、测试、交接 skill，不能回答人的讨论是否过载、设计是否容易理解、约束能否长期发现、证据是否仍有效。

作者将其定位为小型、可调整、可组合的 skills，并有意避免由一个框架接管整个开发过程。“AI 原生 SDLC 的一组实践”是我们对其用途的归类，作者并没有在该 README 声称交付统一的完整 SDLC。[上游 README](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/README.md)

## show-me 与 eli5 对当前可读性问题的帮助

本次假定用户所说的 `eli5` 是 `anthropics/claude-plugins-community` 中的同名 skill；若实际安装来源不同，需要重新核对。两者不属于 mattpocock/skills。

| 来源与核查版本 | 源码实际要求 | 本方法如何借鉴 |
| --- | --- | --- |
| [show-me](https://github.com/humanlayer/skills/blob/ca7c8088db69e315a8b2deea43820270457f8f3c/plugins/show-me/skills/show-me/SKILL.md)，HumanLayer，`ca7c8088` | 用讲清当前问题的最小视图，按问题选择树、伪代码、Mermaid、diff 或 HTML；已有结构优先呈现变化；图文相邻，避免一次使用全部形式。标记为 `disable-model-invocation: true` | 首轮展示功能的整体路径，后续展示本轮变化；只有交互确实改善理解时才增加 HTML，不把图数量当质量 |
| [eli5](https://github.com/anthropics/claude-plugins-community/blob/a727be1c7bd6064419b6f60d71993a19198adc17/eli5/skills/eli5/SKILL.md)，社区插件仓库，`a727be1c` | 一条很短的核心指令：面向不了解主题的人，用 HTML、大图和少量文字解释；没有完整的教学设计或准确性校验流程 | 先用具体场景与直观结果建立理解，再按需展开规则；简化表达仍保留关键限制和依据，不把读者幼儿化 |

**判断：两者能直接改善呈现，但不会自行修复方法结构、抽象词过多或规则相互缠绕。** 当前更值得先做的是“给人看的短入口 + 可追溯的详细规则”：入口让人看懂这个功能如何推进、此刻要判断什么，细节留在同一工程资料体系按需读取。社区仓库归属不是研究实证；以上源码没有提供可读性效果试验，不能宣称已证明提升理解。

## 与我们需要的八类活动对照

| 活动 | 上游实际提供什么 | 适合借用什么；需要调整什么 |
| --- | --- | --- |
| 需求澄清 | `grill-with-docs` 本体调用 `grilling` 和 `domain-modeling`；`grilling` 按设计树逐轮提出整个待决前沿，要求所有分支走完、决定交由人作出 | 借用调查事实、识别决策依赖和及时记录。提问量、所有决定交给人、穷尽分支的终点与我们的收敛原则冲突，不能原样成为默认入口。[源码](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/grilling/SKILL.md) |
| 解释与图文理解 | `prototype` 区分逻辑演示和 UI 变体；`improve-codebase-architecture` 生成带前后对比图的 HTML 报告；`wait-what` 重新提供背景并用简明语言解释 | 原型回答具体设计问题、前后对比和重新解释均可借用；架构报告的 `/tmp` 落点、CDN 依赖及后续 grilling 要适配持久文档与适量讨论。`wait-what` 的简化英语要求也需适配中文。[prototype](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/prototype/SKILL.md)、[架构报告](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/improve-codebase-architecture/SKILL.md)、[wait-what](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/wait-what/SKILL.md) |
| 领域与设计知识 | `domain-modeling` 维护术语表、用边界场景核对概念、当场更新；ADR 需同时满足难逆转、缺少背景会令人困惑、有真实取舍 | 共享术语、惰性建文档和精选 ADR 可复用。但术语表被明确限制为词汇表，小而重要的不变量未必达到 ADR 门槛，不能仅靠两者承担全部工程知识。[源码](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/domain-modeling/SKILL.md) |
| 规格形成 | `to-spec` 综合已有对话，不重新访谈；列需求、实现与测试决定、非目标；要求确认测试边界，生成很长的用户故事清单并发布到配置的 tracker | 综合既有决定、先考虑验证很适合借用；长清单、额外确认与发布行为应按实际范围裁剪。它本身不是图文审阅流程。[源码](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/to-spec/SKILL.md) |
| 拆解与渐进规划 | `to-tickets` 采用可演示的纵向切片与阻塞关系；`wayfinder` 维护低分辨率索引、尚未明确事项和按需读取的决定票据 | 纵向切片、只展开当前可知部分、索引指向唯一细节都值得借用；逐次批准拆分、默认人参与的决定票据、每会话最多解决一个非研究票据，会限制自主推进。[to-tickets](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/to-tickets/SKILL.md)、[wayfinder](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/wayfinder/SKILL.md) |
| 实现与测试 | `implement` 驱动 `tdd`、运行检查、最后做 `code-review` 并提交当前分支；`tdd` 强调公共行为、独立预期和一个切片一次测试 | 行为测试与小步反馈可复用；预先确认测试边界应复用已有授权，不能每次重复问。提交行为需服从当前范围。该版本将重构放到评审阶段，不能用通常的 red-green-refactor 标签代替实际源码。[implement](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/implement/SKILL.md)、[tdd](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/tdd/SKILL.md) |
| 审阅与故障诊断 | `code-review` 用独立子 agent 检查规范和需求符合性；`diagnosing-bugs` 要求先建立能复现症状的反馈，再缩小、检验假设并回归 | 两条审阅轴与症状回归很有价值。审阅默认 `git diff <base>...HEAD`，不能直接涵盖未提交变更；还需明确 tracker 和 spec 来源。源码阅读不是运行证据或系统验收的替代。[code-review](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/code-review/SKILL.md)、[diagnosing-bugs](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/diagnosing-bugs/SKILL.md) |
| 接力与持续改进 | `handoff` 用指针引用已有产物并保存会话摘要；`in-progress/retro` 从失败中寻找导航、自动检查和指令删减机会 | 引用现有资料、从失败修正环境可借用；handoff 指定保存到 OS 临时目录，适合短期恢复但不满足长期工程资产要求。retro 属于 `in-progress`，不应当作稳定交付。[handoff](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/handoff/SKILL.md)、[retro](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/in-progress/retro/SKILL.md) |

## 能不能作为子 skill

**可以借用，但需要区分可自动调用的能力与由用户触发的编排入口。** 当前 README 明确规定：user-invoked skills 负责编排，可以调用 model-invoked skills，但不能调用另一个 user-invoked skill。这是作者的组合约定；具体宿主怎样执行元数据，需要在选定运行环境后确认，不能将它说成跨所有 agent 的强制隔离机制。[上游组合说明](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/README.md#reference)

由一个 workflow 入口选择性组合这些能力，是我们后续实现的设计建议，尚不是已实现、跨平台可用的函数调用协议。本阶段只确定职责与兼容原则。

- **可复用能力候选**：`research`、`domain-modeling`、`codebase-design`、`prototype`、`tdd`、`diagnosing-bugs`、`code-review`，其主文件没有 `disable-model-invocation: true`。选择任务实际需要的能力；上表中的授权、输出位置与审阅范围仍需核对。
- **用户触发的入口**：`grill-with-docs`、`to-spec`、`to-tickets`、`implement`、`wayfinder`、`handoff` 等明确设置 `disable-model-invocation: true`。未来若要由我们的 workflow 自动编排，不宜直接串起原入口；可以让人显式调用，或将真正需要的机制做成清楚标注来源的适配版本。
- **skill 与子 agent 不同**：此仓库很多调用只是要求加载另一个 skill 的指令；是否创建独立执行上下文由具体技能另行规定。例如 `research` 明确要求后台研究，`code-review` 明确要求两个并行评审。不能因为称作“子 skill”就假定天然具备上下文、权限或文件隔离。[research](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/research/SKILL.md)、[code-review](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/code-review/SKILL.md)

借用时还要保留支撑文件和实际依赖，不能只复制入口：`domain-modeling` 引用文档格式，`prototype` 引用逻辑/UI 分支说明，`tdd` 引用测试与 mocking 指南。若使用 tracker 流程，`setup-matt-pocock-skills` 配置 `docs/agents/issue-tracker.md`、领域文档及可选 triage 标签；GitHub/GitLab 路径分别使用 `gh`/`glab`，也支持本地 Markdown。涉及子 agent、浏览器、Git 和外部 tracker 的能力需由宿主提供。[setup 源码](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/setup-matt-pocock-skills/SKILL.md)

仓库提供 [MIT LICENSE](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/LICENSE)，包括修改与分发许可及保留版权、许可声明的要求。若将来做适配版本，应记录来源提交与差异；本次没有复制这些 skills 到方法项目或安装它们。

## 本地与上游的差异核查

逐字节比较本机已安装的 `<name>/SKILL.md` 与上述固定提交，以下 16 个主文件一致：`grill-with-docs`、`grilling`、`domain-modeling`、`to-spec`、`to-tickets`、`implement`、`prototype`、`tdd`、`code-review`、`diagnosing-bugs`、`research`、`handoff`、`wayfinder`、`setup-matt-pocock-skills`、`teach`、`wait-what`。

这只能证明已检查的主文件一致；没有核验所有支撑文件、安装器元数据、宿主对调用标记的解释或真实执行效果。磁盘存在也不等于当前会话已将它作为可调用 skill 暴露。

## 对方法设计的建议

1. **复用具体工程动作，保留统一的交接规则。** 将成熟的调查、原型、领域建模、行为测试和双轴审阅作为候选能力。本方法只约定何时用、输入什么、什么结果足以继续，以及授权与资料如何沿用，不重新写一套 TDD 或调试教科书。
2. **先借呈现方式解决当前可读性问题。** 人的入口先展示一个具体功能如何从需求走到维护，说明此刻看什么、决定什么、下一步是谁做。规则正文按需展开；把文本放进 HTML 或增加图数量，本身不能证明更易理解。
3. **不要借回原先已经证明不合适的默认行为。** 穷尽访谈、全部选择由人批准、长用户故事清单、一个决定一个会话、临时目录作为唯一保存位置，都需按已接受目标调整。形式上的可组合不等于语义兼容。

在本轮核查的核心路径中，尚未看到一套统一机制完整覆盖：按理解与风险收敛审阅、承诺/实现符合性/证据有效性分开维护、资料与实际版本共同演进、跨会话接手效果验证，以及包含人的负担的整体评价。发布、运行与安全等领域有局部辅助能力，也不能仅凭这些开发 skills 推断完整覆盖。这些是我们方法需要继续定义的衔接，而不是否定上游实践价值。

以上是来源核查与设计判断；没有真实比较试验，不能给出“已解决百分之多少”或效率提升结论。
