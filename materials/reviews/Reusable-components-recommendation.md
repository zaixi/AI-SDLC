# 用现成组件解决当前痛点：选型核对

核对日期：2026-10-08。目标是使用持续维护的上游组件，少量补充本地适配；当前只做选型与资料保存，没有安装或运行，不能据此宣称已验证兼容性。

## 建议组合

优先保留现有代理工具，使用 Matt Skills 主交付链；补充 Humanlayer Show Me 的通用视觉解释；团队共享与知识检索需要时评估腾讯 TeamAI。先配置现成能力，再决定是否需要自写 Skill。

| 组件 | 直接使用价值 | 更新与边界 |
|---|---|---|
| Matt `grill-with-docs` → `to-spec` → `to-tickets` → `implement` → `code-review` | 串联目标、设计决策、任务、实现与评审 | 官方 README 提供 Claude Code / Codex / Copilot 插件安装方式；插件有自动更新路径。具体客户端兼容性未实测 |
| Matt `improve-codebase-architecture` | 探索存量代码中的架构摩擦，生成带前后图示的 HTML 候选报告 | 不是完整系统架构知识库；重点是重构候选与深模块。报告使用 CDN，未保证完全离线 |
| Matt `pr` | 可视化变更摘要、前后验证证据、合入风险与影响范围 | 是 PR 正文写作方法，不是 Gerrit API 集成；可借鉴到评审说明 |
| Matt `diagnosing-bugs`、`research`、`wayfinder`、`retro` | 存量问题调查、未知问题探索、跨会话规划和环境改进 | 按问题选择，不必强制所有任务走全流程 |
| Humanlayer `show-me` | 通用架构、调用与数据流解释，短文字与图示结合 | Matt `pr` 明确注明借鉴该 Skill；两者可分别用于日常理解与变更说明。Show Me 不验证图的正确性，也不提供自动维护机制 |
| 腾讯 `teamai-cli` | 分发 Skills / Rules / Docs；团队经验检索、代码图谱与知识维护 | 官方文档的 Team Context / Improvement 标为 beta；需试点，不等于完整理解问题已经解决 |
| TeamAI Reference Template | 快速建立团队资产仓、取得现成工程规则及评审资源 | 内容是经过改编的上游文件；复制模板不会自动继承原始 Matt/ECC 的更新 |
| 字节 Trae Agent | 可安装的编码代理与执行轨迹记录 | 是执行工具，不是现有代理旁的流程补丁。仓库强调研究友好；本次 API 显示最后 push 为 2026-02-05，不适合仅据 README 判断持续维护频率 |
| 字节 DeerFlow | 长任务代理 harness、工具、记忆与沙箱 | 可以使用，但增加部署与运行框架；对当前已有编码代理的需求优先级低 |

## 享受更新：关键选择

1. Matt 官方 README 推荐每个代理选一种安装路径，不要插件和文件安装同时部署造成重复。插件可自动更新；`skills.sh` 文件方式需要运行更新命令，并重新添加新 Skills。优先保持上游文件原样，把本地政策写在项目配置或独立 Skills 中。
2. TeamAI 自动同步的是团队资产仓的更新，不自动证明第三方上游内容也已更新。跨团队 `source` 订阅要求源仓 `teamai.yaml` 声明 `publicSkills`；没有该声明会同步零个 Skill。不能直接承诺把 `mattpocock/skills` URL 填进去就可用。可选 Matt 官方插件独立更新，TeamAI 分发自有资产；如果希望 TeamAI 统一分发 Matt，需另行验证其子模块或桥接方案。
3. 模板是起点，不是依赖管理系统。不要复制其旧版 Matt Skills 后再与官方插件安装同一功能。
4. 当前抓取的 TeamAI main 文档包含新功能与迁移说明；npm latest 元数据显示 0.26.0，而抓取的 main package.json 显示 0.22.0。这些元数据存在差异，需要按安装版本核对实际命令，不能把所有 main 文档功能都当作已验证的发行功能。

## Gerrit 与 C/C++ 的实际适配点

- Matt Setup 支持 GitHub、GitLab、本地文件与用户描述的其他 tracker；可保留已有任务管理系统。Gerrit 是变更评审系统，不应默认替代需求/任务跟踪。
- 本次 TeamAI provider 文档没有专门的 Gerrit provider。通用 Git provider支持仓库 Git 操作，但不提供统一的自动 PR/MR 创建；不能视为已支持 Gerrit Change / patch set / 评论 / 审批流程。
- TeamAI 官方文档列出的 AST 轨为 TS/JS、Python、Go、Swift，其余语言使用启发式轨。C/C++ / Kernel / BSP 场景的调用、宏、构建配置与并发语义需要真实样例检验，不能把知识图谱当作精确静态分析器。

## 国内实践哪些是工具，哪些是经验

阿里 AAIC/SDD、腾讯端到端交付、美团重构与测试等已归档材料，可以指导规格、验证、评审与知识维护。对这些文章所述完整内部系统，目前未找到与文章逐一对应、可公开安装的完整发行物。不能将实践文章当成可以直接安装的 Skills 包。

