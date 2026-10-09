# 容器重测：六份原始输出

每组两份输出。各份在新的容器与CLI会话中生成；Skill与相关参考由测试器直接注入输入。不是自动加载测试。协议、输入、解析结果见[README](README.md)。

## 支付并发与迟到回调

### show-me

[原始文件](outputs/show-me/01-concurrent.md)

```mermaid
sequenceDiagram
    participant C as 客户端
    participant O as 订单服务
    participant P as 支付服务
    participant G as 支付渠道

    C->>O: 提交 payment_id
    O->>P: 发起扣款
    P->>G: 【扣款】请求扣款

    alt 渠道及时返回成功
        G-->>P: 扣款成功
        P->>P: 原子登记一次成功
        P->>O: 【状态通知】置 paid
        O-->>C: 支付成功
    else 渠道响应超时
        Note over P,G: 超时不进入 failed
        P->>O: 【状态通知】置 pending
        O-->>C: 结果未知

        par 客户端重试路径
            loop 至多两次重试，使用同一 payment_id
                C->>O: 重试 payment_id
                O->>P: 转交重试
                P->>G: 【查询】查询支付结果
                Note over P,G: 每次只查询，不再次扣款
                G-->>P: 查询结果
                alt 查询确认成功
                    P->>P: 原子尝试登记成功
                    alt 首次登记成功
                        P->>O: 【状态通知】置 paid
                    else 成功已登记
                        Note over P: 忽略后到成功，不再次通知
                    end
                else 查询结果未知
                    Note over P,O: 未确认成功时保持 pending
                end
            end
        and 渠道回调路径（可能发生）
            opt 收到成功回调
                G->>P: 成功回调
                P->>P: 原子尝试登记成功
                alt 首次登记成功
                    P->>O: 【状态通知】置 paid
                else 成功已登记
                    Note over P: 忽略后到成功，不再次通知
                end
            end
        end

        opt 两次查询均未知，且尚无成功确认
            Note over O,P: 保持 pending，仍接受迟到回调
            G->>P: 迟到的成功回调（若到达）
            P->>P: 原子尝试登记成功
            alt 首次登记成功
                P->>O: 【状态通知】置 paid
            else 成功已登记
                Note over P: 忽略后到成功，不再次通知
            end
        end
    end
```

`par` 表示重试与回调可并发；两条路径共享同一原子成功登记，只有首次成功触发 `paid` 通知。末尾展示回调晚于两次未知查询到达的情形。

### mermaid-diagrams

[原始文件](outputs/mermaid-diagrams/01-concurrent.md)

```mermaid
sequenceDiagram
    autonumber
    participant C as 客户端
    participant O as 订单服务
    participant P as 支付服务
    participant G as 支付渠道

    C->>O: 提交 payment_id
    O->>P: 发起扣款（payment_id）
    P->>G: 请求扣款（payment_id）

    alt 渠道及时返回成功
        G-->>P: 扣款成功
        P->>P: 原子登记一次成功
        P->>O: 状态通知：置 paid
        O-->>C: 支付成功
    else 渠道响应超时
        P->>O: 状态通知：置 pending
        O-->>C: 结果未知
        Note over O,P: 超时不进入 failed

        par 客户端重试路径
            loop 至多两次，使用同一 payment_id
                C->>O: 重试（同一 payment_id）
                O->>P: 转交重试
                P->>G: 查询结果（不再次扣款）
                G-->>P: 查询结果
                alt 查询确认成功
                    P->>P: 原子尝试登记成功
                    alt 首次登记成功
                        P->>O: 状态通知：置 paid
                    else 成功已登记
                        Note over P: 忽略后到成功，不再次通知
                    end
                else 查询结果未知
                    Note over O,P: 未确认成功时保持 pending<br/>若已 paid，不回退
                end
                P-->>O: 返回当前支付状态
                O-->>C: paid 或结果未知
            end
        and 渠道成功回调路径（可能发生）
            opt 渠道发送成功回调
                G-)P: 成功回调（payment_id）
                P->>P: 原子尝试登记成功
                alt 首次登记成功
                    P->>O: 状态通知：置 paid
                else 成功已登记
                    Note over P: 忽略后到成功，不再次通知
                end
            end
        end

        opt 两次查询均未知，且尚未确认成功
            Note over O,P: 保持 pending，仍可接受迟到回调
            opt 之后收到迟到成功回调
                G-)P: 迟到成功回调（payment_id）
                P->>P: 原子尝试登记成功
                alt 首次登记成功
                    P->>O: 状态通知：置 paid
                else 成功已登记
                    Note over P: 忽略后到成功，不再次通知
                end
            end
        end
    end
```

查询与回调可并发；原子登记确保仅首次确认成功时通知订单置 `paid`。两次查询均未知且未收到成功回调时，订单保持 `pending`。

### visual-v041

[原始文件](outputs/visual-v041/01-concurrent.md)

