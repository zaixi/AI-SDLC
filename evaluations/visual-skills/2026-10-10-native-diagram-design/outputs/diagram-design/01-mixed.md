保留已看到的三个视图：协作架构、发布状态、批次时序，均为 **1280 × 720**。本次图源码不变；已提供的渲染、自检和几何检查均通过。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>发布体系：协作、状态与审批约束</title>
<style>
*{box-sizing:border-box}
:root{
--paper:#f5f5f5;--ink:#2d3142;--muted:#4f5d75;--soft:#5a6580;
--accent:#bf4520;--link:#2e5aa8;
--sans:'Geist','Noto Sans SC','PingFang SC','Microsoft YaHei',system-ui,sans-serif;
--serif:'Instrument Serif','Noto Serif SC','Songti SC',serif;
--mono:'Geist Mono',ui-monospace,monospace;
}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);line-height:1.65}
main{max-width:1360px;min-width:0;margin:auto;padding:40px}
header{margin-bottom:32px}
h1{font:400 28px/1.3 var(--serif);margin:8px 0 12px}
h2{font-size:20px;font-weight:600;margin:0 0 8px}
p{margin:8px 0;color:var(--muted)}
.eyebrow{font-size:12px;color:var(--soft)}
section{margin:36px 0 48px}
.diagram-container{width:100%;overflow-x:auto}
svg{display:block;width:100%;min-width:1280px}
svg text{font-family:var(--sans);fill:var(--ink)}
.name{font-size:12px;font-weight:600}
.group{font-size:14px;font-weight:600}
.label{font-size:12px;fill:var(--soft)}
.note{font-size:12px;fill:var(--muted)}
.mono{font-family:var(--mono);font-size:9px;fill:var(--soft)}
.box{fill:#fff;stroke:var(--ink);stroke-width:1}
.state{fill:#fff;stroke:var(--ink);stroke-width:1}
.focal{fill:#f0e7e3;stroke:var(--accent);stroke-width:1.2}
.arrow{fill:none;stroke:var(--muted);stroke-width:1.2}
.api-arrow{fill:none;stroke:var(--link);stroke-width:1.2}
.return{stroke-dasharray:5 4}
.mask{fill:var(--paper)}
.rule{stroke:#bfc0c0;stroke-width:1}
table{width:100%;border-collapse:collapse;background:#fff;font-size:14px}
th,td{text-align:left;vertical-align:top;padding:12px 16px;border-bottom:1px solid #dedfe2}
th{font-weight:600;background:#ececec}
.table-wrap{overflow-x:auto}
.constraint{border-left:3px solid var(--accent);padding:8px 16px;margin-top:16px}
footer{border-top:1px solid #bfc0c0;padding-top:16px;font-size:12px;color:var(--soft)}
@media(max-width:600px){main{padding:24px 16px}}
@media print{
.diagram-container{overflow-x:visible}
svg{min-width:0}
main{padding:0}
section{break-inside:avoid}
}
</style>
</head>
<body>
<main>
<header>
<div class="eyebrow">新同事阅读指南 · 已确认的发布体系</div>
<h1>一张发布单，一个固定产物，逐批执行</h1>
<p>先看组件怎样协作，再看发布状态，最后看批次成功、失败和重复结果的处理。</p>
</header>

<section>
<h2>01 · 各部分怎样协作</h2>
<div class="diagram-container">
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="collab-title collab-desc">
<title id="collab-title">发布体系的组件协作</title>
<desc id="collab-desc">门户向发布API提交操作，API记录发布单，调度器读取待执行单并写回状态，工作器执行批次并读取指定产物。</desc>
<defs>
<marker id="c-arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#4f5d75"/></marker>
<marker id="c-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#bf4520"/></marker>
<marker id="c-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#2e5aa8"/></marker>
</defs>
<rect width="1280" height="720" fill="#f5f5f5"/>
<text class="group" x="40" y="84">操作入口 → 发布记录 → 执行编排 → 批次部署</text>
<text class="note" x="40" y="116">API 记录发布单；存储实现未提供，因此不展开数据库或其他基础设施。</text>

<!-- 先绘制连线及其标签，再绘制节点 -->
<path class="api-arrow" d="M240 248 H352" marker-end="url(#c-link)"/>
<rect class="mask" x="244" y="224" width="104" height="16"/>
<text class="label" x="296" y="237" text-anchor="middle">提交／审批／取消</text>

<path class="api-arrow" d="M664 232 H552" marker-end="url(#c-link)"/>
<rect class="mask" x="556" y="208" width="104" height="16"/>
<text class="label" x="608" y="221" text-anchor="middle">读取待执行单</text>

<path class="api-arrow" d="M664 280 H552" marker-end="url(#c-link)"/>
<rect class="mask" x="568" y="288" width="80" height="16"/>
<text class="label" x="608" y="301" text-anchor="middle">写回状态</text>

<path class="arrow" d="M864 232 H976" marker-end="url(#c-arrow)"/>
<rect class="mask" x="880" y="208" width="80" height="16"/>
<text class="label" x="920" y="221" text-anchor="middle">批次任务</text>

<path class="arrow return" d="M976 280 H864" marker-end="url(#c-arrow)"/>
<rect class="mask" x="880" y="288" width="80" height="16"/>
<text class="label" x="920" y="301" text-anchor="middle">批次结果</text>

<path class="arrow" d="M1076 304 V448" marker-end="url(#c-arrow)"/>
<rect class="mask" x="1084" y="364" width="112" height="16"/>
<text class="label" x="1092" y="377">读取指定产物</text>

<rect class="box" x="40" y="208" width="200" height="96" rx="6"/>
<text class="name" x="140" y="246" text-anchor="middle">发布门户</text>
<text class="note" x="140" y="270" text-anchor="middle">发布人／审阅人操作入口</text>

<rect class="mask" x="352" y="208" width="200" height="96" rx="6"/>
<rect class="focal" x="352" y="208" width="200" height="96" rx="6"/>
<text class="name" x="452" y="246" text-anchor="middle">发布 API</text>
<text class="note" x="452" y="270" text-anchor="middle">记录发布单</text>

<rect class="box" x="664" y="208" width="200" height="96" rx="6"/>
<text class="name" x="764" y="246" text-anchor="middle">调度器</text>
<text class="note" x="764" y="270" text-anchor="middle">编排批次、推进执行状态</text>

<rect class="box" x="976" y="208" width="200" height="96" rx="6"/>
<text class="name" x="1076" y="246" text-anchor="middle">部署工作器</text>
<text class="note" x="1076" y="270" text-anchor="middle">部署批次、返回结果</text>

<rect x="976" y="448" width="200" height="96" rx="6" fill="#e9e9ed" stroke="#4f5d75"/>
<text class="name" x="1076" y="486" text-anchor="middle">产物仓库</text>
<text class="note" x="1076" y="510" text-anchor="middle">提供不可变构建产物</text>

<text class="group" x="40" y="456">产物绑定约束</text>
<text class="note" x="40" y="488">每张发布单关联且仅关联一个不可变构建产物。</text>
<text class="note" x="40" y="516">同一产物可被多个发布单使用；工作器读取当前单指定的产物。</text>

<line class="rule" x1="40" y1="660" x2="1240" y2="660"/>
<text class="label" x="40" y="692">蓝色实线：API 交互</text>
<text class="label" x="352" y="692">灰色实线：任务／读取</text>
<text class="label" x="704" y="692">灰色虚线：结果返回</text>
</svg>
</div>
</section>

<section>
<h2>02 · 发布状态怎样演变</h2>
<div class="diagram-container">
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="states-title states-desc">
<title id="states-title">发布单状态与异常分支</title>
<desc id="states-desc">发布单从草稿经待审和待执行进入执行中，拒绝回草稿，待执行可取消，执行失败停止后续批次，全部成功才完成。</desc>
<defs>
<marker id="s-arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#4f5d75"/></marker>
<marker id="s-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#bf4520"/></marker>
<marker id="s-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#2e5aa8"/></marker>
</defs>
<rect width="1280" height="720" fill="#f5f5f5"/>
<text class="group" x="40" y="64">正常推进</text>
<text class="note" x="40" y="96">创建后为草稿。调度器只执行待执行单，派发批次前先进入执行中。</text>

<path class="arrow" d="M200 256 H288" marker-end="url(#s-arrow)"/>
<path class="arrow" d="M448 256 H536" marker-end="url(#s-arrow)"/>
<path class="arrow" d="M696 256 H784" marker-end="url(#s-arrow)"/>
<path class="arrow" d="M944 256 H1072" marker-end="url(#s-arrow)"/>

<rect class="mask" x="212" y="232" width="64" height="16"/>
<text class="label" x="244" y="245" text-anchor="middle">提交</text>
<rect class="mask" x="452" y="232" width="80" height="16"/>
<text class="label" x="492" y="245" text-anchor="middle">审核通过</text>
<rect class="mask" x="704" y="232" width="72" height="16"/>
<text class="label" x="740" y="245" text-anchor="middle">开始执行</text>
<rect class="mask" x="948" y="232" width="120" height="16"/>
<text class="label" x="1008" y="245" text-anchor="middle">全部批次成功</text>

<path class="arrow" d="M368 304 V368 Q368 376 360 376 H128 Q120 376 120 368 V304" marker-end="url(#s-arrow)"/>
<rect class="mask" x="208" y="352" width="72" height="16"/>
<text class="label" x="244" y="365" text-anchor="middle">审核拒绝</text>

<path class="arrow" d="M616 304 V488" marker-end="url(#s-arrow)"/>
<rect class="mask" x="624" y="388" width="104" height="16"/>
<text class="label" x="632" y="401">发布人取消</text>

<path class="arrow" d="M864 304 V488" marker-end="url(#s-arrow)"/>
<rect class="mask" x="872" y="388" width="112" height="16"/>
<text class="label" x="880" y="401">任一批次失败</text>

<rect class="state" x="40" y="208" width="160" height="96" rx="8"/>
<text class="name" x="120" y="246" text-anchor="middle">草稿</text>
<text class="note" x="120" y="272" text-anchor="middle">创建后的初始状态</text>

<rect class="state" x="288" y="208" width="160" height="96" rx="8"/>
<text class="name" x="368" y="246" text-anchor="middle">待审</text>
<text class="note" x="368" y="272" text-anchor="middle">等待审阅人决定</text>

<rect class="state" x="536" y="208" width="160" height="96" rx="8"/>
<text class="name" x="616" y="246" text-anchor="middle">待执行</text>
<text class="note" x="616" y="272" text-anchor="middle">调度器可执行</text>

<rect class="state" x="784" y="208" width="160" height="96" rx="8"/>
<text class="name" x="864" y="246" text-anchor="middle">执行中</text>
<text class="note" x="864" y="272" text-anchor="middle">不能取消</text>

<rect class="state" x="1072" y="208" width="160" height="96" rx="8"/>
<text class="name" x="1152" y="246" text-anchor="middle">完成</text>
<text class="note" x="1152" y="272" text-anchor="middle">全部批次成功</text>

<text class="group" x="40" y="456">取消与失败</text>
<rect class="state" x="536" y="488" width="160" height="96" rx="8"/>
<text class="name" x="616" y="530" text-anchor="middle">已取消</text>
<text class="note" x="616" y="556" text-anchor="middle">从待执行取消</text>

<rect class="mask" x="784" y="488" width="160" height="96" rx="8"/>
<rect class="focal" x="784" y="488" width="160" height="96" rx="8"/>
<text class="name" x="864" y="530" text-anchor="middle">失败</text>
<text class="note" x="864" y="556" text-anchor="middle">停止后续批次</text>
<text class="note" x="976" y="526">已成功批次不自动回滚。</text>
<text class="note" x="976" y="554">失败后恢复方案未提供。</text>

<line class="rule" x1="40" y1="660" x2="1240" y2="660"/>
<text class="label" x="40" y="692">提交／取消：发布人</text>
<text class="label" x="368" y="692">通过／拒绝：审阅人</text>
<text class="label" x="744" y="692">执行中／失败／完成：调度器推进</text>
</svg>
</div>
</section>

<section>
<h2>03 · 每批成功才前进，重复结果不再推进</h2>
<div class="diagram-container">
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="batch-title batch-desc">
<title id="batch-title">调度器与工作器的批次执行时序</title>
<desc id="batch-desc">调度器先更新执行中状态再派发批次，工作器返回结果，调度器忽略已记录批次的重复结果，并按首次结果决定继续、完成或失败。</desc>
<defs>
<marker id="b-arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#4f5d75"/></marker>
<marker id="b-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#bf4520"/></marker>
<marker id="b-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#2e5aa8"/></marker>
</defs>
<rect width="1280" height="720" fill="#f5f5f5"/>
<text class="note" x="40" y="64">时间向下；展示一个批次的处理，后续批次遵循同一规则。</text>

<!-- 可选重复返回区 -->
<rect x="416" y="364" width="488" height="112" rx="4" fill="#eeeeef" stroke="#bfc0c0"/>
<rect x="416" y="364" width="40" height="16" rx="2" fill="#f5f5f5" stroke="#bfc0c0"/>
<text class="mono" x="436" y="376" text-anchor="middle">OPT</text>
<text class="label" x="472" y="380">[同一批结果再次返回]</text>

<line x1="160" y1="144" x2="160" y2="620" stroke="#bfc0c0" stroke-dasharray="3 3"/>
<line x1="440" y1="144" x2="440" y2="620" stroke="#bfc0c0" stroke-dasharray="3 3"/>
<line x1="880" y1="144" x2="880" y2="620" stroke="#bfc0c0" stroke-dasharray="3 3"/>

<path class="api-arrow" d="M440 200 H160" marker-end="url(#b-link)"/>
<rect class="mask" x="216" y="176" width="168" height="16"/>
<text class="label" x="300" y="189" text-anchor="middle">待执行 → 执行中</text>

<path class="arrow" d="M440 272 H880" marker-end="url(#b-arrow)"/>
<rect class="mask" x="580" y="248" width="160" height="16"/>
<text class="label" x="660" y="261" text-anchor="middle">派发当前批次任务</text>

<path class="arrow return" d="M880 328 H440" marker-end="url(#b-arrow)"/>
<rect class="mask" x="588" y="304" width="144" height="16"/>
<text class="label" x="660" y="317" text-anchor="middle">返回当前批次结果</text>

<path class="arrow return" d="M880 428 H440" marker-end="url(#b-arrow)"/>
<rect class="mask" x="580" y="404" width="160" height="16"/>
<text class="label" x="660" y="417" text-anchor="middle">重复返回同一批结果</text>

<rect class="box" x="80" y="96" width="160" height="48" rx="6"/>
<text class="name" x="160" y="125" text-anchor="middle">发布 API</text>
<rect class="box" x="360" y="96" width="160" height="48" rx="6"/>
<text class="name" x="440" y="125" text-anchor="middle">调度器</text>
<rect class="box" x="800" y="96" width="160" height="48" rx="6"/>
<text class="name" x="880" y="125" text-anchor="middle">部署工作器</text>

<text class="note" x="928" y="272">部署当前服务批次</text>
<text class="note" x="928" y="296">读取本单指定产物</text>

<text class="note" x="48" y="424">调度器发现该批结果已记录：</text>
<text class="note" x="48" y="452">忽略重复，不再次推进批次。</text>

<!-- 结果规则注释位于消息区之后，不作为时序参与者 -->
<rect class="mask" x="480" y="504" width="680" height="112" rx="6"/>
<rect class="focal" x="480" y="504" width="680" height="112" rx="6"/>
<text class="group" x="496" y="530">首次记录的批次结果决定下一步</text>
<text class="note" x="496" y="556">成功且还有批次 → 派发下一批，发布单保持执行中</text>
<text class="note" x="496" y="580">最后一批成功 → 写回完成</text>
<text class="note" x="496" y="604">任一批失败 → 写回失败，停止后续批次；已成功批次不自动回滚</text>

<line class="rule" x1="40" y1="660" x2="1240" y2="660"/>
<text class="label" x="40" y="692">实线：请求／任务</text>
<text class="label" x="352" y="692">虚线：结果返回</text>
<text class="label" x="664" y="692">工作器返回结果，发布状态由调度器更新</text>
</svg>
</div>
</section>

<section>
<h2>审批约束落在操作边界与当前发布单上</h2>
<div class="table-wrap">
<table>
<thead>
<tr><th>身份</th><th>允许的操作</th><th>关键约束</th></tr>
</thead>
<tbody>
<tr>
<td>发布人</td><td>提交、取消</td>
<td>取消仅适用于待执行；执行中不能取消。</td>
</tr>
<tr>
<td>审阅人</td><td>审批：通过或拒绝</td>
<td>同一单的提交人不能审批该单。</td>
</tr>
<tr>
<td>调度器</td><td>推进执行状态</td>
<td>只执行待执行单；根据批次结果推进。</td>
</tr>
</tbody>
</table>
</div>
<p class="constraint">同一个人可以同时拥有发布人和审阅人角色，但角色叠加不解除“不能审批自己提交的发布单”这一约束。门户通过 API 发起操作；具体鉴权与校验实现未提供。</p>
</section>

<footer>
范围说明：未提供数据库、消息队列、通知、超时、自动重试或失败后恢复方案，本文不补充这些机制。
</footer>
</main>
</body>
</html>
```