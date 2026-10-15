采用每日折线图，6 月 3 日留空并标注“未采集”；画布为 600 × 360，随屏幕宽度缩放。

```html
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>6 月 1 日至 6 月 6 日每日处理包裹数</title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 32px 16px;
    background: #f3f4f5;
    color: #24282d;
    font-family: system-ui, -apple-system, "Segoe UI", "Microsoft YaHei", sans-serif;
  }
  main {
    max-width: 760px;
    margin: auto;
    padding: 28px;
    background: #fff;
    border: 1px solid #dce0e3;
    border-radius: 12px;
  }
  h1 { margin: 0 0 8px; font-size: 24px; line-height: 1.4; }
  .subtitle, .note { color: #555d65; font-size: 15px; line-height: 1.7; }
  .subtitle { margin: 0 0 16px; }
  figure { margin: 0; }
  svg { display: block; width: 100%; height: auto; }
  svg text { font-family: inherit; font-size: 19px; fill: #555d65; }
  .value { fill: #24282d; font-size: 22px; font-weight: 650; }
  .grid { stroke: #e1e4e7; stroke-width: 1; }
  .line { fill: none; stroke: #404a55; stroke-width: 3; }
  .point { fill: #fff; stroke: #404a55; stroke-width: 3; }
  .note { margin: 12px 0 0; }
  @media (max-width: 480px) {
    body { padding: 16px 8px; }
    main { padding: 18px 10px; }
    h1 { font-size: 21px; }
    .subtitle, .note { font-size: 14px; }
    svg text { font-size: 22px; }
    .value { font-size: 24px; }
  }
</style>
</head>
<body>
<main>
  <h1>每日处理包裹数</h1>
  <p class="subtitle">某仓库 · 6 月 1 日—6 月 6 日 · 单位：件</p>
  <figure>
    <svg viewBox="0 0 600 360" role="img" aria-labelledby="chart-title chart-desc">
      <title id="chart-title">每日处理包裹数趋势图</title>
      <desc id="chart-desc">
        6月1日80件，6月2日92件，6月3日未采集，6月4日88件，
        6月5日115件，6月6日112件。
        纵轴从0到120件。6月3日没有数据点，折线在此断开，
        不连接6月2日和6月4日。没有其他日期的数据。
      </desc>

      <!-- 缺失日期的背景仅标记日期，不表示数值。 -->
      <rect x="226" y="48" width="76" height="232" rx="6" fill="#f0f1f2"/>

      <g class="grid">
        <path d="M58 68H574"/>
        <path d="M58 132H574"/>
        <path d="M58 196H574"/>
        <path d="M58 260H574"/>
      </g>
      <g text-anchor="end">
        <text x="48" y="75">120</text>
        <text x="48" y="139">80</text>
        <text x="48" y="203">40</text>
        <text x="48" y="267">0</text>
      </g>

      <!-- 两段折线在缺失日期处断开，不插值。 -->
      <path class="line" d="M80 132L172 112.8"/>
      <path class="line" d="M356 119.2L448 76L540 80.8"/>

      <g class="point">
        <circle cx="80" cy="132" r="5"/>
        <circle cx="172" cy="112.8" r="5"/>
        <circle cx="356" cy="119.2" r="5"/>
        <circle cx="448" cy="76" r="5"/>
        <circle cx="540" cy="80.8" r="5"/>
      </g>
      <g class="value" text-anchor="middle">
        <text class="value" x="80" y="113">80</text>
        <text class="value" x="172" y="94">92</text>
        <text class="value" x="356" y="100">88</text>
        <text class="value" x="448" y="57">115</text>
        <text class="value" x="540" y="62">112</text>
      </g>

      <text x="264" y="212" text-anchor="middle">未采集</text>

      <g text-anchor="middle">
        <text x="80" y="312">6/1</text>
        <text x="172" y="312">6/2</text>
        <text x="264" y="312">6/3</text>
        <text x="356" y="312">6/4</text>
        <text x="448" y="312">6/5</text>
        <text x="540" y="312">6/6</text>
      </g>
    </svg>
    <figcaption class="note">
      6 月 3 日未采集，折线在该日断开；缺失值未补值、未记为零。仅展示所提供的六个日期。
    </figcaption>
  </figure>
</main>
</body>
</html>
```