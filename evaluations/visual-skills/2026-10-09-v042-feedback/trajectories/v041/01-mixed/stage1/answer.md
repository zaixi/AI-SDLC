### 各部分怎样协作

```mermaid
flowchart LR
    P["发布门户"] -->|"提交 / 审批 / 取消"| A["发布 API<br/>记录发布单"]
    S["调度器"] -->|"读取待执行单<br/>写回状态"| A
    S -->|"下发服务批次任务"| W["部署工作器"]
    W -->|"返回批次结果<br/>可能重复"| S
    W -->|"读取该单指定产物"| R["产物仓库"]
```

每张发布单关联且仅关联 **一个不可变构建产物**；同一产物可被多个发布单使用。

### 发布状态与异常

```mermaid
stateDiagram-v2
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
    Review --> Ready: 审阅人通过
    Ready --> Cancelled: 发布人取消
    Ready --> Running: 调度器启动
    Running --> Running: 本批成功且有下一批
    Running --> Failed: 任一批失败
    Running --> Done: 全部批次成功
```

调度器只启动待执行单，先进入执行中，再按服务批次逐批部署。**每批成功才部署下一批；执行中不能取消。** 任一批失败就停止后续批次，已成功批次不自动回滚。

### 批次结果如何推进状态

```mermaid
sequenceDiagram
    participant A as 发布 API
    participant S as 调度器
    participant W as 部署工作器

    S->>A: 读取待执行单
    S->>A: 写回执行中
    S->>W: 下发首批任务

    loop 每次收到批次结果
        W-->>S: 返回批次结果
        alt 该批结果已记录
            Note over S: 忽略重复结果<br/>不再次推进批次
        else 该批结果未记录
            S->>S: 记录批次结果
            alt 本批失败
                S->>A: 写回失败
                Note over S: 停止后续批次
            else 本批成功，仍有后续批次
                S->>W: 下发下一批任务
            else 本批成功，全部批次成功
                S->>A: 写回完成
            end
        end
    end
```

失败或完成后，重复回报仍按“已记录则忽略”处理；接收重复结果不会重新启动部署。

### 审批约束落在哪里

门户是操作入口，API 接收请求并记录发布单。请求须满足以下规则；具体校验实现未提供。

| 主体 | 允许的动作 | 约束 |
|---|---|---|
| 发布人 | 提交、取消 | 草稿可提交；待执行可取消；执行中不可取消 |
| 审阅人 | 审核通过、拒绝 | 仅审批待审单；不能审批自己提交的单 |
| 调度器 | 推进执行状态 | 只启动待执行单；根据批次结果推进状态 |

**一个人可以拥有两个角色，但同一单的提交人不能审批该单。** 双角色不解除这一限制。

未提供数据库、消息队列、通知、超时、自动重试或失败后恢复方案，图中不作补充。

上一版已成功渲染；本版缩短了标签、移出了较长注释，尚待实际渲染确认布局。