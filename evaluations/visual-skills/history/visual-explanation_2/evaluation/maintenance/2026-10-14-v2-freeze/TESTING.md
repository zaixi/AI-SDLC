# 继续测试的方法

先读 [HANDOFF.md](HANDOFF.md)。本文件记录评测操作，不是生成模型的绘图规则。冻结版本不要求立即重跑。

## 本轮默认约定

用户最后选定 OpenCode + Grok 4.7 high，只测当前 skill，每个 case 一次。重试需单独记轮次。若要测试其他模型、无 skill 或 show-me，比对范围先按当次用户意图确定；不默认三组或三次重复。

原始题库：[16 个 case](../../2026-10-14-grok47-simplified-once/inputs/cases.json)。A 是局部说明，B 是关系/状态/流程，C 是 HTML/数据/交互，D 是表达边界/复杂文档/局部修改。fixture 在同目录 fixtures/。

当前配置：OpenCode 1.14.28，wire model `grok-4.7`，reasoning_effort `high`，三并发，每题 900 秒、64 次模型请求、131072 输出 token（含推理）上限，单请求 65536。限额是当时实验设置，不是 skill 的运行要求。修改任一参数需要在新 protocol 中记录，避免把模型/预算/依赖变化归因为 skill 改进。

冻结依赖在历史 suite 的 dependencies/ 下，来源和逐文件 hash 见其 manifest.json：am 0.5.1，diagram-design 2.6，mermaid-diagrams 固定提交。优先复用这些本地快照，不自动拉取最新版本。

## 准备下一轮

用当前冻结版作基准时，以下命令只准备文件，不调用模型；把输出目录名换成尚不存在的新轮次。候选版通过 `--skill-dir /path/to/candidate` 显式传入。`--cases all` 选全部 16 题，也可逗号分隔选题。

```bash
python3 evaluation/maintenance/2026-10-14-v2-freeze/prepare_iteration.py \
  --output evaluation/NEXT-ITERATION \
  --cases B03,D03
```

上述准备命令在 skill 仓库目录（包含 SKILL.md 和 evaluation/ 的目录）执行。填写新目录 plan.md 的假设与差异，然后进入该目录。准备器只支持当前自包含的 skill；若候选新增资源，它会停止，需先更新生成白名单。脚本中的条件名和 snapshots/visual-explanation 是旧 harness 槽位，实际 skill 名称与文件 hash 在 manifest 内。不要为了改显示名称而全局替换历史文件。

## 先验证环境，再运行生成

以下命令均在新 suite 根目录执行：

```bash
python3 scripts/run.py audit --label initial-
python3 scripts/verify_environment.py --label initial-
```

audit 使用本地假响应，不访问模型；verify_environment 实际检查隔离文件系统、离线渲染与 am。首次校验记录保留，重复检查使用新 label。确认主机 CPU/可用内存没有明显异常，再执行已授权的模型测试。

环境脚本含本机绝对路径：OpenCode、Node、Python、Chromium、Playwright 与 Mermaid bundle 等在 run.py 和 dependencies/ 中配置。迁移机器先核对这些路径与版本。凭证由原有 OpenCode provider 配置读取，只验证可用性，不打印原始配置或密钥。

```bash
python3 scripts/run_monitored.py run
```

runner 为每题创建独立 home/work/input，用 bwrap 隔离宿主历史和其他 skill；工具网络隔离，API 经固定路径 Unix socket relay。生成模型只看到该题和 fixture、当前 skill、允许的三份专业依赖；看不到 judge、答案、旧结果或本交接目录。若恢复无 skill/show-me 比较，必须额外验证它们看不到专业依赖；当前准备器不创建这两组。

run_monitored.py 每 20 秒记录主机资源。模型配置必须从实际 request 文件确认。遇到连续服务错误且尚无工具执行，可终止无效轮次；记录信号、时刻和原因，不能归类成任务超时或 skill 质量失败。不要悄悄继续重采样。

run.py 会跳过已有 result.json 的题目；这只适合恢复同一轮中尚未启动的题。追加尝试应创建新 suite。异常终止且没有 result.json 时先查原日志，不能把重启当成没有发生过的第一次。

## 生成结束后复核

先确认进程结束，再运行以下命令，避免浏览器评审与生成争抢资源：

```bash
python3 scripts/prepare_review.py
python3 scripts/interaction_checks.py
```

prepare_review 提取原始最终回复、保留残稿，并生成桌面/手机证据；interaction_checks 只处理 C04，依次操作五组参数。控件无法自动识别时先检查原页面，再补 control-map.json，不能修改产物来迁就检查。

检查依据是 [RUBRIC.md](RUBRIC.md)。原题、原产物和 reader probes 优先；自动检查结果只提供证据。脚本中的静态 `finished` 标记或进程退出码 0 均不足以证明完成：看 reply_scope、实际产物和末条服务端响应。已有提取逻辑能恢复服务端正常 stop、CLI 漏记的最终回复，必须保留这一来源说明。

将逐题理解效果和重要发现写入 review/manual-case-notes.json。如需 gallery 显示评审意见，写入 review/adjudication.json 的 `supplementary_missing_score_checks`，以匿名 sample ID 为 key，每项含 `note`。这是报告脚本沿用的字段名，不要求独立模型评分。

```bash
python3 scripts/report.py
```

该命令生成 gallery.html、review/sample-metrics.json 和 review/summary.json；还需要依据实际结果编写 report.md，并更新 manifest/protocol 的真实完成状态。它不会自动完成质量评审。没有模型打分时 scores/qualified 等历史数值字段不能解释为质量 0 分，以逐题评审为准。

report.py 的 token 总计来自收到的 usage。若 requests_without_usage 非零，报告“已记录下界”；全无 usage 则记未知，不称消耗为零。核对实际 HTTP 请求与 title mock 的区别。失败尝试也计入成本。

## 保存与比较

每轮保留 inputs、snapshots、dependencies manifest、protocol、requests/responses、events、result、原产物和评审证据。手写报告链接到这些证据，标明是否盲评和未验证项；不要把外部评测器的验证说成生成 agent 自己完成的验证。

首轮与补测分开，最新结果可以汇总，但不择优替换旧结果。旧 consolidate.py 专门合并 10-14 的三轮，未复制到新 suite，不能直接复用它作通用汇总。对照版本时同时报告语义/理解效果、交付覆盖和成本；不要仅凭一次耗时差下结论。

完成迭代后更新评测根目录 README 的当前入口，记录采用/未采用的改动及其证据。冻结快照和过去的协议、报告保持原样。
