已查看图表与桌面渲染，标签、刻度和轴标题无重叠，保留当前稿：单张 800 × 400 横向条形图。窄屏支持横向滚动，但尚未收到窄屏渲染画面。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>本次实验 P95 延迟比较</title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 24px;
    color: #242424;
    background: #f5f5f4;
    font-family: system-ui, -apple-system, "Segoe UI", "Microsoft YaHei",
      "PingFang SC", sans-serif;
    line-height: 1.6;
  }
  main {
    max-width: 880px;
    margin: 0 auto;
    padding: 28px;
    background: #fff;
    border: 1px solid #d6d6d3;
    border-radius: 12px;
  }
  h1 { margin: 0 0 6px; font-size: 26px; line-height: 1.35; }
  p { margin: 0; font-size: 16px; }
  .context { color: #595959; }
  figure { margin: 20px 0; }
  .chart {
    overflow-x: auto;
    border: 1px solid #e0e0dd;
    border-radius: 8px;
  }
  .chart:focus-visible { outline: 2px solid #555; outline-offset: 3px; }
  svg {
    display: block;
    width: 100%;
    min-width: 720px;
    height: auto;
    font-family: inherit;
  }
  figcaption { margin-top: 10px; font-size: 15px; color: #595959; }
  .conclusion { padding-top: 16px; border-top: 1px solid #dededb; }
  .mobile-hint { display: none; }
  @media (max-width: 600px) {
    body { padding: 12px; }
    main { padding: 18px 14px; }
    h1 { font-size: 23px; }
    .mobile-hint {
      display: block;
      margin-top: 8px;
      color: #595959;
      font-size: 14px;
    }
  }
</style>
</head>
<body>
<main>
  <h1>本次实验 P95 延迟比较</h1>
  <p class="context">同样测试环境 · 每个方案一个汇总值 · 延迟越低越好</p>
  <p class="mobile-hint">可左右滑动查看完整图表。</p>

  <figure>
    <div class="chart" tabindex="0" role="region"
         aria-label="P95 延迟图表，窄屏可横向滚动">
      <svg xmlns="http://www.w3.org/2000/svg"
           viewBox="0 0 800 400" role="img"
           aria-labelledby="chart-title chart-desc">
        <title id="chart-title">四个方案的 P95 绝对延迟</title>
        <desc id="chart-desc">
          所有条形共用从零到四十毫秒的线性尺度。
          方案甲十八毫秒，验收上限二十毫秒；
          方案乙二十五毫秒，验收上限四十毫秒；
          方案丙十二毫秒，验收上限十五毫秒；
          旧版基准三十毫秒，没有验收上限。
          无原始样本或误差估计，未绘制误差线。
        </desc>
        <rect width="800" height="400" fill="#fff"/>

        <!-- 图例 -->
        <rect x="140" y="22" width="28" height="14" rx="2" fill="#666b70"/>
        <text x="180" y="36" font-size="17" fill="#333">测得 P95 延迟</text>
        <path d="M 376 20 V 39" stroke="#292929" stroke-width="3"/>
        <text x="390" y="36" font-size="17" fill="#333">各方案验收上限</text>

        <!-- 共同零基线与线性尺度：x = 140 + 延迟(ms) × 13 -->
        <g stroke="#e4e4e1" stroke-width="1">
          <path d="M 270 66 V 313"/>
          <path d="M 400 66 V 313"/>
          <path d="M 530 66 V 313"/>
          <path d="M 660 66 V 313"/>
        </g>
        <path d="M 140 66 V 313" stroke="#777" stroke-width="1.5"/>

        <g font-size="19" fill="#242424" text-anchor="end">
          <text x="119" y="111">方案甲</text>
          <text x="119" y="176">方案乙</text>
          <text x="119" y="241">方案丙</text>
          <text x="119" y="306">旧版基准</text>
        </g>

        <!-- 条形长度只编码测得的绝对延迟 -->
        <g fill="#666b70">
          <rect x="140" y="88" width="234" height="30" rx="2"/>
          <rect x="140" y="153" width="325" height="30" rx="2"/>
          <rect x="140" y="218" width="156" height="30" rx="2"/>
          <rect x="140" y="283" width="390" height="30" rx="2"/>
        </g>

        <!-- 各方案验收上限为独立刻线；旧版没有验收上限 -->
        <g stroke="#292929" stroke-width="3">
          <path d="M 400 83 V 123"/>
          <path d="M 660 148 V 188"/>
          <path d="M 335 213 V 253"/>
        </g>
        <g font-size="17" fill="#555">
          <text x="400" y="77" text-anchor="middle">上限 20 ms</text>
          <text x="660" y="142" text-anchor="middle">上限 40 ms</text>
          <text x="335" y="207" text-anchor="middle">上限 15 ms</text>
          <text x="588" y="306">无验收上限</text>
        </g>

        <!-- 四个测得原值，单位均为 ms -->
        <g font-size="18" font-weight="600" fill="#fff" text-anchor="end">
          <text x="362" y="110">18 ms</text>
          <text x="453" y="175">25 ms</text>
          <text x="284" y="240">12 ms</text>
          <text x="518" y="305">30 ms</text>
        </g>

        <path d="M 140 327 H 660" stroke="#777" stroke-width="1"/>
        <g font-size="17" fill="#444" text-anchor="middle">
          <text x="140" y="351">0</text>
          <text x="270" y="351">10</text>
          <text x="400" y="351">20</text>
          <text x="530" y="351">30</text>
          <text x="660" y="351">40</text>
        </g>
        <text x="400" y="382" text-anchor="middle" font-size="17" fill="#444">
          P95 延迟（ms）
        </text>
      </svg>
    </div>
    <figcaption>
      条形共用零基线，比较绝对延迟；刻线表示各自验收上限。
      无原始样本或误差估计，未绘制误差线。
    </figcaption>
  </figure>

  <p class="conclusion">
    <strong>方案丙延迟最低（12 ms）。</strong>
    本次测得值从低到高为：丙、甲、乙、旧版基准。
    甲、乙、丙均低于各自验收上限；现有汇总值不足以判断差异的统计显著性。
  </p>
</main>
</body>
</html>
```