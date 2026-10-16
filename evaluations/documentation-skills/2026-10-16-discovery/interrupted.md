# 主动发现与维护文档：实测中断记录

2026-10-16。两题 × 三组 × 两轮，计划 12 条真实文件编辑轨迹。**仅 1 条完整结束，其余 11 条因服务额度不足失败或中断，不能作完整组间比较。** 认证有效，重新登录不能解决本次额度问题。

## 测什么

期限变更题只要求把下载可用期限由 7 天改为 24 小时，保留 30 天审计期限，并实施必要验证；未提醒更新文档。旧契约、架构图、ADR 分散在 docs/reference、docs/architecture、docs/decisions 中，README 经 docs/index.md 指向它们。另一题只要求私有求和重构，用于检查是否误改文档。

三组分别为无额外 Skill、在 `.agents/skills/` 安装 Addy 原文但不点名、安装且显式点名。模型 gpt-6.1-sol、medium，独立 Git 仓库和临时 CLI 会话；共享 CLI 内置指令与认证，不是容器级隔离。任务允许真实文件编辑及测试，不给评分标准。详见 [protocol.json](protocol.json)、[cases.json](cases.json) 与运行前固定的 [RUBRIC](RUBRIC.md)。

## 已完成的证据

### 无额外 Skill，期限变更第一轮

完整结束，模型主动修改了代码、测试、下载契约、架构说明及 Mermaid。复查 6 项测试通过，外部独立检查 86,399 / 86,400 / 86,401 秒和 30 天审计期限也通过。

但它把旧 ADR 标题从 `Seven-day artifact retention` 改为 `24-hour artifact retention`，保留 Accepted 状态，并在同一正文混合原理由与新决定，没有新增替代 ADR。因此：

- 主动发现与更新契约、图：通过。
- 期限实现、精确边界、审计期限：通过。
- 按本次判据保留独立历史决定并建立替代关系：未通过。
- 原理由没有完全丢失：正文仍说明原先七天是为减少重复生成请求，不能把该失败描述为历史被全部删除。

### 中断轨迹：只能作局部观察

无额外 Skill 第二轮、仅安装 Addy 第一轮均已产生代码及文档修改，且创建了 `docs/decisions/0002-retention.md`。两者随后额度中断，没有完成报告，不能计入完成样本或稳定成功率。

仅安装 Addy 第一轮有直接读取证据：日志中的 `cat .agents/skills/documentation-and-adrs/SKILL.md` 执行成功（退出码 0），事前没有在任务中点名它。因此本次有一次“未点名也被读取”的观察，不代表跨客户端触发率或完成质量。

## 阻塞与结论

模型服务明确返回 `You've hit your usage limit`。原始运行器将剩余作业继续提交，均失败；已保留全部失败记录，并为可复用脚本补充额度错误后停止后续作业的逻辑。该修正只做语法检查，未因额度问题再次实测，不改变已发生的运行结果。

当前能确认：无额外 Skill 的模型也可能主动更新文档，但历史决定的处理方式存在一次不符合预期的结果；Addy 在原生安装路径中至少有一次被主动读取。**无法判断 Addy 是否提高同步完整性，也无法宣称文档漂移已解决。** 暂不采用新 Skill。

模型生成日志、真实仓库及 diff 位于 `/tmp/doc-discovery-20261016/`，未发布持久附件。仓库保存方法、fixture、简要结果和哈希；不能将 /tmp 声称为长期归档。

## 继续运行

需要当前账号的 Codex 使用额度恢复。额度恢复后，在新的仓库外目录运行失败的 11 条轨迹，不覆盖本轮产物，也不重跑已完成样本来择优。额度中断轨迹重新从初始 fixture 开始；报告分别记录尝试次数与有效完成数。

```bash
python scripts/run.py --output /tmp/doc-discovery-retry --skill /path/to/pinned/SKILL.md --only \
  01-retention-change-baseline-2 \
  01-retention-change-discoverable-1 01-retention-change-discoverable-2 \
  01-retention-change-explicit-1 01-retention-change-explicit-2 \
  02-private-refactor-baseline-1 02-private-refactor-baseline-2 \
  02-private-refactor-discoverable-1 02-private-refactor-discoverable-2 \
  02-private-refactor-explicit-1 02-private-refactor-explicit-2
```

Skill 来源与校验哈希沿用[上一轮来源](../2026-10-16-addy/source.json)。脚本自动校验 Skill 哈希。当前只测试 Addy 与无额外 Skill，不是 Matt 完整工作流对照。
