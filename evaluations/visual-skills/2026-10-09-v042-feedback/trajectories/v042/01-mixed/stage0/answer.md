### 各部分怎样协作

```mermaid
flowchart LR
    P["发布门户"] -->|"提交／审批／取消"| A["发布 API<br/>记录发布单"]
    S["调度器"] -->|"读取待执行单／写回状态"| A
    S -->|"下发批次任务"| W["部署工作器"]
    W -->|"返回批次结果（可能重复）"| S
    W -->|"读取发布单指定的产物"| R["产物仓库"]
```

每个发布单**仅关联一个不可变构建产物**；同一产物可供多个发布单使用。工作器负责部署并返回结果，调度器据此更新发布状态。

### 发布状态怎样演变

```mermaid
stateDiagram-v2
    direction TB
    state "草稿" as Draft
    state "待审" as Review
    state "待执行" as Ready
    state "执行中" as Running
    state "已取消" as Cancelled
    state "失败" as Failed
    state "完成" as Done

    [*] --> Draft: 创建
    Draft --> Review: 发布人提交
    Review --> Draft: 审阅人拒绝
    Review --> Ready: 审阅人审核通过
    Ready --> Cancelled: 发布人取消
    Ready --> Running: 调度器开始执行
    Running --> Running: 本批成功且仍有下一批
    Running --> Failed: 任一批失败
    Running --> Done: 全部批次成功

    note right of Running
        按服务批次逐批部署
        执行中不能取消
        已记录批次的重复结果不推进状态
    end note
    note right of Failed
        停止后续批次
        已成功批次不自动回滚
    end note
```

### 批次结果怎样影响执行

下图展开“执行中”的处理；重复结果不会触发下一批。

```mermaid
sequenceDiagram
    participant A as 发布 API
    participant S as 调度器
    participant W as 部署工作器
    participant R as 产物仓库

    S->>A: 读取待执行单
    A-->>S: 待执行单及指定产物
    S->>A: 状态写为执行中

    loop 按服务批次逐批执行；失败后停止
        S->>W: 下发当前批次任务
        W->>R: 读取该单指定产物
        R-->>W: 指定产物
        W-->>S: 返回批次结果

        alt 该批次结果已记录
            Note over S: 忽略重复结果<br/>不再次推进批次
        else 该批次结果尚未记录
            S->>S: 记录批次结果
            alt 本批失败
                S->>A: 状态写为失败
                Note over S,W: 停止后续批次<br/>已成功批次不自动回滚
            else 本批成功且仍有下一批
                S->>S: 推进到下一批
            else 本批成功且全部批次已成功
                S->>A: 状态写为完成
            end
        end
    end
```

### 审批与操作约束

门户向 API 发起操作；下表说明各操作必须遵守的约束。具体校验实现位置未提供。

| 主体 | 允许的操作 | 约束 |
|---|---|---|
| 发布人 | 提交、取消 | 草稿可提交；仅待执行可取消 |
| 审阅人 | 审核通过、拒绝 | 仅审批待审单；不能审批自己提交的同一单 |
| 调度器 | 推进执行状态 | 只执行待执行单；根据批次结果推进 |

一个人可以同时拥有发布人和审阅人角色，**双角色仍不能绕过同一单的提交人与审批人分离约束**。

未提供数据库、消息队列、通知、超时、自动重试或失败后恢复方案。以上为可编辑草稿，尚未检查实际渲染画面。