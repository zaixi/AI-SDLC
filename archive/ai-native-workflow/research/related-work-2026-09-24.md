# 同类实践调查：Spec-Kit / OpenSpec / Superpowers / Trellis / mattpocock-skills

调查者：Claude（Opus 5），2026-09-24
性质：**一手来源调查，不是选型决定。** 本文只回答"别人怎么做的、哪些机制值得借鉴"，不主张采用任何一个项目。不采用同样是有效结论——借鉴一个概念，不等于安装一个工具。

调查动机：方法正文第 9 节此前只写"综合 Anthropic、OpenAI、Google/DORA 资料"，未对照同期的开源工程实践。若不核对，容易出现两种错误判断——"这些已经解决了大部分问题，照搬即可"，或"它们都不相干，全部自建"。

调查方法：五个项目均查官方仓库与文档，不依据印象或二手概述。本地已安装的 `mattpocock/skills` 直接读源码（60 个 skill 的描述，以及 `handoff`、`wayfinder` 全文）。

文中 `:NNN` 形式的行号均指 **`METHOD.md`**（即 2026-09-24 文件重组前的 `README.md` v0.8，重组后行号未变）。

---

## 一、各项目定位与最值得借鉴的机制

### OpenSpec（Fission-AI）

面向 AI 编码助手的 spec-driven 框架，npm 分发，明确定位 **brownfield（1→n）**：先发现既有行为，再写任何规划产物。

- **`specs/`（当前真相）与 `changes/`（提案）双目录分离。** 归档时把当前规格同步回真相源，**整个变更目录移入 archive 保留**——proposal、design、task 并非删除，而是退出"当前"、转为历史。（本条最初据二手摘要写作"用完即弃"，经固定版本源码核查后更正，见文末校正记录。）
- **spec deltas**：每个变更以 ADDED / MODIFIED / REMOVED 的需求条目表达，采用 GIVEN/WHEN/THEN 格式，对着持久基线审查，代码未写前即可审。
- 命令：`/opsx:explore`（先探明当前行为）→ `/opsx:propose` → `/opsx:apply` → 归档。
- 学术对照指出其取舍：profile 刻意精简，把意图集中在单一规格与可追溯的变更提案上，**复杂场景下覆盖的过程较少**。

### Spec-Kit（GitHub）

`constitution` → `specify` → `clarify` → `plan` → `tasks` → `implement`/`converge`，每阶段产出下阶段消费的产物。

- **`constitution.md`：一次性确立项目层面不可协商的原则**，与特性级 spec 分层。
- `converge`：重复 implement → converge 直到报告收敛。
- 局限：GitHub 自己定位其为"检验 SDD 方法论是否可行的实验"，非成品。外部批评为 **"sea-of-markdown"**——给出干净的 spec 和第一次生成后，后续留给用户自理。

### Superpowers（obra / Jesse Vincent）

四支柱：Socratic brainstorming（创造性工作前强制）、TDD（红绿重构，明确要求删除先于测试写出的代码）、系统化调试（四阶段，根因先于修复）、subagent 驱动开发（生成独立 subagent 对照计划复核并按严重度标记）。

- **最值得借鉴的一条：作者用 "TDD for skills" 验证 skill 本身**——让 Claude 在一组 subagent 上测试新 skill 是否可理解、完整、会被遵守。早期失败模式是 **"游戏问答式测验（gameshow-style quizzing）"，改用真实压力场景后才有效。**
- 官方 marketplace 分发，截至 2026 年中逾 82 万次安装。

### Trellis（mindfold-ai）

多平台 agent harness，4 阶段循环：Plan(Brainstorm) → Implement → Verify(Check) → Finish(**Update Specs**)。

