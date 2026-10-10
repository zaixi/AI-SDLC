# 能力接入

在当前表达已选定、确有能力缺口时使用本参考。先找环境已有的工具；专用 skill 可以补足语法或布局指导。加载 skill 是读取指导，不等于启动另一个 agent。

## 选择与可用性

- 用户指定的工具优先。否则，根据当前缺口选择一种合适能力，避免为同一任务先后加载多个完整工作流。
- 使用当前会话公布的名称、位置和调用规则；调用专用 skill 时读取真实 `SKILL.md`，参考文件按当前图种加载。仅允许用户手动调用的 skill 保持手动调用。
- 缺少可选 skill 时，使用已有工具或直接生成。普通解释任务不自动安装新依赖，不更改共享配置。
- 用户明确指定的能力不可用时，如实说明；替代实现不冒充该工具的产出。

## 按缺口接入

| 缺少的能力 | 接入方式 |
|---|---|
| Mermaid 的特定图种语法或配置 | 查询所用版本的资料；可用时按需使用 `mermaid-diagrams` |
| 精确连线、复杂边界、品牌或编辑式排版 | 可用时使用 `diagram-design`，加载当前图种需要的指导 |
| 重复的 HTML 页面布局与组件绘制 | 默认选用 `answer-me-with-html` 随附的 `am` 渲染器，按下面的适用边界接入 |
| 精确数值与坐标映射 | 使用已有的标准绘图库 |

HTML 渲染器需能表达当前内容，例如分支条件、独立实例或统一刻度。组件不匹配时换实现，不能为了填模板改变含义。面板数和布局服从当前问题；不用空面板或重复内容填满页面。

## 默认 HTML 后端

已确定需要 HTML、内容适合现成组件且能力可用时，使用 [answer-me-with-html](https://github.com/QingYunA/answer-me-with-html/tree/main/skills/answer-me-with-html) 的 `am` CLI：模型写扩展 Markdown，渲染器负责页面和图形布局。是否需要 HTML、内容范围和表达深度仍由当前读者问题决定；默认后端不意味着每个解释都生成网页。

- 接入时读取实际 `SKILL.md`，仅查询当前组件的 `am help <component>`。随附 CLI 为 skill 目录内的 `scripts/am.mjs`，按安装版要求使用 Node.js 运行；其他客户端中的未展开路径变量应替换为真实 skill 路径。能力缺失时沿用直接生成的回退方式。
- 流程、结构、时序、关系与内容比较可先检查现成组件是否合适。精确数据图、已有产品 UI、专门交互或独立 SVG，若组件不能忠实表达，直接用合适的绘图库或自定义 HTML/SVG；不要先生成整页再发现组件不适用。`limits` 表示用量与上限，不将各行不同分母的比例条当成绝对数值比较图。
- 保留 Markdown 源和最终 HTML，遵守用户要求的路径、离线条件与样式。若后端的必要流程或模板与当前要求无法兼容，选其他实现；不改写第三方 skill 来掩盖冲突。渲染成功后按 [渲染与交付](rendering.md) 检查实际画面。

## 协作边界

- 沿用已有的读者问题、原始材料、关键约束、图种和交付格式；信息已足够时直接执行所选路径，无需重新询问或重做整套选图规划。
- 遵循所选能力的实际用法。用户要求优先于通用风格建议；若仍无法兼容，回到能满足要求的实现，不通过改写第三方 skill 绕过其流程。
- `diagram-design` 等能力可能有品牌配置流程。已有授权与偏好足够时直接使用；确有必填信息缺失才说明出处并询问，避免虚构偏好或修改共享样式。
- 本 skill 负责语义核对，工具负责其可执行的渲染和结构检查。按 [渲染与交付](rendering.md) 查看最终图形；相同交付版本已完成的有效检查可复用，有关内容变更后再检查受影响部分。

一个能力已完成当前任务即可交付；发现具体缺口时再换工具或增加视图。

## 设计来源

默认表达结构参考 show-me，示例按本 skill 的用途重新编写；语义、渲染和能力接入按需补充。设计来源如下：

- [show-me 评测快照](https://github.com/zaixi/AI-SDLC/blob/main/evaluations/visual-skills/2026-10-10-native-diagram-design/inputs/show-me/SKILL.md)：默认就地解释、代码与组件结构、diff/完整块的选择、说明紧邻视图。
- [visual-explanation 0.4.2 评测快照](https://github.com/zaixi/AI-SDLC/blob/main/evaluations/visual-skills/2026-10-10-native-diagram-design/inputs/v042/SKILL.md)：忠实表达、按需接入、区分实际渲染与语法检查。
- [diagram-design 评测快照](https://github.com/zaixi/AI-SDLC/blob/main/evaluations/visual-skills/2026-10-10-native-diagram-design/inputs/diagram-design/SKILL.md)：先选语义和图种、线路与版面设计。
- [mermaid-diagrams 评测快照](https://github.com/zaixi/AI-SDLC/blob/main/evaluations/visual-skills/2026-10-10-native-diagram-design/inputs/mermaid-diagrams/SKILL.md)：图种语法的按需参考。

这些链接用于追溯设计来源；运行时以实际安装版本为准，不在每次画图时联网下载这些快照。
