# 写作 Skill：五道扩展题

比较无 skill、writing-clearly-and-concisely、humanizer、i-have-adhd。每题每组一次，共 20 个独立会话；排除 asd-ste100。沿用上一轮固定 skill 提交、OpenCode 1.14.28、deepseek-flash 和隔离设置。

- [结果与判断](report.md)
- [原题](inputs/cases.json)
- [运行前固定的评审要点](RUBRIC.md)
- [协议与来源哈希](protocol.json)

原始材料位于 `/home/liyujiang/.codex/skill-evaluations/writing/2026-10-15-expanded-cases/`；仓库只保存方法和报告，未上传公共附件。

## 复现

新建仓库外实验目录，复制 scripts、inputs 和协议，建立 review 目录；按 protocol.json 中固定提交准备 snapshots/clear、snapshots/humanizer、snapshots/adhd，并核对文件哈希。无 skill 组不装任何 skill。不要覆写已有 runs。保存新的协议和日期，再执行：

```sh
python3 scripts/run.py audit --model deepseek-flash
python3 scripts/run.py probe --model deepseek-flash
# 连通检查成功后再运行正式题
python3 scripts/run.py run --model deepseek-flash
python3 scripts/prepare_review.py
python3 scripts/gallery.py
```

依赖 Linux、Python 3（gallery 需 markdown）、bubblewrap、OpenCode 及宿主现有 llmproxy provider。脚本中的 OpenCode 路径需要与本机一致；凭据在宿主 relay 内存中使用，不给生成模型。单会话 300 秒、16 次模型请求、32768 输出 token 上限，并发 2；服务传输重试保留在同一次尝试内，禁止静默重跑或切换模型。