```mermaid
sequenceDiagram
    participant C as 客户端
    participant O as 订单服务
    participant P as 支付服务
    participant G as 支付渠道

    C->>O: 提交 payment_id
    O->>P: 发起扣款
    P->>G: 扣款请求

    alt 渠道及时返回成功
        G-->>P: 扣款成功
        P->>O: 订单状态通知：置 paid
        O-->>C: 支付成功
    else 渠道响应超时
        Note over P,G: 超时不进入 failed
        P->>O: 订单状态通知：置 pending
        O-->>C: 结果未知

        par 客户端重试路径
            loop 至多两次重试，使用同一 payment_id
                C->>O: 重试 payment_id
                O->>P: 转发重试
                P->>G: 结果查询（不再次扣款）
                G-->>P: 查询结果
                alt 查询确认成功
                    P->>P: 原子尝试登记成功
                    alt 首次登记成功
                        P->>O: 订单状态通知：置 paid
                    else 成功已登记
                        Note over P: 忽略后到成功，不再通知订单服务
                    end
                else 查询结果未知
                    Note over P,O: 保持当前订单状态
                end
            end
        and 渠道回调路径（可能发生）
            opt 渠道发送成功回调
                G-)P: 成功回调
                P->>P: 原子尝试登记成功
                alt 首次登记成功
                    P->>O: 订单状态通知：置 paid
                else 成功已登记
                    Note over P: 忽略后到成功，不再通知订单服务
                end
            end
        end

        Note over O,P: 两次查询均未知且未确认成功时，保持 pending
        opt 之后收到迟到的成功回调
            G-)P: 迟到成功回调
            P->>P: 原子尝试登记成功
            alt 首次登记成功
                P->>O: 订单状态通知：置 paid
            else 成功已登记
                Note over P: 忽略后到成功，不再通知订单服务
            end
        end
    end
```

查询与回调可并发；谁先原子登记成功，谁触发唯一一次 `paid` 通知。查询未知不会覆盖已确认的 `paid`。未添加明确失败或退款分支；未运行语法检查或实际渲染。

## 领域数量关系与约束

### show-me

[原始文件](outputs/show-me/02-cardinality.md)

```mermaid
classDiagram
    class 团队
    class 用户
    class 成员资格
    class 项目
    class 任务
    class 分派

    团队 "1" -- "0..*" 成员资格 : 连接
    用户 "1" -- "0..*" 成员资格 : 连接
    团队 "1" -- "0..*" 项目 : 拥有
    项目 "1" -- "0..*" 任务 : 包含
    任务 "1" -- "0..*" 分派 : 连接
    成员资格 "1" -- "0..*" 分派 : 连接

    note for 分派 "成员资格的团队 = 任务所属项目的团队\n同一任务与同一成员资格最多有一个分派"
    note for 成员资格 "用户退出团队时只停用成员资格\n历史分派仍保留"
```

线端的 `1` 表示恰好一个，`0..*` 表示零到多个。图中使用普通关系线；跨关系的团队一致性、分派唯一性及退出后的保留规则由注释补充。未规定团队、项目、任务或用户的删除行为。

### mermaid-diagrams

[原始文件](outputs/mermaid-diagrams/02-cardinality.md)

```mermaid
classDiagram
    class 团队
    class 用户
    class 成员资格
    class 项目
    class 任务
    class 分派

    团队 "1" -- "0..*" 成员资格 : 具有
    用户 "1" -- "0..*" 成员资格 : 具有
    团队 "1" -- "0..*" 项目 : 拥有
    项目 "1" -- "0..*" 任务 : 包含
    任务 "1" -- "0..*" 分派 : 具有
    成员资格 "1" -- "0..*" 分派 : 参与

    note for 分派 "成员资格所属团队必须等于任务所属项目的团队。\n同一任务与同一成员资格最多有一个分派。"
    note for 成员资格 "用户退出团队时仅停用成员资格，历史分派仍保留。"
```

每条线的 `1` 表示另一端的每个实例必须且只关联一个该概念实例；`0..*` 表示可关联零到多个实例。

图中使用普通关联线，不推定生命周期依赖。团队一致性、分派唯一性及退出后的保留规则由注释补充；团队、项目、任务和用户的删除行为均未规定。

### visual-v041

[原始文件](outputs/visual-v041/02-cardinality.md)

```mermaid
classDiagram
    class Team["团队"]
    class User["用户"]
    class Membership["成员资格"]
    class Project["项目"]
    class Task["任务"]
    class Assignment["分派"]

    Team "1" -- "0..*" Membership : 连接
    User "1" -- "0..*" Membership : 连接
    Team "1" -- "0..*" Project : 所属
    Project "1" -- "0..*" Task : 所属
    Task "1" -- "0..*" Assignment : 连接
    Membership "1" -- "0..*" Assignment : 连接

    note for Assignment "成员资格的团队须等于任务所属项目的团队。同一任务与同一成员资格最多有一个分派。"
    note for Membership "用户退出团队时只停用成员资格，历史分派仍保留。"
```

端点的 `1` 表示恰好一个，`0..*` 表示零到多个。图中使用普通关联线；跨关系的团队一致性、分派唯一性和退出后的保留规则由注释补充。

未规定删除团队、项目、任务或用户的行为；本图不表示表结构、外键或级联删除设计。Mermaid 源码未进行工具语法检查或实际渲染。