- **`trellis-update-spec`：把实现中获得的新认识提升回 `.trellis/spec/`**，使下一次会话起点更高。
- **hook 自动注入**：每次会话开头自动提供 `.trellis/spec/` 的架构约定，减少重复提示。
- `.trellis/tasks/` 做有状态任务跟踪，`workspace/` 保存跨会话 journal；同一结构覆盖 22 个平台。
- 官方警告两条：生成的项目文件会造成 **review noise**；**只有团队真正维护 spec/tasks/journal，价值才会出现**。

### mattpocock/skills（本地已安装，60 个）

以 **issue tracker 为骨架**的 SDLC 实践，不是零散技法：`define-goal` → `wayfinder` → `grilling`/`grill-with-docs` → `domain-modeling` → `to-spec` → `to-tickets` → `implement` → `code-review` → `retro`。

- **`wayfinder`**：把超出单次会话的大块工作化为 issue tracker 上的**共享决策地图**。其中三条规则与本方法高度重合，且已可执行：
  - "The map is an **index**, not a store"——一个决策只存在于一处，地图只索引不复述；
  - 阻塞用 tracker 原生依赖，**frontier** = 开放且未阻塞未认领的票；
  - `Not yet specified`（fog of war）与 `Out of scope` 分开表达。
- **`handoff` 与本方法方向相反**：它把当前对话压缩成交接文档，并明确要求**存入操作系统临时目录而非工作区**。它确实要求"不重复 spec/ADR/issue/commit 已有内容，改为引用路径"，但产物仍是会话摘要，不是持久工程知识。

---

## 二、按四个高层目标对照

不按方法文档的条款逐项对账，而是回到最初提出的四个目标，看这些项目分别解决到什么程度。

### 目标一：少提问、先看整体、再逐层细化

| 现有解法 | 空白 |
| --- | --- |
| Superpowers 的 brainstorming 被设为创造性工作的强制前置；OpenSpec 的 `explore` 在既有代码库里先探明当前行为；wayfinder 用 frontier 控制"现在该决定哪一件"；Spec-Kit 的 `clarify` 只针对欠明确处提问 | **机制层面没有明显空白，重新发明收益最低。** 但须注意：**存在澄清机制不等于"少问且理解充分"已被证明**——源码只能证明机制存在，效果仍需实际任务评价 |

### 目标二：文档可读、能快速评审

| 现有解法 | 空白 |
| --- | --- |
| Spec-Kit 的 constitution 与特性级 spec 分层；show-me 的"最小视图"原则 | **所有项目都有同一个未解问题：产出会膨胀。** Spec-Kit 被批评 "sea-of-markdown"，Trellis 官方警告 review noise。**没有任何一个项目给出"文档增长本身也是成本"的处理规则** |

### 目标三：agent 在授权内连续执行，人不必值守

| 现有解法 | 空白 |
| --- | --- |
| Trellis 用 hook 在会话开头自动注入约定，保证上下文可得；Superpowers 用独立 subagent 复核并按严重度标记，其执行 skill 亦定义了连续执行与停点；Spec-Kit 有可恢复的 workflow；Trellis 的 check 子 agent 能自修 lint/type/test | **各自有局部停点，但没有统一的授权边界模型**——哪类动作需要哪种授权、越界如何升级、子 agent 是否继承权限，均无跨流程的一致表达。真正的问题是各家的默认停点是否适合本项目，而非完全没有这类机制。（本条最初写作"没有一个回答"，过强，已更正） |

### 目标四：知识持久有效，支持跨人跨 agent 接力

| 现有解法 | 空白 |
| --- | --- |
| OpenSpec 的 `specs/`（真相）与 `changes/`（脚手架，用完即弃）；Trellis 的 `update-spec` 回流；wayfinder 的"地图是索引不是存储" | **三处空白：**①无"前提变化→结论待复核"的生命周期；②证据不绑定被测版本与环境；③无接力验证——`handoff` 方向相反，它生成会话摘要并存入临时目录 |

