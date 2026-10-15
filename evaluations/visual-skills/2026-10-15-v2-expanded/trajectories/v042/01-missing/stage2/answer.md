保留已查看的版本：单幅折线图，画布 360 × 290，6 月 3 日留空断线。桌面渲染清晰；手机适配已写入样式，但未收到手机实图。以下源码未作改动。

```html
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>仓库每日处理包裹数</title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 24px 16px;
    background: #f4f4f3;
    color: #242424;
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  }
  main {
    max-width: 720px;
    margin: 0 auto;
    padding: 28px;
    background: #fff;
    border: 1px solid #dededb;
    border-radius: 12px;
  }
  h1 { margin: 0 0 8px; font-size: 24px; line-height: 1.4; }
  .subtitle { margin: 0; color: #606060; font-size: 15px; }
  figure { margin: 20px 0 0; }
  svg { display: block; width: 100%; height: auto; }
  svg text { font-family: inherit; }
  figcaption {
    margin-top: 8px;
    padding: 12px 14px;
    background: #f5f5f4;
    border-left: 3px solid #777;
    font-size: 14px;
    line-height: 1.7;
  }
  @media (max-width: 480px) {
    body { padding: 12px 8px; }
    main { padding: 20px 10px; }
    h1 { font-size: 21px; }
    .subtitle, figcaption { font-size: 14px; }
  }
</style>
</head>
<body>
<main>
  <h1>仓库每日处理包裹数</h1>
  <p class="subtitle">6 月 1 日—6 月 6 日 · 单位：件</p>

  <figure>
    <svg viewBox="0 0 360 290" role="img"
         aria-labelledby="chart-title chart-desc">
      <title id="chart-title">每日处理包裹数趋势</title>
      <desc id="chart-desc">
        6月1日80件，6月2日92件，6月3日未采集，
        6月4日88件，6月5日115件，6月6日112件。
        6月3日留空，折线在该日断开，不表示零，也不连接两侧数据。
        纵轴从0到120件。
      </desc>

      <!-- 纵轴与水平网格线 -->
      <g stroke="#e5e5e3" stroke-width="1">
        <path d="M42 60H340 M42 120H340 M42 180H340"/>
      </g>
      <path d="M42 240H340" stroke="#999" stroke-width="1"/>
      <g fill="#666" font-size="12" text-anchor="end">
        <text x="33" y="64">120</text>
        <text x="33" y="124">80</text>
        <text x="33" y="184">40</text>
        <text x="33" y="244">0</text>
      </g>
      <text x="42" y="27" fill="#666" font-size="12">处理量（件）</text>

      <!-- 缺失日背景提示；不绘制数据点 -->
      <rect x="141" y="48" width="42" height="192"
            rx="4" fill="#f2f2f0"/>
      <text x="162" y="153" fill="#666" font-size="12"
            text-anchor="middle">未采集</text>

      <!-- 仅连接相邻且都有数据的日期 -->
      <g fill="none" stroke="#414141" stroke-width="2.5"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M48 120L105 102"/>
        <path d="M219 108L276 67.5L333 72"/>
      </g>
      <g fill="#414141" stroke="#fff" stroke-width="1.5">
        <circle cx="48" cy="120" r="4.5"/>
        <circle cx="105" cy="102" r="4.5"/>
        <circle cx="219" cy="108" r="4.5"/>
        <circle cx="276" cy="67.5" r="4.5"/>
        <circle cx="333" cy="72" r="4.5"/>
      </g>

      <!-- 有效观测值 -->
      <g fill="#242424" font-size="14" font-weight="600"
         text-anchor="middle">
        <text x="48" y="106">80</text>
        <text x="105" y="88">92</text>
        <text x="219" y="94">88</text>
        <text x="276" y="53.5">115</text>
        <text x="333" y="58">112</text>
      </g>

      <g fill="#555" font-size="12" text-anchor="middle">
        <text x="48" y="264">6/1</text>
        <text x="105" y="264">6/2</text>
        <text x="162" y="264">6/3</text>
        <text x="219" y="264">6/4</text>
        <text x="276" y="264">6/5</text>
        <text x="333" y="264">6/6</text>
      </g>
    </svg>

    <figcaption>
      <strong>6 月 3 日未采集。</strong>
      该日无数据点，折线断开；未补值，也未按零计算。
      图中仅展示 6 月 1 日至 6 月 6 日的数据。
    </figcaption>
  </figure>
</main>
</body>
</html>
```