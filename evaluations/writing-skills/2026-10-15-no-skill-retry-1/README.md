# 无 skill 基线重试

三题均成功；与上轮四个 skill 合并为十五份输出。

- [结果与判断](report.md)
- [原题](inputs/cases.json)
- [协议与哈希](protocol.json)
- [评审口径](RUBRIC.md)

原始材料：`/home/liyujiang/.codex/skill-evaluations/writing/2026-10-15-no-skill-retry-1/`。未上传公共附件。

继续实验时另建仓库外目录，复制 scripts、inputs 和 protocol.json，保留 parent 指向四组原始结果；不要覆盖已有 runs。准备 review/rubric.md（来自 RUBRIC.md）及上一轮 review/expectations.json 后，先审计和连通检查，再运行正式题：

```sh
python3 scripts/run.py audit --model deepseek-flash
python3 scripts/run.py probe --model deepseek-flash
python3 scripts/run.py run --model deepseek-flash
python3 scripts/prepare_review.py
python3 scripts/combine.py
python3 scripts/gallery.py
```

probe 成功后才运行正式题。依赖 Linux、Python 3（gallery 需要 markdown）、bubblewrap、OpenCode 及宿主现有 llmproxy provider。凭据仅在宿主 relay 内存中使用。该方法复用已有本机原始材料，仓库单独检出不包含历史完整输出；改变条件时需同步修改协议及脚本，并重新审计输入。
