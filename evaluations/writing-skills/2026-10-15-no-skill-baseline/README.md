# 无 skill 基线：服务错误，尚无质量结果

沿用上轮 DeepSeek Flash、OpenCode 1.14.28、原来三道题、reasoning_effort=high、每题一次；不重跑已有四组，不测试新指令。

隔离与实际请求审计通过：模型环境看不到 SKILL.md、全局 skills、仓库、其他组和评审材料；输入目录为空。保留原工具权限及通用请求说明，仅移除技能调用和技能文件位置说明。

C01、C02 已启动，各记录 6 次 HTTP 429，服务端没有返回模型正文。控制器随后停止客户端自动重试和任务调度。E01 尚未启动。本轮没有可评审产物，不据此比较无 skill 与四个 skill 的优劣，也没有改用其他模型替代。

- [协议、源文件哈希及实际状态](protocol.json)
- [原题](inputs/cases.json)
- [上轮四组结果](../2026-10-15-four-skills/report.md)

本机原始错误及隔离记录：`/home/liyujiang/.codex/skill-evaluations/writing/2026-10-15-no-skill-baseline/`。未上传公共附件。错误只记录状态码与类型，没有保存供应商错误正文，因此不能断言是余额、配额或并发限制。

## 恢复方式

待同一服务可用后，在新的尝试目录复制本轮脚本和输入，保留这两份失败轨迹，明确标记为重试。先 audit，再确认服务可用，最后 run。不要直接覆盖 runs/ 下的原始记录，也不要把这次错误计入输出质量得分。

```sh
python3 scripts/run.py audit --model deepseek-flash
python3 scripts/run.py probe --model deepseek-flash
# probe 成功后才运行正式任务
python3 scripts/run.py run --model deepseek-flash
```

脚本需要现有 Linux、Python 3、bubblewrap、OpenCode 和宿主 llmproxy provider。继承上轮基础执行器，原凭据只在宿主 relay 内存读取，不暴露给生成模型。仓库外新目录需保留 protocol.json 中指向上轮原始证据的 parent 路径，才能用 combine.py 生成五组对照页；本轮无产物，尚未生成该页面。
