D1 这四条消息都保存成功：保存 4 次，发送 ACK 4 次。去重键是 `device_id + boot_id + seq`。第三次 `(D1, b7, 2)` 已记录，只重发 ACK、不重复保存；第四次换成 `b8`，是新键，要再保存。

[file:///home/eval/.answer-me-with-html/pages/采样接收规则-20261014-075617.html](file:///home/eval/.answer-me-with-html/pages/采样接收规则-20261014-075617.html)
