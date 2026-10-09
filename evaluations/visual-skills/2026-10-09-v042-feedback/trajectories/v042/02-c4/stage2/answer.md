已检查五张实际渲染图：通信标签已分开，未见连线遮挡关键节点；部分名称有自动换行，但仍可辨认。以下保留已检查的图源码。

**阅读规则：**C4 上下文视图展示人员、系统和组织边界；容器视图展开本公司系统的运行单元，外部系统保持整体。箭头表示调用或访问方向，标签说明读取、写入和消费。同名节点在各图中代表同一运行单元。

### 1. 系统上下文：组织边界

采购协同系统归本公司所有，供应商系统和付款系统分别归合作供应商、银行所有。

```mermaid
flowchart TB
    buyer["【人员】采购员"]
    support["【人员】支持工程师"]

    subgraph company["组织：本公司"]
        procurement["【系统】采购协同系统"]
    end

    subgraph supplierOrg["组织：合作供应商"]
        supplier["【外部系统】供应商系统"]
    end

    subgraph bankOrg["组织：银行"]
        bank["【外部系统】付款系统"]
    end

    buyer -->|"发订单"| procurement
    support -->|"通过管理门户查看处理状态"| procurement
    procurement -->|"HTTPS：发送订单"| supplier
    supplier -->|"HTTPS：发送交付事件"| procurement
    procurement -->|"HTTPS：请求付款"| bank
    bank -->|"HTTPS：异步回传付款结果"| procurement

    classDef person fill:#e8eef7,stroke:#345577,color:#172b4d
    classDef internal fill:#dbeafe,stroke:#2563eb,color:#172b4d
    classDef external fill:#f1f5f9,stroke:#64748b,color:#172b4d
    class buyer,support person
    class procurement internal
    class supplier,bank external
```

### 2. 容器视图：订单发送

采购API读写订单库、写入Outbox库；事件发布器读取Outbox事件，向供应商发送订单。

```mermaid
flowchart LR
    buyer["【人员】采购员"]

    subgraph company["本公司 · 采购协同系统（容器视图：订单发送）"]
        web["【容器】Web门户"]
        api["【容器】采购API<br/>独立部署进程"]
        orders[("【数据容器】订单库<br/>PostgreSQL 实例一")]
        outbox[("【数据容器】Outbox库<br/>PostgreSQL 实例二")]
        publisher["【容器】事件发布器"]

        web -->|"HTTPS：调用"| api
        api -->|"读写订单"| orders
        api -->|"写入待发送事件"| outbox
        publisher -->|"读取事件"| outbox
    end

    supplier["【外部系统】供应商系统<br/>归属：合作供应商"]

    buyer -->|"使用门户发订单"| web
    publisher -->|"HTTPS：发送订单"| supplier
```

### 3. 容器视图：交付事件处理

供应商回调经网关写入Kafka；订单处理器消费交付事件并写订单库。

```mermaid
flowchart LR
    supplier["【外部系统】供应商系统<br/>归属：合作供应商"]

    subgraph company["本公司 · 采购协同系统（容器视图：交付处理）"]
        callback["【容器】回调网关"]
        kafka[("【消息容器】内部Kafka")]
        worker["【容器】订单处理器"]
        orders[("【数据容器】订单库<br/>PostgreSQL 实例一")]

        callback -->|"写入交付事件"| kafka
        worker -->|"消费交付事件"| kafka
        worker -->|"写入订单"| orders
    end

    supplier -->|"HTTPS：发送交付事件"| callback
```

### 4. 容器视图：付款申请与异步结果

付款处理器消费付款申请事件，向银行请求付款；银行异步回传的结果经回调网关进入Kafka，由付款处理器消费并写付款库。

```mermaid
flowchart TB
    subgraph company["本公司 · 采购协同系统（容器视图：付款处理）"]
        api["【容器】采购API<br/>独立部署进程"]
        kafka[("【消息容器】内部Kafka")]
        worker["【容器】付款处理器"]
        callback["【容器】回调网关"]
        payments[("【数据容器】付款库<br/>PostgreSQL 实例三")]

        api -->|"写入付款申请事件"| kafka
        worker -->|"消费付款申请事件<br/>及付款结果"| kafka
        callback -->|"写入付款结果"| kafka
        worker -->|"写入付款数据"| payments
    end

    bank["【外部系统】付款系统<br/>归属：银行"]

    worker -->|"HTTPS：发送付款请求"| bank
    bank -->|"HTTPS：异步回传付款结果"| callback
```

### 5. 容器视图：支持工程师只读查询

支持工程师只通过管理门户查看处理状态；查询API只读订单库与付款库。

```mermaid
flowchart LR
    support["【人员】支持工程师"]

    subgraph company["本公司 · 采购协同系统（容器视图：状态查询）"]
        admin["【容器】管理门户"]
        query["【容器】查询API<br/>独立部署进程"]
        orders[("【数据容器】订单库<br/>PostgreSQL 实例一")]
        payments[("【数据容器】付款库<br/>PostgreSQL 实例三")]

        admin -->|"HTTPS：调用"| query
        query -->|"只读订单数据"| orders
        query -->|"只读付款数据"| payments
    end

    support -->|"查看处理状态"| admin
```

| 部署边界 | 已确认事实 |
|---|---|
| 采购API、查询API | 两个独立部署进程 |
| 订单库、Outbox库、付款库 | 三个独立运行的PostgreSQL实例 |
| 内部Kafka、回调网关 | 各容器视图中重复出现的是同一运行单元 |
| 供应商系统、银行付款系统 | 内部容器未规定，保持外部系统层级 |

图中未补充缓存、身份服务、补偿或重试机制，也未指定Kafka主题。