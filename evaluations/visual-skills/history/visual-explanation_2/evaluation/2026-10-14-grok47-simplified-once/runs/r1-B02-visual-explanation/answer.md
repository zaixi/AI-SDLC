接收规则要画清分支，并用这段采样例子算出保存和 ACK 次数。我先看可视化技能怎么落图。

去重键是 `device_id + boot_id + seq`。我按首次保存、重复只回 ACK、保存失败不记键这三条分支画页，并用 D1 的四条采样算出保存和 ACK 次数。

D1 这四条消息都保存成功：保存 4 次，发送 ACK 4 次。去重键是 `device_id + boot_id + seq`。第三次 `(D1, b7, 2)` 已记录，只重发 ACK、不重复保存；第四次换成 `b8`，是新键，要再保存。

[file:///home/eval/.answer-me-with-html/pages/采样接收规则-20261014-075617.html](file:///home/eval/.answer-me-with-html/pages/采样接收规则-20261014-075617.html)
