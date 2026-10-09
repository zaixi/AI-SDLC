```mermaid
flowchart LR
    API[API：订单入队] --> Q[队列]
    Q --> W[Worker：消费订单]
    W --> DB[(数据库)]
```

已知事实：API负责入队，Worker负责消费并写数据库；ADR确认API不直接写数据库。

尚未确认：为何选队列、是否为了提高吞吐或隔离故障。图中的职责分工不能证明这些设计动机。
