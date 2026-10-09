**协作关系：发布单绑定产物，调度器组织部署，工作器执行批次。**

```mermaid
flowchart LR
    P["发布门户"] -->|"提交 / 审批 / 取消"| A["发布 API<br/>记录发布单"]
    S["调度器"] -->|"读取待执行单"| A
    S -->|"写回发布状态"| A
    S -->|"下发批次任务"| W["部署工作器"]
    W -->|"返回批次结果（可能重复）"| S
    W -->|"读取该单指定产物"| R["产物仓库"]
```

每张发布单**关联且仅关联一个不可变构建产物**；同一产物可以被多张发布单使用。

**状态演变：先审批，再执行；失败保留已经成功的部署。**

```mermaid
stateDiagram-v2
    state "草稿" as Draft
    state "待审" as Review
    state "待执行" as Ready
    state "执行中" as Running
    state "已取消" as Cancelled
    state "失败" as Failed
    state "完成" as Done

    [*] --> Draft: 创建发布单
    Draft --> Review: 发布人提交
    Review --> Draft: 审阅人拒绝
    Review --> Ready: 审阅人通过
    Ready --> Cancelled: 发布人取消
    Ready --> Running: 调度器开始执行
    Running --> Running: 当前批成功，仍有下一批
    Running --> Failed: 任一批失败，停止后续批次
    Running --> Done: 全部批次成功

    note right of Running
        按服务批次逐批部署
        执行中不能取消
    end note
    note right of Failed
        已成功批次不自动回滚
    end note
```

**批次推进：每批成功才继续，同一批结果只处理一次。**

```mermaid
sequenceDiagram
    participant S as 调度器
    participant W as 部署工作器
    participant A as 发布 API

    S->>A: 读取待执行单
    S->>A: 更新为执行中

    loop 按服务批次逐批部署，直到全部成功或任一批失败
        S->>W: 下发当前批次任务
        W-->>S: 返回批次结果
        alt 该批次结果已记录
            Note over S: 忽略重复结果，不再次推进批次
        else 该批次结果尚未记录
            S->>S: 记录批次结果
            alt 当前批失败
                S->>A: 更新为失败
                Note over S,W: 停止后续批次；已成功批次不自动回滚
            else 当前批成功，仍有下一批
                Note over S: 推进下一批
            else 当前批成功，且全部批次已成功
                S->>A: 更新为完成
            end
        end
    end
```

**审批约束针对具体发布单，拥有双角色也不能自审。**

| 主体 | 允许的操作 | 关键约束 |
|---|---|---|
| 发布人 | 提交、取消 | 仅待执行可取消；执行中不能取消 |
| 审阅人 | 审批（通过或拒绝） | 不能审批自己提交的同一张单 |
| 调度器 | 推进执行状态 | 只执行待执行单，根据批次结果推进 |

一个人可以同时拥有发布人和审阅人角色，但**该单提交人与审批人必须不同**。这些约束适用于门户向 API 发起的发布单操作；材料未指定具体权限校验实现位置。

图中未补入数据库、消息队列、通知、超时、自动重试或失败后恢复机制。以上为可编辑 Mermaid 源码，未进行工具语法检查或实际渲染。