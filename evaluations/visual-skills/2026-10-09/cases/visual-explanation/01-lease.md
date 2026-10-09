```mermaid
sequenceDiagram
    participant A as Worker A
    participant P as 任务平台
    participant B as Worker B
    participant E as 外部系统
    A->>P: t=0 领取任务（租约30秒）
    B->>P: t=31 重新领取已过期任务
    Note over A,B: 同一任务可能有两次执行尝试
    A->>P: t=35 提交旧租约结果
    P-->>A: 拒绝过期租约提交
    Note over A,E: 外部写入的去重和隔离保证未提供
```
**结论：不能保证只执行一次。** 两个Worker可能都执行；平台只拒绝旧租约结果，没有提供外部副作用去重保证。依据：题目的租约和提交规则；外部写入情况未提供。未渲染验证。此图为一次性解释，不写长期设计文档。
