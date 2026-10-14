采用“区域全貌、成功路径明细、失败影响”三个视图；画布宽 1120 px，高度随内容展开，小屏可横向查看图。以下为完整静态 HTML 草稿，尚未经过实际渲染检查。

```html
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>数字化平台：全貌与失败影响</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#eee;color:#222;font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif;font-size:16px;line-height:1.65}
main{max-width:1120px;margin:24px auto;background:#fff;padding:36px}
h1{font-size:30px;margin:0 0 8px}
h2{font-size:23px;margin:0 0 12px}
h3{font-size:18px;margin:0 0 8px}
p{margin:8px 0 16px}
.subtitle,.note{color:#555}
section{margin-top:30px;padding-top:24px;border-top:1px solid #ccc}
.scroll{overflow-x:auto}
svg{display:block;width:1048px;height:auto;font-family:system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif}
svg text{fill:#222}
.region{fill:#fafafa;stroke:#aaa}
.unit{fill:#fff;stroke:#999}
.arrow{fill:none;stroke:#555;stroke-width:1.5;marker-end:url(#arrow)}
table{width:100%;border-collapse:collapse;font-size:15px}
th,td{padding:12px 14px;text-align:left;vertical-align:top;border:1px solid #ccc}
th{background:#eee;font-weight:600}
td p{margin:0 0 6px}
td p:last-child{margin-bottom:0}
.tag{display:inline-block;border:1px solid #999;border-radius:4px;padding:1px 7px;background:#f5f5f5}
.callout{padding:12px 16px;background:#f5f5f5;border-left:3px solid #888;margin-top:16px}
caption{text-align:left;font-weight:600;margin-bottom:8px}
@media(max-width:700px){
main{margin:0;padding:22px 16px}
h1{font-size:25px}
th,td{padding:10px}
table{min-width:780px}
}
@media print{
body{background:#fff}
main{margin:0;max-width:none;padding:12px}
section{break-inside:avoid}
}
</style>
</head>
<body>
<main>
<header>
<h1>数字化平台：从原件到可检索结果</h1>
<p class="subtitle">先认识四个区域，再沿读写顺序追踪作业；值班时按失败类型查看状态与影响范围。</p>
</header>

<section aria-labelledby="overview">
<h2 id="overview">1 · 区域全貌</h2>
<p>成功主链：提交原件 → 保存原件并建作业 → OCR 识别 → 建立索引 → 作业完成。完成后，通知器调用平台外的邮件服务。</p>
<div class="scroll">
<svg viewBox="0 0 1048 410" role="img" aria-labelledby="overview-title overview-desc">
<title id="overview-title">数字化平台四个区域及十四个内部单元</title>
<desc id="overview-desc">接入三个单元，处理四个单元，检索四个单元，运维三个单元。下方单独列出外部邮件服务。区域分组表示职责，不表示部署方式。</desc>

<rect class="region" x="4" y="8" width="246" height="294" rx="8"/>
<rect class="region" x="268" y="8" width="246" height="294" rx="8"/>
<rect class="region" x="532" y="8" width="246" height="294" rx="8"/>
<rect class="region" x="796" y="8" width="246" height="294" rx="8"/>

<g font-size="20" font-weight="600" text-anchor="middle">
<text x="127" y="43">接入</text>
<text x="391" y="43">处理</text>
<text x="655" y="43">检索</text>
<text x="919" y="43">运维</text>
</g>
<g font-size="14" text-anchor="middle">
<text x="127" y="68">接收并保存原件</text>
<text x="391" y="68">管理作业与识别文本</text>
<text x="655" y="68">建立索引并提供查询</text>
<text x="919" y="68">查看状态与发送通知</text>
</g>

<g class="unit">
<rect x="22" y="88" width="210" height="42" rx="4"/>
<rect x="22" y="140" width="210" height="42" rx="4"/>
<rect x="22" y="192" width="210" height="42" rx="4"/>
<rect x="286" y="88" width="210" height="42" rx="4"/>
<rect x="286" y="140" width="210" height="42" rx="4"/>
<rect x="286" y="192" width="210" height="42" rx="4"/>
<rect x="286" y="244" width="210" height="42" rx="4"/>
<rect x="550" y="88" width="210" height="42" rx="4"/>
<rect x="550" y="140" width="210" height="42" rx="4"/>
<rect x="550" y="192" width="210" height="42" rx="4"/>
<rect x="550" y="244" width="210" height="42" rx="4"/>
<rect x="814" y="88" width="210" height="42" rx="4"/>
<rect x="814" y="140" width="210" height="42" rx="4"/>
<rect x="814" y="192" width="210" height="42" rx="4"/>
</g>
<g font-size="17" text-anchor="middle">
<text x="127" y="115">上传页</text>
<text x="127" y="167">接收 API</text>
<text x="127" y="219">原件库</text>
<text x="391" y="115">作业表</text>
<text x="391" y="167">调度器</text>
<text x="391" y="219">OCR 工作者</text>
<text x="391" y="271">文本库</text>
<text x="655" y="115">索引工作者</text>
<text x="655" y="167">搜索索引</text>
<text x="655" y="219">查询 API</text>
<text x="655" y="271">搜索页</text>
<text x="919" y="115">状态页</text>
<text x="919" y="167">状态 API</text>
<text x="919" y="219">通知器</text>
</g>
<rect x="796" y="336" width="246" height="58" rx="6" fill="#f3f3f3" stroke="#777" stroke-dasharray="5 4"/>
<text x="919" y="361" text-anchor="middle" font-size="17">外部邮件服务</text>
<text x="919" y="382" text-anchor="middle" font-size="13">平台之外</text>
<text x="10" y="352" font-size="15">14 个内部单元均独立列出。</text>
<text x="10" y="378" font-size="15">此图按职责分区；调用、读写与先后约束见下表。</text>
</svg>
</div>
</section>

<section aria-labelledby="success">
<h2 id="success">2 · 成功路径：谁读、谁写、先做什么</h2>
<p>①—⑤是处理主链；⑥、⑦是查询路径；⑧从已完成作业读取通知信息。箭头表示给定的动作方向，未指定传输协议。</p>
<div class="scroll">
<table>
<caption>全部已知关系</caption>
<thead>
<tr><th style="width:15%">路径</th><th style="width:64%">动作与顺序</th><th style="width:21%">结果 / 职责</th></tr>
</thead>
<tbody>
<tr>
<td>① 提交</td>
<td>上传页 → 接收 API：提交原件。</td>
<td>上传页供用户提交原件。</td>
</tr>
<tr>
<td>② 保存与建作业</td>
<td><p>先：接收 API → 原件库：写入原件。</p><p>再：接收 API → 作业表：建立待处理作业。</p></td>
<td>原件库保存原始文件；作业表保存作业状态。</td>
</tr>
<tr>
<td>③ 派发 OCR</td>
<td><p>调度器 ← 作业表：读取待处理作业。</p><p>先：调度器 → 作业表：状态改为处理中。</p><p>再：调度器 → OCR 工作者：派发 OCR。</p></td>
<td><span class="tag">处理中</span></td>
</tr>
<tr>
<td>④ 识别与交接</td>
<td><p>OCR 工作者 ← 原件库：读取原件。</p><p>OCR 工作者 → 文本库：写入识别结果。</p><p>再：OCR 工作者 → 作业表：状态改为待索引。</p><p>随后：OCR 工作者 → 索引工作者：通知索引。</p></td>
<td>文本库保存识别结果。<br><span class="tag">待索引</span></td>
</tr>
<tr>
<td>⑤ 建立索引</td>
<td><p>索引工作者 ← 文本库：读取文本。</p><p>索引工作者 → 搜索索引：写入索引。</p><p>成功后：索引工作者 → 作业表：状态改为已完成。</p></td>
<td>搜索索引保存可查询索引。<br><span class="tag">已完成</span></td>
</tr>
<tr>
<td>⑥ 搜索</td>
<td><p>搜索页 → 查询 API：调用查询。</p><p>查询 API ← 搜索索引：只读。</p></td>
<td>搜索页供用户检索。</td>
</tr>
<tr>
<td>⑦ 查看状态</td>
<td><p>状态页 → 状态 API：调用状态查询。</p><p>状态 API ← 作业表：只读。</p></td>
<td>状态页供用户查看作业状态。</td>
</tr>
<tr>
<td>⑧ 完成通知</td>
<td><p>通知器 ← 作业表：读取已完成作业。</p><p>通知器 → 外部邮件服务：调用服务发送完成通知。</p></td>
<td>外部邮件服务不属于平台。</td>
</tr>
</tbody>
</table>
</div>
</section>

<section aria-labelledby="failure">
<h2 id="failure">3 · 失败定位：作业状态与影响范围</h2>
<p>图中状态均保存在作业表。索引失败停留在待索引；邮件失败发生在作业已完成之后。</p>
<div class="scroll">
<svg viewBox="0 0 1048 308" role="img" aria-labelledby="state-title state-desc">
<title id="state-title">成功状态转换及三类失败的位置</title>
<desc id="state-desc">待处理经调度器变为处理中，OCR 成功后变为待索引，索引成功后变为已完成。OCR 失败变为失败，索引失败保持待索引，邮件发送失败仍为已完成。</desc>
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
<path d="M0 0 L10 5 L0 10Z" fill="#555"/>
</marker>
</defs>
<g fill="#f4f4f4" stroke="#888">
<rect x="18" y="68" width="160" height="54" rx="5"/>
<rect x="290" y="68" width="160" height="54" rx="5"/>
<rect x="562" y="68" width="160" height="54" rx="5"/>
<rect x="834" y="68" width="190" height="54" rx="5"/>
</g>
<g font-size="19" text-anchor="middle">
<text x="98" y="102">待处理</text>
<text x="370" y="102">处理中</text>
<text x="642" y="102">待索引</text>
<text x="929" y="102">已完成</text>
</g>
<path class="arrow" d="M178 95 H290"/>
<path class="arrow" d="M450 95 H562"/>
<path class="arrow" d="M722 95 H834"/>
<g font-size="14" text-anchor="middle">
<text x="234" y="48">调度器改状态</text>
<text x="506" y="48">OCR 成功</text>
<text x="778" y="48">索引成功</text>
</g>

<path class="arrow" d="M370 122 V177"/>
<path class="arrow" d="M642 122 V177"/>
<path class="arrow" d="M929 122 V177"/>
<g font-size="14" text-anchor="middle">
<text x="370" y="155">OCR 失败</text>
<text x="642" y="155">索引失败</text>
<text x="929" y="155">邮件发送失败</text>
</g>
<g fill="#fff" stroke="#888">
<rect x="278" y="180" width="184" height="106" rx="5"/>
<rect x="550" y="180" width="184" height="106" rx="5"/>
<rect x="822" y="180" width="214" height="106" rx="5"/>
</g>
<g text-anchor="middle">
<text x="370" y="208" font-size="18" font-weight="600">改为失败</text>
<text x="370" y="237" font-size="14">OCR 工作者写入状态</text>
<text x="370" y="263" font-size="14">再次处理需人工重新排队</text>
<text x="642" y="208" font-size="18" font-weight="600">保持待索引</text>
<text x="642" y="237" font-size="14">保留文本，只重试索引</text>
<text x="642" y="263" font-size="14">不重跑 OCR</text>
<text x="929" y="208" font-size="18" font-weight="600">仍是已完成</text>
<text x="929" y="237" font-size="14">通知器只重试邮件发送</text>
<text x="929" y="263" font-size="14">不重跑 OCR 或索引</text>
</g>
<text x="18" y="214" font-size="14">上方：成功状态链</text>
<text x="18" y="241" font-size="14">下方：失败后的状态</text>
<text x="18" y="268" font-size="14">箭头不代表重试调度</text>
</svg>
</div>

<div class="scroll">
<table>
<caption>值班速查：针对该作业的已知影响</caption>
<thead>
<tr><th style="width:14%">失败点</th><th style="width:27%">直接影响</th><th style="width:34%">保留 / 不重跑的部分</th><th style="width:25%">再次处理与未知项</th></tr>
</thead>
<tbody>
<tr>
<td><strong>OCR</strong></td>
<td>OCR 工作者将状态改为失败；该次执行未达到“待索引 → 已完成”的成功路径。</td>
<td>原件此前已保存。材料未说明失败时是否已有部分文本或索引，不推断其结果。</td>
<td>再次处理需人工重新排队；人工操作入口尚未确定。</td>
</tr>
<tr>
<td><strong>索引</strong></td>
<td>状态保持待索引，未达到已完成；该作业尚不满足通知器读取已完成作业的条件。</td>
<td>已写入的文本保留，不重跑 OCR。失败时搜索索引具体写入到何种程度未说明。</td>
<td>只重试索引；由谁、何时调度尚未确定。</td>
</tr>
<tr>
<td><strong>邮件发送</strong></td>
<td>完成通知发送失败，作业仍是已完成。</td>
<td>OCR 与索引的成功结果不因邮件失败而回退；不重跑 OCR 或索引。</td>
<td>通知器只重试邮件发送；重试时机未定。</td>
</tr>
</tbody>
</table>
</div>

<div class="callout">
<strong>状态与搜索分别读取不同数据。</strong>
状态 API 只读作业表，因此对应作业分别显示“失败”“待索引”“已完成”；
查询 API 只读搜索索引。材料未定义 OCR 或索引失败后的搜索可见性，也未说明其他作业的影响范围。
</div>
<p class="note">边界：传输协议、消息队列、部署方式均未提供；此图不指定这些实现，也不补充重试调度或人工处理入口。</p>
</section>
</main>
</body>
</html>
```