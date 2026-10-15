# search-before-build 再次修订实测

沿用[上一轮方法](../2026-10-15-search-before-build/README.md)，仅跑当前修订版，五题各一次。OpenCode 1.14.28 + deepseek-flash/high；600 秒、48 请求、49,152 输出 token/会话，并发 2。未重跑旧版，旧结果仅作历史比较。无无-Skill基线，非盲评；不得把差异直接归因于指令改动。

原始目录：`/home/liyujiang/.codex/skill-evaluations/reuse/2026-10-15-search-before-build-refined-191910`。完整快照、请求、usage、事件、产出与隔离审计仅在本机；尚未公共归档。`gallery.html` 并排展示上轮修改版与本轮修订版，输出已转义，不执行生成内容。

复跑：将 scripts、inputs 与已校验的 snapshots/search-before-build 放到新的仓库外目录，创建 review，然后依次运行 `run.py audit`、`run.py probe --model deepseek-flash`、`run.py run --model deepseek-flash`、`summarize.py`、`verify.py`、`gallery.py`。gallery.py 的历史对照路径需按实际位置调整。环境、provider 私密配置适配与限制沿用上一轮说明。原始请求可能含私有上下文，勿直接发布。

生成前协议与哈希见 protocol.json；gallery 后处理改动另记哈希。隔离输入不含本轮评审、旧答案、宿主全局指令或其他 Skill。R01/R02 独立检查通过；设计题静态核对，没有安装候选、执行 CI 或实际发布。当前 Skill 在本轮期间未修改。
