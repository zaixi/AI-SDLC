# 评测报告与原始材料

本目录保存轻量报告、索引，以及可复用的测试方法、案例、协议和脚本。2026-10-15 清理前约 143 MB（恢复可复用测试资产后约 4 MB），主要是重复请求 JSON、截图、依赖副本与运行日志；这些内容已移出当前版本，原始证据仍完整保存在固定提交中。

- [文档主动维护：三组 12 条完成，ADR 处理出现小样本差异](documentation-skills/2026-10-16-discovery/report.md)
- [Addy 文档维护：三题两组各两轮，未观察到额外收益](documentation-skills/2026-10-16-addy/report.md)
- [如何继续测试：方法、案例与运行边界](TESTING.md)
- [范围控制研究索引与最终决定](scope-skills/README.md)
- [Design scope 单段删除对照：三题实际实现](scope-skills/2026-10-15-design-scope-ablation/report.md)
- [范围控制：原版与修订版 AGENTS.md，两题实际实现](scope-skills/2026-10-15-execution/report.md)
- [search-before-build 再次修订：五题单次实测](reuse-skills/2026-10-15-search-before-build-refined/report.md)
- [search-first 与修改版 search-before-build：五题重新对照](reuse-skills/2026-10-15-search-before-build/report.md)
- [复用与选型 Skill：三个 Skill × 两个真实架构问题](reuse-skills/2026-10-15-real-architecture/report.md)
- [复用 Skill：search-first 与 reuse-before-build，三题实测](reuse-skills/2026-10-15-two-skills/report.md)
- [写作 Skill 扩展题：五题 × 四组，全部完成](writing-skills/2026-10-15-expanded-cases/report.md)
- [写作五组比较：无 skill 基线重试成功](writing-skills/2026-10-15-no-skill-retry-1/report.md)
- [写作无 skill 基线尝试：HTTP 429，无质量结果](writing-skills/2026-10-15-no-skill-baseline/README.md)
- [四个写作 Skill 实测：信息密度与重复](writing-skills/2026-10-15-four-skills/report.md)
- [视觉 Skill 评测索引](visual-skills/README.md)
- [全部原始评测目录（固定版本）](https://github.com/zaixi/AI-SDLC/tree/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations)
- [下载原始版本 ZIP](https://github.com/zaixi/AI-SDLC/archive/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475.zip)：包含当时整个仓库，解压后取 evaluations/；不是仅评测目录的下载。
- [归档索引](archive-index.json)：来源提交、本地完整压缩备份的 SHA-256，以及保留报告在清理前的哈希。

保留报告的正文不改写，指向已移出文件的 Markdown 链接改为固定提交链接。历史报告描述的是当时状态，历史脚本、本机路径、归档结构和验证结果不代表当前文件布局。报告中的原始相对链接版本仍在上述固定提交中。

## 后续评测如何保存

仓库提交每轮报告及必要的测试方法、案例、协议、脚本和依赖锁文件。原始输入输出、可运行交付、图片、日志与依赖放在仓库外，例如 /tmp/ai-sdlc-evaluations/；需要长期共享时上传到可用的附件存储，在报告中记录地址、来源版本与 SHA-256。确认附件可下载后再声明已归档。不要提交逐请求完整上下文、依赖目录或打包副本。

根目录 .gitignore 对评测区实行轻量资产白名单。新增报告提交前检查暂存区体积；其他小型必要材料经判断后再有意识地调整规则。

## 减少 Git 下载量

删除当前文件不会删除旧 Git 对象。已经拥有旧版本的正常更新会删除这些文件，但不会自动收回 .git 的历史空间；首次完整克隆或跨越旧提交的完整拉取仍可能下载历史大文件。

只需要当前版本时，另建浅克隆即可避开旧历史：

```bash
git clone --depth 1 --single-branch --no-tags https://github.com/zaixi/AI-SDLC.git AI-SDLC-light
```

如果只使用 Skill，不需要资料库，可在服务端支持部分克隆时进一步只检出所需目录：

```bash
git clone --depth 1 --single-branch --no-tags --filter=blob:none --sparse https://github.com/zaixi/AI-SDLC.git AI-SDLC-skills
cd AI-SDLC-skills
git sparse-checkout set skills scripts
```

materials/ 仍含约 107 MB 的参考资料，不在这次清理范围内。浅克隆整个工作区仍会下载这些当前文件；稀疏部分克隆可以避开它们。不支持过滤的服务端可能仍下载全部当前文件。

本次没有重写公共 Git 历史或强推。彻底清除历史对象需要另行规划历史迁移，并同步处理协作者克隆和固定版本归档；不能把本次文件清理说成已缩减完整历史。

- [2026-10-16：visual-explanation、Archify、Fireworks 实测](visual-skills/2026-10-16-specialist-tools/report.md)：两个用例，每组一次；保留预算截断、局部产物与完整交付的区别，未更改正式 Skill。

- [2026-10-16 图解工具扩展评测](visual-skills/2026-10-16-specialist-tools-expanded/README.md)：4 题 × 3 组，预算加倍，剔除维护说明；逐题区分交付、含义、可读性与消耗。
