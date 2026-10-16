# Ponytail 对现有全局规则的增量效果

比较现有全局 AGENTS.md，与相同规则加 Ponytail full 原文。每个 case 每组一次，OpenCode + deepseek-flash/high。使用五个已有可运行的合成 Python 用例；两组重新生成，无历史答案输入。

全局规则仅将两个表达 skill 的绝对链接改为隔离容器路径，内容和支持文件两组一致。本轮不加载 AI-SDLC 项目规则或 search-before-build。Ponytail 明确调用，未安装到全局，未测试插件 hook 和自动触发。

来源提交、预算、输入哈希、原始目录见 [protocol.json](protocol.json)。题目见 [inputs/cases.json](inputs/cases.json)，评审标准见 [RUBRIC.md](RUBRIC.md)。独立检查与历史输出不向生成会话开放。完整请求、响应、产物在仓库外。

复跑需要现有 OpenCode、bwrap、Python 3.11 和本机已有 llmproxy provider 配置；凭据由宿主中继使用，不交给容器或写入报告。运行命令（目标必须不存在）：

```bash
python scripts/prepare.py /absolute/path/to/fresh-evaluation
python /absolute/path/to/fresh-evaluation/scripts/run.py audit
python /absolute/path/to/fresh-evaluation/scripts/run.py run
python /absolute/path/to/fresh-evaluation/scripts/verify.py
```

脚本每题每组一次，跳过已有运行目录，不自动重试。核实 events.jsonl 中实际读取规则和 Ponytail，复查测试失败与最终代码，不能仅凭退出码认定完成。评审非盲评，单次小样本只能作为是否继续测试的依据。

实测结论见 [report.md](report.md)，逐次指标见 [metrics.json](metrics.json)。追加诊断和统计可运行 `scripts/probe_precision.py`、`scripts/summarize_results.py`（在新评测副本执行）。
