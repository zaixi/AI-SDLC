# 三种图解方案：现有 visual-explanation、Archify、Fireworks

比较实际完整工具流程，两个已有用例，每题每组一次。原题取自之前评测；V01 增加离线 HTML 交付要求，V02 增加文档 SVG+PNG 交付要求，组间完全相同。题目中的 digitization.md 全文已内联，未单独挂载该路径。

- 当前 visual-explanation 0.5.0，提供过去已固定的 diagram-design、mermaid-diagrams、answer-me-with-html 可选依赖。
- Archify 3.1.0 官方发行 ZIP，固定到提交 `f8021f7eee6870a552bbad3373cf6bad32c80f37`。
- Fireworks 1.2.0，固定提交 `31fea364eda5f1852b1175f3d9e29ea31d22dcb4` 的 nested skill 运行文件、引用、schema、模板和文本/SVG 样例；不包含 docs/tests、演示 PNG/GIF/视频。SVG/PNG/HTML 样例运行成功。GIF 依赖未装，本轮不请求 GIF。

两组新工具安装到隔离评测目录，未全局安装。最初 installer 下载超时，SSH 与 API 路径也未成功；最终 Archify 使用固定版本 raw 官方发行 ZIP，Fireworks 通过固定版本 GitHub 目录和 raw 文件恢复。安装排障不计入模型生成时间。

模型 OpenCode + deepseek-flash/high，仅文本输入。各组同样可以调用浏览器截图/DOM 检查，模型无法看图片，因此不得声称模型视觉检查。最终由主 Agent 统一查看画面并核对原题；没有把评审反馈发回生成会话，也没有为失败组重试。

预算、哈希与完整原始目录见 [protocol.json](protocol.json)，上游及依赖固定来源见 [sources.json](sources.json)，[题目](inputs/cases.json)、[评分依据](RUBRIC.md)。网络与宿主目录隔离，不提供其他组、旧输出、评分材料、全局 AGENTS 或主会话。

## 继续或复跑

原始运行目录：`/home/liyujiang/.codex/skill-evaluations/visual-explanation/2026-10-16-specialist-tools-102457`。大型源码、运行依赖、完整请求/响应、产物和截图保存在这个目录，不进入 Git。

本机复跑（目标目录必须不存在）：

```bash
python scripts/prepare.py /path/to/archived-evaluation /path/to/new-evaluation
python /path/to/new-evaluation/scripts/run.py audit
python /path/to/new-evaluation/scripts/run.py run
python /path/to/new-evaluation/scripts/metrics.py
```

prepare 只恢复 snapshots、specialists、runtime，复制当前方法和题目，不复制历史会话或产物。它先检查源码快照哈希。宿主仍需 OpenCode、既有 llmproxy 配置、bwrap、Node.js 和 Playwright Chromium；具体本机路径在脚本中，换机器时调整并重新做隔离与工具自检。认证仅由宿主中继使用，不进入生成容器。

迁移到别的机器时应另外归档原始目录的 snapshots、specialists、runtime 和渲染证据。sources.json 提供上游定位与文件哈希，但不把只有 Git 文本视作已恢复浏览器及 Python 二进制依赖。

每个运行目录只执行一次，脚本拒绝覆盖并跳过已存在目录。需要新一轮时新建目录，不覆盖旧失败记录。成功退出、schema 通过、浏览器能打开都不等于含义完整或易于理解。

结果见 [report.md](report.md)。完整当前 visual-explanation 包包含维护说明，模型读取过；这是已记录的环境限制，下一轮应在生成前限定允许文件。
