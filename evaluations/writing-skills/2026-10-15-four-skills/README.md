# 四个写作 Skill：单轮实测

已完成：OpenCode 1.14.28 + DeepSeek Flash，3 题 × 4 组，每组一次。11 组正常 CLI 回复，1 组服务端完成但 CLI 漏记；内容从原始响应恢复，未重新生成。

- [结论、具体问题和运行数据](report.md)
- [原始输出对照页（本机）](/home/liyujiang/.codex/skill-evaluations/writing/2026-10-15-four-skills/gallery.html)
- [原题](inputs/cases.json) · [协议与固定依赖](protocol.json) · [评审口径](RUBRIC.md)

原始依赖、逐请求日志、模型文件和对照页位于 `/home/liyujiang/.codex/skill-evaluations/writing/2026-10-15-four-skills`。该目录为本机持久记录，尚未上传公开附件；仓库只保存轻量报告和复用方法。

## 复现边界

在新的仓库外目录复制 scripts/、inputs/、protocol.json。`fetch_skills.py` 优先按协议内固定提交下载文件，不安装到全局。运行环境需 Linux、Python 3、bubblewrap、OpenCode，以及当前账户已配置的 `llmproxy` provider。生成进程仅看到占位凭据；实际 API 凭据留在宿主 relay 内存，不写入日志。

```sh
python3 scripts/fetch_skills.py
python3 scripts/run.py audit --model deepseek-flash
python3 scripts/run.py probe --model deepseek-flash
# 确认 probe 有正常输出后，以下命令会调用模型产生新的付费运行。
python3 scripts/run.py run --model deepseek-flash
python3 scripts/prepare_review.py
python3 scripts/gallery.py
```

`gallery.py` 需要 Python markdown 包；原始生成不需要此包。脚本拒绝覆盖已存在的运行目录，不自动重试。需要换模型或题目时更新新一轮协议，不修改本轮记录。服务端输出恢复与 CLI 原始记录分开保存。

正式评审读取原题、回答及 RUBRIC.md。参考文件和原始输出不能和题目一起挂给其他组。是否增加无 skill 基线、次数或独立评审，按下一轮用户授权决定。