CodeBuddy、TRAE、Qoder 等商业工具属于另一个选项：可以评估其公开产品能力，但不能据其品牌推断包含文章中的所有内部机制，也不能据它们支持 Skills 推断已经支持你的 Gerrit 流程。既然用户已有代理与 ask-matt，暂不以换 IDE 为主方案。

## 少量本地补充：候选而非已决定实现

- 中文输出、图示优先、术语保留对应英文、给出来源：先用项目规则配置，不急着新增 Skill。
- Gerrit 变更说明：确有缺口时用独立 Skill 将 Change-Id / patch set、改动意图、接口与不变量影响、前后证据和未验证项串起来。是否需要 API 适配取决于现有工具能力。
- 知识校验：先试 TeamAI 的检索、代码图谱、维护能力，再决定是否补“图/ADR 与代码版本关联、标记失效”的小 Skill。

原则是采用一套主流程，各补充组件承担清楚的职责。不要同时叠加多套完整方法论，让重复的规划、TDD 与评审规则成为新的负担。

## 依据

- [本次官方文档与元数据快照](../references/reusable-components-20261008/README.md)
- [Matt Skills](https://github.com/mattpocock/skills)，当前核对提交 b0618bc436ad893b3c5e84e55fba86586d34a404。
- [TeamAI](https://github.com/Tencent/teamai-cli)，当前核对提交 ec7d4db07e4be5aea2c18bafec7472b7792fdf38。
- [TeamAI Reference Template](https://github.com/teamai-hub/teamai-template)。
- [Humanlayer Show Me](https://github.com/humanlayer/skills/tree/main/plugins/show-me)。
- [Trae Agent](https://github.com/bytedance/trae-agent)、[DeerFlow](https://github.com/bytedance/deer-flow)。

网页和代码文档可能继续变化。本次未执行这些文档中的安装、发布或代理调用指令。

## 阿里与字节：补查后的修正

先前仅按现有代理旁的补充组件筛选，对 Qoder 知识能力介绍不足。官方 Repo Wiki 文档表明：可生成结构化项目知识，支持中英文、代码变更检测、受影响部分更新、人工修订保护和 Git 共享；自动团队共享需要 Teams plan，生成与更新消耗 Credits。通常需要点击 Update 或手动触发生成，不能将变更检测等同于无条件全自动更新。每项目最多 10,000 文件，因此大型 Kernel/BSP 仓库应按子系统试点。这与用户的存量项目理解和知识更新痛点直接相关，值得优先试用。支持 Skills 不代表已验证 Matt 的所有工具调用与插件机制兼容。

TRAE 官方 Skills 页可读取到内嵌正文，支持 SKILL.md、外部文件/ZIP 导入、全局/项目 Skills、按需加载和规则配置。文档用 codemap 作为调用示例，但此例本身不能证明提供了完整、持续维护的代码架构地图；未据此宣称已经解决知识更新问题。复制导入第三方 Skill 也不等同于自动更新上游。

Qwen Code 官方 README 提供可部署编码代理、IDE 等接入方式和记忆/Skills 能力，可作为开源执行底座；不能将其视为完整公开版 AAIC/SDD，也未证明它替代 Repo Wiki 或完整的系统理解机制。

补查来源与正文已保存到现成组件快照目录。仍未安装或实际验证。

## 美团、华为、京东、百度补查

- 华为云码道（当前产品，不应只依据旧 CodeArts Snap 文档）：官方 CodebaseWiki 文档支持从代码生成全局与项目知识，检测代码改动，点击更新受影响内容；限制代码文件不超过 10,000。Skills 官方文档明确有系统内置、市场内置与自定义技能，市场内置涵盖单测、评审、文档、安全、构建、重构，并支持本地和云端技能。企业文档知识库只支持云端管理；它与代码生成的 CodebaseWiki 是不同功能。值得列为 Qoder 之外的优先试用候选，但未核实 Gerrit 集成、第三方插件兼容性和更新策略。
- 美团 CatPaw：2026-07-28 官方发布描述的是全场景 Agent 工作台与 Managed Agents，包含即装专家/技能、跨会话记忆、团队分发与托管能力。不能把这些能力直接等同于此前文章中的 31 万行代码重构和单测内部系统，也没有据公开页面证明相关完整工程 Skills 可移植到现有代理。NoCode 偏应用原型，当前维护复杂存量项目的优先级低。
- 京东 JoyCode：官方 Skills 文档确认支持技能加载与创建；但本次读取的 RepoWiki 官方页面明确写“当前仅支持京东内部 Coding 代码仓库”。虽然展示结构化可视化知识图谱，不能直接推荐给外部团队作为开箱即用的代码知识库，需要供应商确认新版本是否已开放。
- 百度 Comate：发现官方 Skills 文档入口，但本次静态页面主要是导航，没有取得完整功能正文。暂列候选，不能据搜索摘要宣称已有适用于用户的知识更新与可视化能力。

本次官方文档与搜索发现记录：[公司工具补查快照](../references/company-tools-20261008/README.md)。没有安装、登录或运行这些产品，未将厂商的准确性和效率宣传作为独立实测结论。
