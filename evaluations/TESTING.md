# 如何继续测试视觉 Skill

本文件说明当前保留的测试资产及使用边界，不属于提供给生成模型的 Skill 指令。本次恢复没有调用模型，也没有产生新质量结论。

## 选择方法与案例

- [最近三例的方法与限制](visual-skills/2026-10-15-v2-expanded/README.md)：缺失趋势、独立实例、局部 SVG 修改；[原题](visual-skills/2026-10-15-v2-expanded/inputs/prompts.json)、[协议](visual-skills/2026-10-15-v2-expanded/protocol.json)、[运行脚本](visual-skills/2026-10-15-v2-expanded/scripts/run.py)。
- [前两例](visual-skills/2026-10-14-v2-v042/README.md)：去重计数与复杂平台总览；同目录 inputs/prompts.json、protocol.json 和 scripts/ 保留。
- [16 题库](visual-skills/history/visual-explanation_2/evaluation/2026-10-14-grok47-simplified-once/inputs/cases.json)、[原评分规则](visual-skills/history/visual-explanation_2/evaluation/maintenance/2026-10-14-v2-freeze/RUBRIC.md)、[原操作方法](visual-skills/history/visual-explanation_2/evaluation/maintenance/2026-10-14-v2-freeze/TESTING.md)。这些文档中的模型、预算、冻结名称是历史设置，以本轮用户要求为准。
- [恢复清单与原始哈希](restored-methods.json)：按来源版本逐字恢复的脚本、协议、输入、fixture、轻量版本快照和维护文档。

每组通常选择 2–3 个案例，不默认做十次重复。比较对象、模型、反馈次数和预算需一致；不同任务不能当作同题重复样本合并胜率。

## 准备与运行

历史脚本是保留的方法实现，**不是统一、可直接执行的测试命令**。不同轮次使用不同执行器；运行前阅读脚本及协议。不要直接执行旧 run.py 覆盖旧路径，也不要把所有输入目录、评审文档或历史答案一起挂给模型。

1. 在仓库外新建唯一工作目录，例如 `/tmp/ai-sdlc-evaluations/<新轮次>/`。复制选用轮次的脚本、案例与必要 fixture；报告保存在仓库内新的日期目录。需要长期保留的产物应在完成后转存到持久附件存储，/tmp 不是长期归档。
2. 检查脚本的 REPO、BASE、SOURCE、CLI、TOOLS、镜像、登录卷和临时文件路径。改动只在新工作副本中进行；输出路径全部指向本轮外部目录，运行记录以新空列表初始化，不读取历史 runs.json。明确模型名、推理预算、版本与次数，记录新协议。
3. 依协议准备 Docker、Codex CLI 或 OpenCode、Node、浏览器、Mermaid 和认证。scripts/ 中保留了可用的 package/lock 文件及渲染 Dockerfile；依赖包与镜像本身没有提交。登录文件和密钥不能写入报告或 Git。
4. 当前比较使用 skills/visual-explanation/ 的运行文件；比较历史版本时使用对应轻量输入快照。只给每个生成会话自己的任务、Skill 与必要 fixture，隔离其他组、旧回答、维护资料、评分规则和凭据。渲染与模型认证分离。
5. 先用 fixture 验证渲染器能工作，再开始模型请求。只有本轮实际采用同等图片反馈时才计为该协议；初稿和两轮修改属于一条轨迹，不是三个独立样本。失败保留，不自动无限重试。
6. 按协议实际渲染最终产物，核对关系、计数、未知项、数据和编辑边界，分别报告内容质量、交付覆盖与成本。语法成功不等于读者理解，也不等于 Skill 在客户端原生自动发现成功。

部分脚本依赖已归档的大型后端快照、judge 模板、manifest 或工具文件。完整复现原环境时，在仓库外恢复来源版本，按原目录结构使用：

```bash
# 在 AI-SDLC 仓库根目录执行；不是新评测，也不会运行模型。
# 目标目录应为新建且为空的目录。
mkdir /tmp/ai-sdlc-evaluation-source-b52aa15
git archive b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475 evaluations \
  | tar -x -C /tmp/ai-sdlc-evaluation-source-b52aa15
```

浅克隆可能没有该提交，可先 `git fetch origin b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475`，或按 [存储说明](README.md) 下载原版本 ZIP。该操作会下载历史资料，仅在确实需要原环境时执行。恢复目录含旧输出，仍须另建新运行目录并严格筛选生成输入。旧 prepare_iteration.py 的默认冻结快照和 dependencies/judge 模板需要完整来源目录；它不是精简仓库中的独立入口。

## 保存和验证范围

当前 Git 保留轻量方法、案例、协议、脚本和报告。请求/响应日志、截图、生成页面、渲染输出、依赖安装目录和完整第三方发行版继续在仓库外保存；报告记录来源哈希和可下载归档位置。不要为了让旧脚本路径存在而把这些大目录重新提交。

恢复检查包括文件与来源版本逐字一致、JSON 可解析、Python 语法可解析，以及正式 Skill 包结构校验。它们不证明历史脚本能在当前机器直接运行，不代替环境准备、实际模型生成与质量评审。
