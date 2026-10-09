### 各部分怎样协作

```mermaid
flowchart LR
    P["发布门户"] -->|"提交 / 审批 / 取消"| A["发布 API<br/>记录发布单"]
    S["调度器"] -->|"读取待执行单 / 写回状态"| A
    S -->|"下发服务批次任务"| W["部署工作器"]
    W -->|"返回批次结果（可能重复）"| S
    W -->|"读取该单指定产物"| R["产物仓库"]
```

每张发布单关联且仅关联 **一个不可变构建产物**；同一产物可供多个发布单使用。

### 状态怎样演变

箭头标明动作及其执行角色；执行中的分支由调度器根据工作器返回的批次结果推进。

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
    Review --> Ready: 审阅人审核通过
    Ready --> Cancelled: 发布人取消
    Ready --> Running: 调度器开始执行
    Running --> Running: 当前批成功且还有后续批次，部署下一批
    Running --> Failed: 任一批失败，停止后续批次
    Running --> Done: 全部批次成功

    note right of Running
        按服务批次逐批部署
        执行中不能取消
    end note
    note right of Failed
        已成功批次不自动回滚
        失败后的恢复方案未提供
    end note
```

### 批次结果与重复回报

以下展开执行阶段。调度器只启动待执行单，并在下发首批任务前将其置为执行中。

```mermaid
sequenceDiagram
    participant A as 发布 API
    participant S as 调度器
    participant W as 部署工作器

    S->>A: 读取待执行单
    S->>A: 写回执行中
    S->>W: 下发首批任务

    loop 接收批次结果
        W-->>S: 返回批次结果
        alt 该批次结果已记录
            Note over S: 忽略重复结果，不再次推进批次
        else 首次收到该批次结果
            S->>S: 记录批次结果
            alt 批次失败
                S->>A: 写回失败
                Note over S,W: 停止后续批次，已成功批次不自动回滚
            else 批次成功且还有下一批
                S->>W: 下发下一批任务
            else 批次成功且全部批次完成
                S->>A: 写回完成
            end
        end
    end
```

### 审批约束落在哪里

门户是操作入口，API 接收请求并记录发布单；提交、审批、取消请求必须符合下列角色与状态约束。**具体校验实现未提供。**

| 操作主体 | 允许的动作 | 必须满足的约束 |
|---|---|---|
| 发布人 | 提交、取消 | 草稿可提交；待执行可取消；执行中不可取消 |
| 审阅人 | 审批通过、拒绝 | 仅处理待审单；不能审批自己提交的单 |
| 调度器 | 推进执行状态 | 只启动待执行单；按批次结果推进执行中、失败、完成 |

一个人可以同时拥有发布人和审阅人角色，但 **对同一张单，提交人与审批人必须不同**。

图中未补入数据库、消息队列、通知、超时、自动重试或失败后恢复方案。以上为可编辑草稿，尚未进行工具语法检查或实际渲染验证。