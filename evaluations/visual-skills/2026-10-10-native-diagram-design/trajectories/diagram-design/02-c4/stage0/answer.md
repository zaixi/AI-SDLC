以下为四个 C4 视图，均采用 **doc-wide（1280 × 720）**：系统上下文、容器交易通信、容器事件处理、容器状态查询。后三张是同一容器层级的分视图；同名节点表示同一运行单元。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>采购协同系统 · C4 视图</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#f5f5f5;color:#2d3142;font-family:'Geist','Noto Sans SC','PingFang SC','Microsoft YaHei',system-ui,sans-serif}
main{max-width:1360px;margin:auto;padding:40px;min-width:0}
h1{font:400 28px 'Instrument Serif','Noto Serif SC','Songti SC',serif;margin:0 0 16px}
h2{font-size:20px;margin:0 0 8px;font-weight:600}
p{line-height:1.7;margin:8px 0;color:#4f5d75;font-size:14px}
section{margin-top:40px}
.diagram-container{width:100%;overflow-x:auto}
svg{display:block;width:100%;min-width:1280px}
svg text{font-family:'Geist','Noto Sans SC','PingFang SC','Microsoft YaHei',system-ui,sans-serif;fill:#2d3142;font-size:12px}
.name{font-weight:600}
.group{font-size:14px;font-weight:600;fill:#4f5d75}
.note{fill:#5a6580}
.tech{font-family:'Geist Mono',ui-monospace,monospace;font-size:9px;fill:#4f5d75}
.zone{fill:#ececec;fill-opacity:.45;stroke:#bfc0c0;stroke-dasharray:4 4}
.node{fill:#fff;stroke:#2d3142;rx:6}
.store{fill:#ececec;stroke:#4f5d75;rx:6}
.external{fill:#ececec;stroke:#4f5d75;rx:6}
.person{fill:#e5e7eb;stroke:#5a6580;rx:6}
.focal{fill:#f0e7e3;stroke:#bf4520;rx:6}
.edge{fill:none;stroke:#4f5d75;stroke-width:1.2;marker-end:url(#c4-arrow)}
.http{stroke:#2e5aa8;marker-end:url(#c4-link)}
.async{stroke-dasharray:5 4}
.mask{fill:#f5f5f5}
.rule{stroke:#bfc0c0;stroke-width:1}
table{width:100%;border-collapse:collapse;font-size:14px;margin-top:20px}
th,td{text-align:left;padding:12px;border-bottom:1px solid #bfc0c0;vertical-align:top}
th{font-weight:600}
@media print{
main{padding:16px}
.diagram-container{overflow-x:visible}
svg{min-width:0}
section{break-inside:avoid}
}
</style>
</head>
<body>
<main>
<h1>采购协同系统：组织边界与内部通信</h1>
<p>系统上下文面向业务负责人；容器视图面向工程师。容器表示应用运行单元或数据存储，不表示组件。供应商系统与付款系统始终作为外部软件系统展示。</p>

<section>
<h2>01 · 系统上下文</h2>
<p>本公司拥有采购协同系统；合作供应商与银行分别拥有自己的系统。业务通信汇总到软件系统层级。</p>
<div class="diagram-container">
<svg viewBox="0 0 1280 720" role="img" aria-labelledby="context-title context-desc" xmlns="http://www.w3.org/2000/svg">
<title id="context-title">采购协同系统的组织与系统边界</title>
<desc id="context-desc">采购员与支持工程师使用本公司的采购协同系统，该系统向供应商发送订单、接收交付事件，并向银行请求付款、接收异步付款结果。</desc>
<defs>
<marker id="c4-arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#4f5d75"/></marker>
<marker id="c4-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#bf4520"/></marker>
<marker id="c4-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#2e5aa8"/></marker>
</defs>
<rect width="1280" height="720" fill="#f5f5f5"/>
<rect class="zone" x="40" y="88" width="720" height="504" rx="8"/>
<text class="group" x="56" y="116">本公司</text>
<rect class="zone" x="880" y="88" width="360" height="216" rx="8"/>
<text class="group" x="896" y="116">合作供应商</text>
<rect class="zone" x="880" y="376" width="360" height="216" rx="8"/>
<text class="group" x="896" y="404">银行</text>

<path class="edge" d="M280 196 H352 Q360 196 360 204 V300 Q360 308 368 308 H480"/>
<path class="edge" d="M280 484 H392 Q400 484 400 476 V364 Q400 356 408 356 H480"/>
<path class="edge" d="M720 308 H792 Q800 308 800 300 V188 Q800 180 808 180 H944"/>
<path class="edge async" d="M944 228 H840 Q832 228 832 236 V324 Q832 332 824 332 H720"/>
<path class="edge" d="M720 356 H792 Q800 356 800 364 V468 Q800 476 808 476 H944"/>
<path class="edge async" d="M944 524 H840 Q832 524 832 516 V388 Q832 380 824 380 H720"/>

<rect class="mask" x="288" y="168" width="64" height="20"/><text class="note" x="320" y="183" text-anchor="middle">发订单</text>
<rect class="mask" x="288" y="456" width="96" height="20"/><text class="note" x="336" y="471" text-anchor="middle">查看处理状态</text>
<rect class="mask" x="824" y="152" width="96" height="20"/><text class="note" x="872" y="167" text-anchor="middle">发送订单</text>
<rect class="mask" x="848" y="200" width="88" height="20"/><text class="note" x="892" y="215" text-anchor="middle">交付事件</text>
<rect class="mask" x="824" y="448" width="96" height="20"/><text class="note" x="872" y="463" text-anchor="middle">请求付款</text>
<rect class="mask" x="848" y="496" width="88" height="20"/><text class="note" x="892" y="511" text-anchor="middle">付款结果</text>

<rect class="person" x="80" y="164" width="200" height="64"/>
<text class="name" x="180" y="192" text-anchor="middle">采购员</text>
<text class="note" x="180" y="212" text-anchor="middle">人员</text>
<rect class="person" x="80" y="452" width="200" height="64"/>
<text class="name" x="180" y="480" text-anchor="middle">支持工程师</text>
<text class="note" x="180" y="500" text-anchor="middle">人员 · 仅查看状态</text>
<rect class="focal" x="480" y="276" width="240" height="128"/>
<text class="name" x="600" y="328" text-anchor="middle">采购协同系统</text>
<text class="note" x="600" y="352" text-anchor="middle">软件系统 · 本公司拥有</text>
<rect class="external" x="944" y="148" width="240" height="112"/>
<text class="name" x="1064" y="192" text-anchor="middle">供应商系统</text>
<text class="note" x="1064" y="216" text-anchor="middle">软件系统 · 供应商拥有</text>
<rect class="external" x="944" y="444" width="240" height="112"/>
<text class="name" x="1064" y="488" text-anchor="middle">付款系统</text>
<text class="note" x="1064" y="512" text-anchor="middle">软件系统 · 银行拥有</text>

<line class="rule" x1="40" y1="660" x2="1240" y2="660"/>
<text class="note" x="40" y="688">图例：虚线框＝组织边界　橙色框＝本公司软件系统　灰色框＝外部软件系统　虚线箭头＝异步回传</text>
</svg>
</div>
</section>

<section>
<h2>02 · 容器视图：订单发送与付款申请</h2>
<p>展示前台调用、订单与 Outbox 写入、订单发布，以及付款申请到银行的请求路径。付款处理器的结果消费与落库见下一张。</p>
<div class="diagram-container">
<svg viewBox="0 0 1280 720" role="img" aria-labelledby="transaction-title transaction-desc" xmlns="http://www.w3.org/2000/svg">
<title id="transaction-title">订单发送与付款申请的容器通信</title>
<desc id="transaction-desc">Web门户调用采购API，采购API读写订单库、写入Outbox及Kafka，事件发布器读取Outbox并向供应商发送订单，付款处理器消费付款申请并请求银行付款。</desc>
<rect width="1280" height="720" fill="#f5f5f5"/>
<rect class="zone" x="40" y="56" width="904" height="568" rx="8"/>
<text class="group" x="56" y="84">采购协同系统 · 本公司 · 容器层级（局部）</text>
<text class="group" x="1000" y="84">外部软件系统</text>

<path class="edge http" d="M240 144 H400"/>
<path class="edge" d="M560 144 H720"/>
<path class="edge" d="M520 200 V300"/>
<path class="edge" d="M720 348 H560"/>
<path class="edge http" d="M880 348 H1000"/>
<path class="edge" d="M400 176 H128 Q120 176 120 184 V532 Q120 540 128 540 H160"/>
<path class="edge" d="M320 540 H560"/>
<path class="edge http" d="M720 540 H1000"/>

<rect class="mask" x="288" y="116" width="64" height="20"/><text class="tech" x="320" y="130" text-anchor="middle">HTTPS</text>
<rect class="mask" x="600" y="116" width="80" height="20"/><text class="note" x="640" y="131" text-anchor="middle">读写订单</text>
<rect class="mask" x="528" y="240" width="100" height="20"/><text class="note" x="536" y="255">写待发送事件</text>
<rect class="mask" x="600" y="320" width="80" height="20"/><text class="note" x="640" y="335" text-anchor="middle">读取事件</text>
<rect class="mask" x="888" y="320" width="104" height="20"/><text class="note" x="940" y="335" text-anchor="middle">HTTPS · 订单</text>
<rect class="mask" x="128" y="436" width="112" height="20"/><text class="note" x="136" y="451">写付款申请事件</text>
<rect class="mask" x="376" y="512" width="128" height="20"/><text class="note" x="440" y="527" text-anchor="middle">消费付款申请事件</text>
<rect class="mask" x="792" y="512" width="136" height="20"/><text class="note" x="860" y="527" text-anchor="middle">HTTPS · 付款请求</text>

<rect class="node" x="80" y="104" width="160" height="96"/>
<text class="name" x="160" y="144" text-anchor="middle">Web门户</text><text class="note" x="160" y="168" text-anchor="middle">应用 · 采购员使用</text>
<rect class="focal" x="400" y="104" width="160" height="96"/>
<text class="name" x="480" y="144" text-anchor="middle">采购API</text><text class="note" x="480" y="168" text-anchor="middle">独立部署进程</text>
<rect class="store" x="720" y="104" width="160" height="96"/>
<text class="name" x="800" y="144" text-anchor="middle">订单库</text><text class="tech" x="800" y="168" text-anchor="middle">PostgreSQL · 1</text>
<rect class="store" x="400" y="300" width="160" height="96"/>
<text class="name" x="480" y="340" text-anchor="middle">Outbox库</text><text class="tech" x="480" y="364" text-anchor="middle">PostgreSQL · 2</text>
<rect class="node" x="720" y="300" width="160" height="96"/>
<text class="name" x="800" y="340" text-anchor="middle">事件发布器</text><text class="note" x="800" y="364" text-anchor="middle">应用运行单元</text>
<rect class="external" x="1000" y="300" width="240" height="96"/>
<text class="name" x="1120" y="340" text-anchor="middle">供应商系统</text><text class="note" x="1120" y="364" text-anchor="middle">合作供应商拥有</text>
<rect class="store" x="160" y="492" width="160" height="96"/>
<text class="name" x="240" y="532" text-anchor="middle">Kafka</text><text class="note" x="240" y="556" text-anchor="middle">内部事件基础设施</text>
<rect class="node" x="560" y="492" width="160" height="96"/>
<text class="name" x="640" y="532" text-anchor="middle">付款处理器</text><text class="note" x="640" y="556" text-anchor="middle">应用运行单元</text>
<rect class="external" x="1000" y="492" width="240" height="96"/>
<text class="name" x="1120" y="532" text-anchor="middle">付款系统</text><text class="note" x="1120" y="556" text-anchor="middle">银行拥有</text>

<line class="rule" x1="40" y1="660" x2="1240" y2="660"/>
<text class="note" x="40" y="688">图例：白框＝应用容器　灰框＝存储／外部系统（以标签区分）　蓝箭头＝HTTPS　箭头＝调用、读写或事件交付方向</text>
</svg>
</div>
</section>

<section>
<h2>03 · 容器视图：交付事件与付款结果处理</h2>
<p>两类外部回调进入同一回调网关，由内部 Kafka 向相应处理器交付事件。这里的消费箭头表示事件从 Kafka 到处理器。</p>
<div class="diagram-container">
<svg viewBox="0 0 1280 720" role="img" aria-labelledby="events-title events-desc" xmlns="http://www.w3.org/2000/svg">
<title id="events-title">交付事件与付款结果的内部处理</title>
<desc id="events-desc">供应商和银行通过HTTPS向回调网关发送事件，网关写入Kafka，订单处理器消费交付事件并写订单库，付款处理器消费付款结果并写付款库。</desc>
<rect width="1280" height="720" fill="#f5f5f5"/>
<rect class="zone" x="360" y="256" width="880" height="368" rx="8"/>
<rect class="zone" x="680" y="88" width="240" height="168" rx="8"/>
<text class="group" x="376" y="284">采购协同系统 · 本公司 · 容器层级（局部）</text>
<text class="note" x="696" y="116">同一系统边界 · 回调入口</text>
<text class="group" x="80" y="48">外部软件系统</text>

<path class="edge http" d="M160 136 V88 Q160 80 168 80 H752 Q760 80 760 88 V136"/>
<path class="edge http async" d="M560 184 H720"/>
<path class="edge" d="M800 232 V328"/>
<path class="edge" d="M720 376 H560"/>
<path class="edge" d="M880 376 H1040"/>
<path class="edge" d="M480 424 V520"/>
<path class="edge" d="M1120 424 V520"/>

<rect class="mask" x="352" y="52" width="216" height="20"/><text class="note" x="460" y="67" text-anchor="middle">HTTPS · 发送交付事件</text>
<rect class="mask" x="568" y="156" width="144" height="20"/><text class="note" x="640" y="171" text-anchor="middle">HTTPS · 付款结果</text>
<rect class="mask" x="808" y="276" width="80" height="20"/><text class="note" x="816" y="291">写入事件</text>
<rect class="mask" x="572" y="348" width="136" height="20"/><text class="note" x="640" y="363" text-anchor="middle">消费交付事件</text>
<rect class="mask" x="896" y="348" width="128" height="20"/><text class="note" x="960" y="363" text-anchor="middle">消费付款结果</text>
<rect class="mask" x="488" y="464" width="80" height="20"/><text class="note" x="496" y="479">写订单</text>
<rect class="mask" x="1128" y="464" width="80" height="20"/><text class="note" x="1136" y="479">写付款</text>

<rect class="external" x="80" y="136" width="160" height="96"/>
<text class="name" x="160" y="176" text-anchor="middle">供应商系统</text><text class="note" x="160" y="200" text-anchor="middle">合作供应商拥有</text>
<rect class="external" x="400" y="136" width="160" height="96"/>
<text class="name" x="480" y="176" text-anchor="middle">付款系统</text><text class="note" x="480" y="200" text-anchor="middle">银行拥有</text>
<rect class="focal" x="720" y="136" width="160" height="96"/>
<text class="name" x="800" y="176" text-anchor="middle">回调网关</text><text class="note" x="800" y="200" text-anchor="middle">应用运行单元</text>
<rect class="store" x="720" y="328" width="160" height="96"/>
<text class="name" x="800" y="368" text-anchor="middle">Kafka</text><text class="note" x="800" y="392" text-anchor="middle">内部事件基础设施</text>
<rect class="node" x="400" y="328" width="160" height="96"/>
<text class="name" x="480" y="368" text-anchor="middle">订单处理器</text><text class="note" x="480" y="392" text-anchor="middle">应用运行单元</text>
<rect class="node" x="1040" y="328" width="160" height="96"/>
<text class="name" x="1120" y="368" text-anchor="middle">付款处理器</text><text class="note" x="1120" y="392" text-anchor="middle">同上一视图的容器</text>
<rect class="store" x="400" y="520" width="160" height="96"/>
<text class="name" x="480" y="560" text-anchor="middle">订单库</text><text class="tech" x="480" y="584" text-anchor="middle">PostgreSQL · 1</text>
<rect class="store" x="1040" y="520" width="160" height="96"/>
<text class="name" x="1120" y="560" text-anchor="middle">付款库</text><text class="tech" x="1120" y="584" text-anchor="middle">PostgreSQL · 3</text>

<line class="rule" x1="40" y1="660" x2="1240" y2="660"/>
<text class="note" x="40" y="688">图例：虚线框＝本系统边界　白框＝应用容器　灰框＝存储／外部系统　蓝箭头＝HTTPS　虚线箭头＝银行异步回传</text>
</svg>
</div>
</section>

<section>
<h2>04 · 容器视图：支持工程师查看状态</h2>
<p>支持工程师通过管理门户查看处理状态。查询 API 与采购 API 为两个独立部署进程；查询 API 对两座业务数据库仅有读取通信。</p>
<div class="diagram-container">
<svg viewBox="0 0 1280 720" role="img" aria-labelledby="query-title query-desc" xmlns="http://www.w3.org/2000/svg">
<title id="query-title">支持工程师的只读状态查询路径</title>
<desc id="query-desc">支持工程师使用管理门户，管理门户通过HTTPS调用独立部署的查询API，查询API只读订单库和付款库。</desc>
<rect width="1280" height="720" fill="#f5f5f5"/>
<rect class="zone" x="328" y="128" width="912" height="448" rx="8"/>
<text class="group" x="344" y="156">采购协同系统 · 本公司 · 容器层级（局部）</text>

<path class="edge" d="M240 352 H360"/>
<path class="edge http" d="M520 352 H680"/>
<path class="edge" d="M840 336 H912 Q920 336 920 328 V256 Q920 248 928 248 H1040"/>
<path class="edge" d="M840 368 H944 Q952 368 952 376 V448 Q952 456 960 456 H1040"/>

<rect class="mask" x="256" y="324" width="88" height="20"/><text class="note" x="300" y="339" text-anchor="middle">查看状态</text>
<rect class="mask" x="568" y="324" width="64" height="20"/><text class="tech" x="600" y="338" text-anchor="middle">HTTPS</text>
<rect class="mask" x="944" y="220" width="80" height="20"/><text class="note" x="984" y="235" text-anchor="middle">只读订单</text>
<rect class="mask" x="960" y="428" width="72" height="20"/><text class="note" x="996" y="443" text-anchor="middle">只读付款</text>

<rect class="person" x="80" y="304" width="160" height="96"/>
<text class="name" x="160" y="344" text-anchor="middle">支持工程师</text><text class="note" x="160" y="368" text-anchor="middle">人员</text>
<rect class="node" x="360" y="304" width="160" height="96"/>
<text class="name" x="440" y="344" text-anchor="middle">管理门户</text><text class="note" x="440" y="368" text-anchor="middle">应用容器</text>
<rect class="focal" x="680" y="304" width="160" height="96"/>
<text class="name" x="760" y="344" text-anchor="middle">查询API</text><text class="note" x="760" y="368" text-anchor="middle">独立部署进程</text>
<rect class="store" x="1040" y="200" width="160" height="96"/>
<text class="name" x="1120" y="240" text-anchor="middle">订单库</text><text class="tech" x="1120" y="264" text-anchor="middle">PostgreSQL · 1</text>
<rect class="store" x="1040" y="408" width="160" height="96"/>
<text class="name" x="1120" y="448" text-anchor="middle">付款库</text><text class="tech" x="1120" y="472" text-anchor="middle">PostgreSQL · 3</text>

<line class="rule" x1="40" y1="660" x2="1240" y2="660"/>
<text class="note" x="40" y="688">图例：人员在软件系统边界外　白／橙框＝应用容器　灰框＝独立数据库实例　蓝箭头＝HTTPS　数据库箭头＝只读访问</text>
</svg>
</div>
</section>

<table>
<thead><tr><th>层级／运行单元</th><th>解释</th></tr></thead>
<tbody>
<tr><td>C4 系统上下文</td><td>展示人员、三个软件系统及组织归属；系统间箭头汇总已确认业务通信。</td></tr>
<tr><td>C4 容器</td><td>本公司内部共 12 个运行单元，拆为三个局部视图；外部系统保持软件系统层级并明确标注。</td></tr>
<tr><td>三个 PostgreSQL 实例</td><td>订单库、Outbox库、付款库分别独立运行。编号仅用于跨图识别，不代表新增实例名称。</td></tr>
<tr><td>视图完整性</td><td>全部已确认通信均已保留；重复节点未合并运行单元。未展开组件层级、外部系统内部容器或未规定的通信细节。</td></tr>
</tbody>
</table>
<p>离线静态文档，使用本机字体回退；窄屏可在每张图内横向滚动。</p>
</main>
</body>
</html>
```