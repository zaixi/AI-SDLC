# 方案设计中的范围控制 Skill 对照

比较无 skill、boring-engineering、microsoft/agentic-loops 的 yagni、karpathy-guidelines；随后补测现有 `~/.codex/AGENTS.md`。

- [题目](inputs/cases.json)：CSV 导出、账单导入可靠性、第三方存储 SDK。
- [评分规则](RUBRIC.md)：范围克制与需求完整分别评判，生成前固定。
- [实测报告](report.md)：15 份正式回答的逐题证据、篇幅和限制。
- [协议及来源版本](protocol.json)：模型、预算、各 skill 的固定提交及文件哈希。
- [运行脚本](scripts/run.py)：标准库 Python，通过已有 OpenCode provider 发起独立模型请求。
- [AGENTS.md 补测协议](global-agents/protocol.json)与[补测脚本](scripts/run_agents.py)：保留原三题及参数，只增加第五组，未叠加其他 skill。

本轮是无工具、单轮的设计文本测试。Skill 主文件和列出的参考文件直接加入请求；不读取宿主全局指令，也不测试客户端自动发现 skill。参考文件提前完整提供，与实际按需读取的行为和 token 开销可能不同。

补测仅将 AGENTS.md 的快照作为第五组输入，使用相同 user-message 包装，不测试 Codex 原生加载机制。`run_agents.py --raw-root <新的外部目录>` 在首次运行时保存快照和补测协议；发现已有补测协议会拒绝覆盖。另开一轮时应复制整个轻量评测目录并移除副本中的 `global-agents/protocol.json`，保留父协议及其哈希对应的脚本、题目和评分规则；不会重跑前四组。

运行需要 Python 3.11、git、已配置 llmproxy provider 的 OpenCode，以及公共网络。认证仅由配置命令在内存中交给请求，不写入产物。脚本不自动重试失败请求。

复测时把 scripts/run.py、inputs/cases.json、RUBRIC.md 复制到新的评测目录；不要复制已有 protocol.json。先执行 `python3 scripts/run.py prepare --raw-root <仓库外新的空目录> --model <模型名>`，然后执行 `python3 scripts/run.py run`。prepare 会解析当时的上游提交，因此这是新版本复测；要复现本轮输入，应使用 protocol.json 中固定的文件 URL 并逐个核对 SHA-256。

原始请求、回答、usage 和 skill 快照位于 protocol.json 的 raw_root。它们保存在本机仓库外，尚未上传为公共附件，Git 中的轻量报告不能替代原始回答。
