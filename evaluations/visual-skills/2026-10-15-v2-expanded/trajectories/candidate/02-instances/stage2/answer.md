采用站点分区视图，画布 **1100 × 640 px**。已看到的画面中，站点、实例及双向交互清晰；本稿仅修正 SVG 无障碍标识的命名，尚未重新渲染检查。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>两站采集架构</title>
<style>
  body {
    margin: 0; padding: 16px; background: #fff; color: #222;
    font-family: system-ui, "Microsoft YaHei", sans-serif;
  }
  main { max-width: 1100px; margin: auto; }
  svg { display: block; width: 100%; height: auto; }
  .zone { fill: #f5f5f5; stroke: #999; }
  .node { fill: #fff; stroke: #555; stroke-width: 1.5; }
  .flow {
    fill: none; stroke: #444; stroke-width: 1.7;
    marker-end: url(#collection-diagram-arrow);
  }
  .request {
    fill: none; stroke: #666; stroke-width: 1.7;
    stroke-dasharray: 7 5; marker-end: url(#collection-diagram-arrow);
  }
  text { fill: #222; font-size: 16px; }
  .heading { font-size: 19px; font-weight: 600; }
  .small { font-size: 14px; fill: #555; }
  .label {
    font-size: 15px; paint-order: stroke;
    stroke: #fff; stroke-width: 5px;
  }
  p { font-size: 14px; line-height: 1.6; margin: 8px 0; }
</style>
</head>
<body>
<main>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 640"
     role="img"
     aria-labelledby="collection-diagram-title collection-diagram-desc">
  <title id="collection-diagram-title">东站、西站与中心的采集架构</title>
  <desc id="collection-diagram-desc">
    两站各有独立采集器、网关和缓冲库。采集器向本网关发送读数，
    网关读写本站缓冲库。两站网关向中心汇总服务发送读数，
    汇总服务向两站网关发送补传请求，并写入归档库。
    实线表示读数或库读写，虚线表示补传请求。
  </desc>
  <defs>
    <marker id="collection-diagram-arrow" viewBox="0 0 10 10"
            refX="9" refY="5" markerWidth="7" markerHeight="7"
            orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 Z" fill="#444"/>
    </marker>
  </defs>

  <text x="30" y="32" class="heading">两站采集架构</text>
  <text x="30" y="55" class="small">站内实例独立；跨站交互分别连接中心汇总服务</text>

  <rect x="30" y="80" width="500" height="235" rx="8" class="zone"/>
  <text x="50" y="110" class="heading">东站</text>
  <text x="115" y="110" class="small">3 个独立实例</text>

  <rect x="30" y="345" width="500" height="235" rx="8" class="zone"/>
  <text x="50" y="375" class="heading">西站</text>
  <text x="115" y="375" class="small">3 个独立实例</text>

  <rect x="735" y="80" width="335" height="500" rx="8" class="zone"/>
  <text x="755" y="110" class="heading">中心</text>

  <!-- 东站实例 -->
  <rect x="60" y="150" width="130" height="60" rx="4" class="node"/>
  <text x="125" y="185" text-anchor="middle">东站采集器</text>
  <rect x="265" y="150" width="130" height="60" rx="4" class="node"/>
  <text x="330" y="185" text-anchor="middle">东站网关</text>
  <path d="M265 257 V287 A65 10 0 0 0 395 287 V257 Z" class="node"/>
  <ellipse cx="330" cy="257" rx="65" ry="10" class="node"/>
  <text x="330" y="282" text-anchor="middle">东站缓冲库</text>

  <!-- 西站实例 -->
  <rect x="60" y="415" width="130" height="60" rx="4" class="node"/>
  <text x="125" y="450" text-anchor="middle">西站采集器</text>
  <rect x="265" y="415" width="130" height="60" rx="4" class="node"/>
  <text x="330" y="450" text-anchor="middle">西站网关</text>
  <path d="M265 522 V552 A65 10 0 0 0 395 552 V522 Z" class="node"/>
  <ellipse cx="330" cy="522" rx="65" ry="10" class="node"/>
  <text x="330" y="547" text-anchor="middle">西站缓冲库</text>

  <!-- 中心实例 -->
  <rect x="785" y="190" width="230" height="240" rx="5" class="node"/>
  <text x="900" y="315" text-anchor="middle" class="heading">汇总服务</text>
  <path d="M820 500 V540 A80 13 0 0 0 980 540 V500 Z" class="node"/>
  <ellipse cx="900" cy="500" rx="80" ry="13" class="node"/>
  <text x="900" y="531" text-anchor="middle">归档库</text>

  <!-- 站内读数 -->
  <path d="M190 180 H265" class="flow"/>
  <text x="227" y="140" text-anchor="middle" class="small">发送读数</text>
  <path d="M190 445 H265" class="flow"/>
  <text x="227" y="405" text-anchor="middle" class="small">发送读数</text>

  <!-- 网关读写本站缓冲库 -->
  <path d="M330 210 V247" class="flow"
        marker-start="url(#collection-diagram-arrow)"/>
  <text x="347" y="236" class="small">读 / 写</text>
  <path d="M330 475 V512" class="flow"
        marker-start="url(#collection-diagram-arrow)"/>
  <text x="347" y="501" class="small">读 / 写</text>

  <!-- 东站与中心 -->
  <path d="M395 165 H695 V230 H785" class="flow"/>
  <text x="550" y="153" text-anchor="middle" class="label">东站读数 → 中心</text>
  <path d="M785 270 H650 V200 H395" class="request"/>
  <text x="550" y="223" text-anchor="middle" class="label">补传请求 → 东站</text>

  <!-- 西站与中心 -->
  <path d="M395 460 H695 V390 H785" class="flow"/>
  <text x="550" y="484" text-anchor="middle" class="label">西站读数 → 中心</text>
  <path d="M785 350 H650 V425 H395" class="request"/>
  <text x="550" y="412" text-anchor="middle" class="label">补传请求 → 西站</text>

  <!-- 中心归档 -->
  <path d="M900 430 V487" class="flow"/>
  <text x="916" y="464" class="small">写入</text>

  <!-- 图例 -->
  <path d="M40 615 H95" class="flow"/>
  <text x="107" y="620" class="small">读数 / 库读写</text>
  <path d="M285 615 H340" class="request"/>
  <text x="352" y="620" class="small">补传请求</text>
</svg>
<p>传输协议、认证方式、是否采用消息队列均待定；图中不作假设。</p>
</main>
</body>
</html>
```