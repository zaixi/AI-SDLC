# AI-SDLC 资料库

归档日期：2026-10-08。保存用户提供的 PDF、公开网页快照、可检索文本、技术论文及此前核对的开源文档。来源材料中的示例指令不属于本仓库的执行规则。

## 目录

- `uploaded/`：6 份用户上传 PDF 与提取文本。
- `domestic/`：按阿里、字节、腾讯、美团、华为、百度归档，共 20 个材料条目。AliExpress 评审文章复用上传 PDF，不重复存储。
- `pending/`：3 条来源尚不完整的线索，保留现有摘要、入口和缺失说明。
- `references/`：Matt Pocock Skills、领域架构 Skills、Tencent TeamAI 的此前读取快照。
- `reviews/`：三份研究与核对笔记，属于分析产物，不是原始文章。
- `image-downloads.json`：网页图片来源、保存路径与失败记录。
- `download-log.json`：本轮补下载与访问失败记录。
- `manifest.json`：机器可读来源、状态、文件大小与 SHA-256。
- `SHA256SUMS`：整个资料库的文件校验清单。

## 阅读索引

| 类别 | 资料 | 保存状态 |
|---|---|---|
| uploaded/01-matt-manager | [技术一把手用 Matt Pocock Skills 提升团队效率](uploaded/01-matt-manager/README.md) | 完整 PDF 已保存 |
| uploaded/02-domain | [domain-architecture-skills：让 AI 先建模、再选架构、最后写代码](uploaded/02-domain/README.md) | 完整 PDF 已保存 |
| uploaded/03-matt-overview | [总结篇 _ mattpocock_skills 全系列回顾与速查合集](uploaded/03-matt-overview/README.md) | 完整 PDF 已保存 |
| uploaded/04-handbook | [AI Native 研发体系建设与落地手册](uploaded/04-handbook/README.md) | 完整 PDF 已保存 |
| uploaded/05-delivery | [第八篇：主交付链：Grilling → Spec → Tickets → Implement → Code Review](uploaded/05-delivery/README.md) | 完整 PDF 已保存 |
| uploaded/06-aaic-review | [在新的研发模式下，如何看懂AI写的技术方案？](uploaded/06-aaic-review/README.md) | 完整 PDF 已保存 |
| domestic/alibaba | [AI Native 研发范式实践手册](domestic/alibaba/01-ai-native-handbook/README.md) | 完整 PDF 与 OCR 已保存 |
| domestic/alibaba | [在新的研发模式下，如何看懂 AI 写的技术方案？](domestic/alibaba/02-aaic-review/README.md) | 完整 PDF 见上传资料 |
| domestic/alibaba | [多 AI 协同 + SDD 编程实践：一个 AI 全流程交付实录](domestic/alibaba/03-multi-ai-sdd/README.md) | 全文快照已保存 |
| domestic/alibaba | [AI 编码实践：从 Vibe Coding 到 SDD](domestic/alibaba/04-taote-vibe-to-sdd/README.md) | 转载正文已保存；公众号原文无法连接 |
| domestic/bytedance | [洪定坤：AI Coding 的实践与探索](domestic/bytedance/01-ai-coding-force/README.md) | 媒体报道已保存；官方原文无法连接 |
| domestic/bytedance | [Trae Agent: An LLM-based Agent for Software Engineering with Test-time Scaling](domestic/bytedance/02-trae-agent/README.md) | 论文 HTML、官方 README 已保存，PDF 已保存 |
| domestic/bytedance | [Trae Agent 架构演进：从 Workflow 到 Agentic Loop](domestic/bytedance/03-trae-qcon/README.md) | 公开介绍页已保存；非完整演讲实录 |
| domestic/bytedance | [AI Native 应用的新范式，Trae 在 Coding Agent 中的工程实践](domestic/bytedance/04-trae-aicon/README.md) | 公开介绍页已保存；非完整演讲实录 |
| domestic/bytedance | [TRAE 的思考：AI 时代程序员的认知进化](domestic/bytedance/05-cognition/README.md) | 公开介绍与提纲已保存；完整附件未取得 |
| domestic/bytedance | [veCLI：命令行超级智能体的最佳实践](domestic/bytedance/06-vecli/README.md) | 公开介绍与提纲已保存；完整附件未取得 |
| domestic/bytedance | [veRL for Training Coding Agent](domestic/bytedance/07-verl/README.md) | 公开介绍与提纲已保存；完整附件未取得 |
| domestic/tencent | [CodeBuddy AI Coding 企业场景落地实践与思考](domestic/tencent/01-codebuddy-enterprise/README.md) | 正文快照已保存 |
| domestic/tencent | [从 Vibe Coding 到 AI 原生研发团队：一套能落地的工程实践](domestic/tencent/02-ai-native-team/README.md) | 全文快照已保存 |
| domestic/tencent | [AI 研发新范式：基于技术方案全链路生成代码](domestic/tencent/03-spec-to-code/README.md) | 全文快照已保存 |
| domestic/tencent | [从提需求到部署发布，全 AI 全自动化后，研发效能全面跃升](domestic/tencent/04-end-to-end-delivery/README.md) | 全文转载已保存 |
| domestic/tencent | [CodeBuddy Code 2.0 核心团队研发实践报道](domestic/tencent/05-codebuddy-self-development/README.md) | 报道全文已保存 |
| domestic/meituan | [用 Agent 评测思路管理 AI Coding——31 万行代码 AI 重构的实践](domestic/meituan/01-ai-refactoring/README.md) | 全文快照已保存 |
| domestic/meituan | [AI Coding 与单元测试的协同进化：从验证到驱动](domestic/meituan/02-ai-unit-testing/README.md) | 正文与代码案例已保存 |
| domestic/huawei | [华为 AI 软件工程实践：30 年专业经验沉淀打造企业级确定性的高质量软件](domestic/huawei/01-ai-software-engineering/README.md) | 正文快照已保存 |
| domestic/baidu | [文心快码官网与使用手册入口](domestic/baidu/01-comate/README.md) | 入口 HTML 已保存；动态正文未完整取得 |
| pending/01-aliexpress-marketing | [AliExpress 营销系统 AI Coding 实践](pending/01-aliexpress-marketing/README.md) | 摘要已保存；原文跳转需要登录 |
| pending/02-aliexpress-configuration | [AliExpress 详情域 AAIC 配置实践](pending/02-aliexpress-configuration/README.md) | 仅有搜索摘要；正文返回空响应 |
| pending/03-tencent-mobile-development-skill | [从代码生成到需求交付：一个开发 Skill 的工程化实践](pending/03-tencent-mobile-development-skill/README.md) | 第三方概述页已保存；腾讯原文未定位 |
| references/matt-skills | [Matt Pocock Skills 原始文档](references/matt-skills/README.md) | 此前读取的文档已保存 |
| references/domain-skills | [domain-architecture-skills 原始文档](references/domain-skills/README.md) | 此前读取的文档已保存 |
| references/tencent-teamai | [Tencent TeamAI README 快照](references/tencent-teamai/README.md) | 此前读取的 README 已保存 |

