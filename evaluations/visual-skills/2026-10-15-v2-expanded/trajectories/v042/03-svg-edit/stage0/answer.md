保留原流程视图与 1000 × 340 尺寸，仅将通知失败路径改为返回“发送通知”，并更新标签。

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="340" viewBox="0 0 1000 340" role="img" aria-labelledby="title description">
  <title id="title">任务与完成通知</title>
  <desc id="description">展示接收请求、执行任务、发送通知、结束四个步骤与失败返回路径。</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 Z" fill="#344054"/>
    </marker>
    <style>
      text { font-family: sans-serif; fill: #172b4d; }
      .node { fill: #fff; stroke: #667085; stroke-width: 2; }
      .edge { fill: none; stroke: #344054; stroke-width: 2; marker-end: url(#arrow); }
      .label { font-size: 20px; text-anchor: middle; }
      .edge-label { font-size: 16px; text-anchor: middle; }
    </style>
  </defs>
  <rect width="1000" height="340" fill="#f7f8fa"/>
  <text x="40" y="40" font-size="26">任务与完成通知</text>
  <g id="receive"><rect class="node" x="40" y="80" width="180" height="70" rx="6"/><text class="label" x="130" y="122">接收请求</text></g>
  <g id="execute"><rect class="node" x="300" y="80" width="180" height="70" rx="6"/><text class="label" x="390" y="122">执行任务</text></g>
  <g id="notify"><rect class="node" x="560" y="80" width="180" height="70" rx="6"/><text class="label" x="650" y="122">发送通知</text></g>
  <g id="done"><rect class="node" x="820" y="80" width="140" height="70" rx="6"/><text class="label" x="890" y="122">结束</text></g>
  <path id="receive-execute" class="edge" d="M220 115 H300"/>
  <path id="execute-notify" class="edge" d="M480 115 H560"/>
  <text class="edge-label" x="520" y="99">成功</text>
  <path id="notify-done" class="edge" d="M740 115 H820"/>
  <text class="edge-label" x="780" y="99">成功</text>
  <path id="failure" class="edge" d="M690 150 V225 Q690 245 670 245 H630 Q610 245 610 225 V150"/>
  <text id="failure-label" class="edge-label" x="650" y="278">通知失败：仅重试通知</text>
</svg>
```