**小结**：目标一基本已被解决，目标二各家都有同样的病，目标三、四是真正的空白区。**若要投入自建，价值集中在目标三和目标四。**

---

## 三、两条应进入风险清单的前车之鉴

1. **Spec-Kit 的 "sea-of-markdown" 批评。** 结构化产出本身会累积成负担，最终无人阅读。
2. **Trellis 的官方警告：review noise，且只有真正维护时才有价值。** 未被维护的规格与日志是净负债。

方法目前详述了"哪些知识必须保留"，但**没有一条规则处理"文档增长本身的成本"**。第 7 节的场景表已呈现逐轮增长趋势（7→9→11），`:150` 新增的删减原则尚未实际执行过一次。建议把"产出负担"列为与"知识缺失"同等的失败模式。

---

## 四、可借鉴的机制清单（借概念 ≠ 装工具）

按本方法 `:194` 的既有立场——"借用机制不意味着绑定、安装或原样执行某个 skill"——以下按机制列出，不按项目绑定：

| 机制 | 来源 | 借鉴方式 |
| --- | --- | --- |
| 真相与提案双目录，脚手架用完即弃 | OpenSpec | **概念可直接采用**，不必引入其工具链 |
| 变更以 ADDED/MODIFIED/REMOVED 增量表达 | OpenSpec | **格式可直接采用** |
| 不可协商原则与特性级规格分层 | Spec-Kit | 概念可采用，注意避免其 markdown 膨胀 |
| 新认识回流到长期规格 | Trellis | 机制可采用，需补"回流什么、谁判断"的规则 |
| 会话开头自动注入约定 | Trellis | 属实现层（hook），方法层只需规定"上下文必须可得" |
| 用真实压力场景而非问答测验验证 | Superpowers | **直接用于接力评估的设计**，可避免自行踩坑 |
| 独立 subagent 按严重度复核 | Superpowers | 与方法的"独立复核"一致，可作为实现参考 |
| 决策地图：索引而非存储；frontier；fog of war | mattpocock `wayfinder` | 机制成熟，可作为跨会话推进的参照 |

若将来确需选定一个项目作为执行骨架，判断依据应是：**是否面向 brownfield（既有代码库）、是否区分真相与提案、产出负担是否可控**——而非功能多寡。本文不作此决定。

---

## 五、调查的局限

- 五个项目均未实际安装试用，结论来自官方文档与（对 mattpocock/skills 而言）源码阅读，**不构成对其实际效果的验证**。
- 各项目仍在快速演进，文中版本细节随时可能变化。
- 覆盖度判断依据其公开文档所述能力；某个项目可能存在文档未描述的机制。
- 本方法自身同样未经试运行，因此上文判为"空白"的各项，只说明别处没有现成方案，**不说明本方法在这些维度上已被证明有效**。

## 六、校正记录

本文初稿依据官方文档与检索摘要写成。同日 [四项框架的源码核查](sdd-frameworks-assessment-20260924.md) 用**固定 commit 的源码**复核后，指出两处事实错误，均已在正文更正：

| 初稿说法 | 更正 | 原因 |
| --- | --- | --- |
| OpenSpec 归档时 proposal/design/tasks "用完即弃、不留存" | 整个变更目录移入 archive 保留，只是退出"当前" | 初稿据二手摘要"scaffolding that served their purpose"推断，未核源码 |
| "五个项目都默认人在旁边，没有一个回答 agent 何时可以不问人" | 各自有局部停点（如 Superpowers 执行 skill、Spec-Kit 可恢复 workflow），缺的是**统一的授权边界模型** | 初稿未读执行类 skill 源码，概括过强 |

另接受一条方法论提醒并写入正文：**存在某种机制不等于该机制的效果已被证明。** 源码可证明机制存在，效果须由实际任务评价。

记录此节的目的，是保留"结论曾经错过、如何被纠正"的过程——这正是本方法主张的：旧结论保留历史原因，当前入口指向有效结论。