## Matt Pocock 原文、访谈与演讲

- [Skills 工作流总览](matt-pocock/01-skills-site/README.md)
- [v1.1：Wayfinder、To Spec、To Tickets 与工作流变更](matt-pocock/02-changelog-v11/README.md)
- [Grill Me / Grill With Docs 常见误用](matt-pocock/03-grill-mistakes/README.md)
- [My grill-me skill has gone viral](matt-pocock/04-grill-origin/README.md)
- [Real-world Feature Build with Claude Code](matt-pocock/05-real-feature/README.md)
- [Wayfinder：跨会话探索与规划](matt-pocock/06-wayfinder/README.md)
- [Prototype：用实验消除不确定性](matt-pocock/07-prototype/README.md)
- [TDD：公开行为与短反馈循环](matt-pocock/08-tdd/README.md)
- [AI Engineer：Software Fundamentals Matter More Than Ever](matt-pocock/09-fundamentals/README.md)
- [AI Engineer：Full Walkthrough — Workflow for AI Coding](matt-pocock/10-workshop/README.md)
- [Latent Space：Wayfinder 访谈](matt-pocock/11-latent-interview/README.md)
- [The Pragmatic Engineer：AI Skills with Matt Pocock](matt-pocock/12-pragmatic-interview/README.md)

## 研究笔记

- [跨 Agent、工程意图优先的 Skills 选型](reviews/Agent-independent-intent-skills.md)

- [现成组件选型与更新方式](reviews/Reusable-components-recommendation.md)

- [分享会话的痛点与当前范围](reviews/Shared-conversation-pain-points.md)

- [Matt Pocock 与 AI SDLC 的关系及版本核对](reviews/Matt-Pocock-AI-SDLC-review.md)

- [AI-SDLC-domestic-research.md](reviews/AI-SDLC-domestic-research.md)
- [AI-SDLC-six-articles-review.md](reviews/AI-SDLC-six-articles-review.md)
- [AI-SDLC-content-review.md](reviews/AI-SDLC-content-review.md)

## 归档边界

HTML 是检索时的网页快照。额外保存了 216 张可公开获取的网页图片，各条目 images.md 可离线浏览。字体、脚本及动态加载资源没有整体镜像，因此离线阅读优先使用 TXT、Markdown、PDF 和图片目录。转载、媒体转述、摘要与完整原文分别标注。微信公众号连接被网络代理拒绝、需要登录的演讲附件和动态页面正文仍有缺失，详情见各条目 README；未将失败响应冒充正文。
