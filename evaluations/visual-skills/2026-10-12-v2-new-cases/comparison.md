# 内层新版与 0.4.2：新案例实测

**内层新版在本轮流程题中更紧凑，数值题与 0.4.2 基本相当；没有显示明确的整体正确性或最终检查优势。**

流程题：新版两张图加组件表，0.4.2 三张图；同等关键内容保留，新版图源码760字符，0.4.2为1408字符。新版采用宽幅布局，1600 px截图文字相对较小，紧凑不代表所有阅读尺寸更好。两版最后反馈后仍改图，都如实标明新稿未检查，评审另看最终图。

数值题：两版都正确使用共同零基线和绝对延迟，三个不同验收上限作为独立标记；不虚构误差或统计显著性。单图和移动端正文清楚，复杂图采用局部横向滚动。新版HTML源码4930字符，0.4.2为4234字符；本轮三次调用输出token分别11576和11370，差别很小。

这两题支持保留新版的简洁组织方式作为候选，但不足以宣布全面替换。**am及其他扩展均未安装，结果不支持其默认后端选择。** 本轮没有修改任何Skill规则。


每版两题、四条独立容器/会话轨迹，每条两次真实桌面图片反馈。相同模型；流程题允许 Mermaid/HTML，数值题按任务要求用离线 HTML/SVG。可选扩展均不可用，测试回退路径。详见 [协议与限制](README.md)。

## 产出规模

| 题目 | Skill | 最终图数 | 原生格式 | 图源码字符 | 全部代码块字符 | 三次调用输出 tokens | 最后反馈后仍改图 |
|---|---|---:|---|---:|---:|---:|---|
| 01-export | visual-explanation 0.4.2 | 3 | Mermaid | 1,408 | 1,408 | 6,184 | 是，最终画面由评审查看 |
| 01-export | 内层新版 | 2 | Mermaid | 760 | 760 | 5,369 | 是，最终画面由评审查看 |
| 02-latency | visual-explanation 0.4.2 | 1 | HTML/SVG | 4,234 | 4,234 | 11,370 | 否，模型已收到相同图源码的画面 |
| 02-latency | 内层新版 | 1 | HTML/SVG | 4,930 | 4,930 | 11,576 | 否，模型已收到相同图源码的画面 |

图数按实际主 SVG/Mermaid 图计数，一份 HTML 可能含多图；伪代码不计作图片，但计入全部代码块。HTML 包含页面样式、文字与表格，Mermaid 源不含外围 Markdown，因此源码字符只反映各自交付物规模。token 是本轮 CLI 用量，含修订，不代表价格或正常按需读取的最低消耗。未测真实需求变更工时。

## 分页导出：状态、授权与去重

本题新版用更少图完成同等内容表达，布局更紧凑；0.4.2 纵向图字号更大、阅读路径更长。两版都在最后反馈后改图并如实标明，未显示新版在检查闭环上的优势。

### visual-explanation 0.4.2

[最终原始回答](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/outputs/v042/01-export.md) · [初稿](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/01-export/stage0/answer.md) · [第一次修订](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/01-export/stage1/answer.md) · [最终阶段](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/01-export/stage2/answer.md)

**内容：** 六种明确任务状态、批准资格、拒绝回草稿、仅可执行可撤销、启动先改状态、逐页推进、按页去重、失败停止且不删除已导出页，以及六条组件交互均保留。

**忠实性：** 没有补设撤销后状态、鉴权位置、标识传递、事务、队列、数据库、重试或恢复机制。

**实际画面：** 三张 Mermaid 图：任务状态、分页处理、组件协作。文字清楚，但状态与分页图均偏高；循环返回线路不遮挡节点。

**检查闭环：** 最后一轮修改分页图两个节点文案，明确说明新文案尚未渲染检查。评审已独立查看最终图；其他两图保持已反馈源。

