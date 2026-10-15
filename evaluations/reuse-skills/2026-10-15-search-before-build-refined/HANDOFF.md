# 冻结版本与下一轮入口

冻结日期：2026-10-15。Skill 位于 `skills/search-before-build/`，与本文件同次提交。SKILL.md 的 SHA-256 为 `9457e217e27d7cb37c2b7978ba834fecddc5a4c2e21dca31aadd60b56d5f7ad1`；完整包哈希见 protocol.json。冻结仅表示保留此版本供使用和比较，不表示已证明优于原版或无 Skill。

## 已完成与结论

- 五题各一次，OpenCode 1.14.28 + deepseek-flash/high；五题交付，两道实现题独立行为检查通过。
- 相比上一轮修改版：总输出 token 少约 6.7%，三份设计更短；附件题收束改善，执行器题成本增加。
- 主动发现保留，缓存更新、单附件校验与候选能力判断仍有错误。当前不继续加规则。
- 本轮与上一轮是历史比较，非同期对照；用过的题属于回归集，不能证明泛化提升。

## 下次如何继续

1. 从 Git 保留此次 Skill 包作为冻结对照，在新目录准备候选，避免覆盖基线。
2. 优先选未参与本次修订的真实任务；旧五题留作回归。若换模型，重新运行需要比较的条件，勿与旧模型成本直接相减。
3. 沿用 README 的隔离和预算，每题每条件先跑一次。预先确定比较范围与判据，运行中不修改候选、不挑选重试结果。
4. 将轻量方法、输入、协议、脚本、结果摘要与报告入 Git。完整请求、产出和日志在仓库外；公共归档需要单独处理。

## 从本次 Git 提交恢复当前冻结包

先用 `git log --oneline -- skills/search-before-build` 找到冻结提交，将其 SHA 保存为 `FREEZE_COMMIT`。在新的评测目录（下方用 `$EVAL_ROOT` 表示）恢复包，不需要访问本机旧快照：

```bash
mkdir -p "$EVAL_ROOT/snapshots" "$EVAL_ROOT/review"
git archive "$FREEZE_COMMIT" skills/search-before-build | tar -x -C "$EVAL_ROOT"
mv "$EVAL_ROOT/skills/search-before-build" "$EVAL_ROOT/snapshots/"
sha256sum "$EVAL_ROOT/snapshots/search-before-build/SKILL.md"
```

把本目录的 scripts/ 和 inputs/ 复制到 `$EVAL_ROOT`，按 README 运行。Linux、bwrap、Node、Python 和 OpenCode 是前提；脚本中的 OpenCode 路径与 provider 配置需要按机器适配。不要打印 provider 凭据。

上一轮两个条件的原始快照及本轮完整输出尚只保存在 protocol.json 指向的本机目录。仓库中的方法足以恢复当前冻结包并新跑五题，但不能在缺少那些原始材料时重新生成历史对照页；此时跳过 gallery.py，或调整它只展示新跑结果。
