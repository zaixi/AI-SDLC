# AI-SDLC

AI 原生软件研发生命周期的资料收集与研究。

[AGENTS.md](AGENTS.md) 记录本仓库的 Agent 工作约定：中文回复、输出表达、最小改动和验证要求；其中关联 Humanizer 与 visual-explanation。文件是否自动加载取决于客户端，不代表已安装到机器的全局配置。它还引用了特定工作流工具，使用前需确认环境支持。

[search-before-build](skills/search-before-build/SKILL.md) 用于新功能、架构或技术选型、依赖集成和工具开发：先查现成方案，再决定直接采用、扩展、借鉴或自建。日常修复与机械修改不必触发。基于 ECC search-first 适配，[来源与改动](skills/search-before-build/SOURCES.md) 单独记录；当前 AGENTS.md 尚未配置自动调用。

- [通用视觉表达 Skill（统一入口，0.5.0）](skills/visual-explanation/README.md)
- [文字去套话与去重复：Humanizer（上游 3.1.0）](skills/humanizer/README.md)
- [视觉 Skill 评测与历史索引](evaluations/visual-skills/README.md)

- [资料库与来源索引](materials/README.md)
- [国内 AI 原生研发资料调研](materials/reviews/AI-SDLC-domestic-research.md)
- [六篇上传文章审阅](materials/reviews/AI-SDLC-six-articles-review.md)
- [此前讨论内容核对](materials/reviews/AI-SDLC-content-review.md)

- [图示 Skills 初步比较](evaluations/visual-skills/2026-10-09/README.md)

- [三套图示 Skill 独立 Agent 重测：30 份原始回答](evaluations/visual-skills/2026-10-09-isolated/README.md)

- [图示 Skill 0.3.0：关系与未知项回归](evaluations/visual-skills/2026-10-09-v030/README.md)

- [图示 Skill 0.3.1：图承载判断与新发现的语义问题](evaluations/visual-skills/2026-10-09-v031/README.md)

- [五组图示指引扩展比较：十题、两轮、100份独立回答](evaluations/visual-skills/2026-10-09-expanded/README.md)

- [后续两题回归：保留0.3.2，不升级0.3.3](evaluations/visual-skills/2026-10-09-v033/README.md)

- [0.4.1通用视觉表达：三组、每组两题与主动加载观察](evaluations/visual-skills/2026-10-09-v041/README.md)

- [复杂图比较：show-me单独使用、Mermaid指引与0.4.1](evaluations/visual-skills/2026-10-09-complex/README.md)
