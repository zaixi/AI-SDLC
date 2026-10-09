### 1. 各部分怎样协作

发布单关联且仅关联一个**不可变构建产物**；同一产物可供多个发布单使用。

```mermaid
flowchart LR
    Portal["发布门户"] -->|"提交／审批／取消"| API["发布 API<br/>记录发布单"]
    Scheduler["调度器"] -->|"读取待执行单"| API
    Scheduler -->|"写回执行状态"| API
    Scheduler -->|"逐批下发部署任务"| Worker["部署工作器"]
    Worker -->|"返回批次结果<br/>可能重复"| Scheduler
    Worker -->|"读取发布单指定产物"| Repo["产物仓库"]
```

### 2. 发布状态与失败边界

箭头标明动作及其责任角色；调度器只从**待执行**开始执行。

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
    Running --> Running: 调度器记录批次成功，推进下一批
    Running --> Failed: 调度器记录任一批失败
    Running --> Done: 调度器记录全部批次成功

    note right of Running
        按服务批次逐批部署
        每批成功才推进下一批
        执行中不能取消
    end note

    note right of Failed
        停止后续批次
        已成功批次不自动回滚
    end note
```

### 3. 批次结果如何推进状态

重复结果的判断与处理在**调度器**：已记录批次的结果被忽略，不再次推进批次。

```mermaid
sequenceDiagram
    participant API as 发布 API
    participant S as 调度器
    participant W as 部署工作器
    participant R as 产物仓库

    S->>API: 读取待执行单
    S->>API: 将该单更新为执行中

    loop 按服务批次逐批执行；失败即停止
        S->>W: 下发当前批次任务
        W->>R: 读取该单指定产物
        R-->>W: 返回产物
        W-->>S: 返回批次结果

        alt 该批次结果已记录
            Note over S: 忽略重复结果，不再次推进批次
        else 该批次结果尚未记录
            S->>S: 记录批次结果
            alt 批次失败
                S->>API: 更新为失败
                Note over S,W: 停止后续批次；已成功批次不自动回滚
            else 批次成功且还有后续批次
                S->>S: 推进到下一批
            else 批次成功且全部批次已成功
                S->>API: 更新为完成
            end
        end
    end
```

### 4. 审批约束落在哪里

门户是操作入口，发布 API 接收这些操作并记录发布单。以下权限和同单约束适用于提交、审批、取消入口；具体鉴权实现位置未提供。

| 主体 | 允许的动作 | 重要约束 |
|---|---|---|
| 发布人 | 提交、取消 | 草稿可提交；仅待执行可取消 |
| 审阅人 | 审批：通过或拒绝 | 仅待审可审批；不能审批自己提交的同一单 |
| 调度器 | 推进执行状态 | 只执行待执行单；依据批次结果推进状态 |

一个人可同时拥有发布人和审阅人角色，但**双角色不豁免同单提交人与审批人的分离约束**。

未提供数据库、消息队列、通知、超时、自动重试或失败后恢复方案，图中未补设。以上为待渲染草稿，尚未检查实际画面。