![visual-explanation 0.4.2 01-export 图 1](https://raw.githubusercontent.com/zaixi/AI-SDLC/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/01-export/rendered/stage2-1.png)

[可编辑 Mermaid](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/01-export/render-inputs/stage2-1.mmd) · [SVG](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/01-export/rendered/stage2-1.svg)

![visual-explanation 0.4.2 01-export 图 2](https://raw.githubusercontent.com/zaixi/AI-SDLC/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/01-export/rendered/stage2-2.png)

[可编辑 Mermaid](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/01-export/render-inputs/stage2-2.mmd) · [SVG](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/01-export/rendered/stage2-2.svg)

![visual-explanation 0.4.2 01-export 图 3](https://raw.githubusercontent.com/zaixi/AI-SDLC/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/01-export/rendered/stage2-3.png)

[可编辑 Mermaid](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/01-export/render-inputs/stage2-3.mmd) · [SVG](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/01-export/rendered/stage2-3.svg)

<details>
<summary>查看初稿实际画面</summary>

![初稿 visual-explanation 0.4.2](https://raw.githubusercontent.com/zaixi/AI-SDLC/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/01-export/rendered/stage0-1.png)

![初稿 visual-explanation 0.4.2](https://raw.githubusercontent.com/zaixi/AI-SDLC/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/01-export/rendered/stage0-2.png)

![初稿 visual-explanation 0.4.2](https://raw.githubusercontent.com/zaixi/AI-SDLC/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/01-export/rendered/stage0-3.png)

</details>

### 内层新版

[最终原始回答](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/outputs/candidate/01-export.md) · [初稿](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/01-export/stage0/answer.md) · [第一次修订](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/01-export/stage1/answer.md) · [最终阶段](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/01-export/stage2/answer.md)

**内容：** 同样关键规则和交互保留，用两张 Mermaid 图加组件表；撤销操作明确连到未提供状态的说明框，正文区分它与新增状态。

**忠实性：** 禁自授权、拒绝返回、分页循环与去重均准确；未补设实现机制。

**实际画面：** 最终横向状态图与分页图更紧凑，表格代替组件图。1600 px 截图中文字也较小，因此不能只按面积认定所有阅读场景更好；适合宽幅查看。

**检查闭环：** 最后一轮再次改状态图方向，模型说明新布局尚未检查；分页图保持已反馈版本。评审已查看最终布局。

![内层新版 01-export 图 1](https://raw.githubusercontent.com/zaixi/AI-SDLC/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/01-export/rendered/stage2-1.png)

[可编辑 Mermaid](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/01-export/render-inputs/stage2-1.mmd) · [SVG](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/01-export/rendered/stage2-1.svg)

![内层新版 01-export 图 2](https://raw.githubusercontent.com/zaixi/AI-SDLC/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/01-export/rendered/stage2-2.png)

[可编辑 Mermaid](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/01-export/render-inputs/stage2-2.mmd) · [SVG](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/01-export/rendered/stage2-2.svg)

<details>
<summary>查看初稿实际画面</summary>

![初稿 内层新版](https://raw.githubusercontent.com/zaixi/AI-SDLC/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/01-export/rendered/stage0-1.png)

![初稿 内层新版](https://raw.githubusercontent.com/zaixi/AI-SDLC/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/01-export/rendered/stage0-2.png)

</details>

## P95 延迟：共同尺度与验收上限

两版图的数值、共同尺度和上限标记均正确，最终图面清楚，没有显示新版的明确正确性或画质优势。新版移动端多一句滑动提示，0.4.2源码更短。

### visual-explanation 0.4.2

[最终原始回答](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/outputs/v042/02-latency.md) · [初稿](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/02-latency/stage0/answer.md) · [第一次修订](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/02-latency/stage1/answer.md) · [最终阶段](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/02-latency/stage2/answer.md)

**内容：** 相同四个原值、单位与三个上限完整，无旧版上限、误差线或额外趋势。

**忠实性：** SVG 基线x=180，比例14 px/ms；条宽252/350/168/420正确对应18/25/12/30，上限x460/740/390正确对应20/40/15。共同0–40 ms轴，未画达标百分比。结论不声称统计显著性。

**实际画面：** 单个880×420图，值标在条外，限额标记在条上方以免贴近数值标签。桌面清楚。移动端336 px局部容器承载740 px图，横向滚动；正文可读，但没有新版的可见滑动提示。

**检查闭环：** 最终图源与已回传stage1相同；模型明确未收到窄屏验证。评审已查看移动截图。自检通过；几何脚本不作为刻度验证。

![visual-explanation 0.4.2 02-latency 图 1](https://raw.githubusercontent.com/zaixi/AI-SDLC/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/02-latency/rendered/stage1-1-svg1.png)

[可编辑 HTML](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/02-latency/render-inputs/stage1-1.html) · [完整桌面页](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/02-latency/rendered/stage1-1-desktop.png) · [移动截图](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/02-latency/rendered/stage1-1-mobile.png)

GitHub 不直接执行 HTML；下载 HTML 后用浏览器打开即可查看原生页面。

<details>
<summary>查看初稿实际画面</summary>

![初稿 visual-explanation 0.4.2](https://raw.githubusercontent.com/zaixi/AI-SDLC/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/v042/02-latency/rendered/stage0-1-svg1.png)

</details>

### 内层新版

[最终原始回答](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/outputs/candidate/02-latency.md) · [初稿](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/02-latency/stage0/answer.md) · [第一次修订](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/02-latency/stage1/answer.md) · [最终阶段](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/02-latency/stage2/answer.md)

**内容：** 甲18、乙25、丙12、旧版30 ms 四个值与三个独立上限20/40/15 ms完整。没有虚构旧版上限、样本、误差线或趋势。

**忠实性：** SVG 共同基线 x=140，比例13 px/ms；四条宽234/325/156/390正确对应18/25/12/30，上限刻线x400/660/335对应20/40/15。共用0–40 ms尺度，没有按各自达标比例画条形。结论限定本次汇总值，不声称显著性。

**实际画面：** 单个800×400图，值标在条内，限额为独立竖刻线；标签清楚无明显重叠。移动端390 px正文正常排版，334 px局部容器承载720 px图并横向滚动，有可见滑动提示。不是图形重排。

**检查闭环：** 最终源码与已回传stage1相同；模型明确说没有看过窄屏，评审已查看移动截图。自检通过；没有箭头的图不以几何脚本证明数值比例。

![内层新版 02-latency 图 1](https://raw.githubusercontent.com/zaixi/AI-SDLC/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/02-latency/rendered/stage1-1-svg1.png)

[可编辑 HTML](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/02-latency/render-inputs/stage1-1.html) · [完整桌面页](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/02-latency/rendered/stage1-1-desktop.png) · [移动截图](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/02-latency/rendered/stage1-1-mobile.png)

GitHub 不直接执行 HTML；下载 HTML 后用浏览器打开即可查看原生页面。

<details>
<summary>查看初稿实际画面</summary>

![初稿 内层新版](https://raw.githubusercontent.com/zaixi/AI-SDLC/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/trajectories/candidate/02-latency/rendered/stage0-1-svg1.png)

</details>

## 证据与限制

四条轨迹独立容器、独立会话、无其他组输出挂载；各阶段实际模型与源码哈希见 [runs.json](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/runs.json)。生成不调用工具，渲染由控制器完成，不测客户端自动加载。每题每组一个样本，主 Agent 知道组别后评审；不能据此宣布普遍排名。

[内容评审](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/content-review.json) · [用量与修订规模](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/metrics.json) · [Mermaid 语法检查](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/syntax-results.json) · [输入及输出完整性](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/integrity-results.json)

本轮没有测试 am、diagram-design 或 mermaid-diagrams 的原生接入；不用未加载的工具为输出背书。数值图的几何脚本没有连线可查，不用于证明刻度正确；刻度和比例由评审对照数据及 SVG 源核对。
