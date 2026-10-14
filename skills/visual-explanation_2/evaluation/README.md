# visual-explanation 迭代入口

当前冻结版：`visual-explanation_2`（2026-10-14）。仓库中的 [SKILL.md](../SKILL.md) 是维护入口。本机安装副本位于 `/home/liyujiang/.codex/skills/visual-explanation_2/`，本次同步未改动该副本；以后改仓库版本时，安装同步另行处理。

下一次接着做时，先读 [HANDOFF.md](maintenance/2026-10-14-v2-freeze/HANDOFF.md)，需要实测再读 [TESTING.md](maintenance/2026-10-14-v2-freeze/TESTING.md)。不要从历史讨论重新推导目标，也不要默认再跑全部测试。

- [冻结文件与校验值](maintenance/2026-10-14-v2-freeze/manifest.json)
- [可恢复的 skill 快照](maintenance/2026-10-14-v2-freeze/snapshot/visual-explanation_2/SKILL.md)
- [当前版本全部 16 题结果](2026-10-14-grok47-failed-retry-2/all-cases.md) · [产出画廊](2026-10-14-grok47-failed-retry-2/all-cases.html)
- [面向理解效果的评审方法](maintenance/2026-10-14-v2-freeze/RUBRIC.md)
- [创建下一轮隔离测试目录](maintenance/2026-10-14-v2-freeze/prepare_iteration.py)（只准备文件，不调用模型）

历史目录是当时的事实记录。新方法从下一轮开始使用，不覆盖旧报告、不追改旧评分。当前冻结的是图解指令内容；最近提出的两处措辞调整和新增绘图后端均未实施。

本目录自带当前三轮结果、必要脚本和冻结依赖；来源及未搬入的缓存见 [SOURCE.json](SOURCE.json)。更早实验仍在原评测目录，不包含在此包中。
