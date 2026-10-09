上次渲染中，双向关系的文字重叠，完整容器图也过于狭长。下面保留 C4 的系统上下文与容器层级，采用 Mermaid 流程图排版，并把容器视图分为三个通信场景。同名节点均代表同一个运行单元。

### 系统上下文：组织各自拥有什么

本图只展示人员、系统和组织边界，不展开系统内部。

```mermaid
flowchart TB
    buyer["采购员<br/>【人员】"]
    support["支持工程师<br/>【人员】"]

    subgraph company["本公司"]
        procurement["采购协同系统<br/>【系统】"]
    end

    subgraph supplierOrg["合作供应商"]
        supplier["供应商系统<br/>【外部系统】"]
    end

    subgraph bankOrg["银行"]
        bank["付款系统<br/>【外部系统】"]
    end

    buyer -->|"发订单"| procurement
    support -->|"仅查看处理状态"| procurement
    procurement -->|"发送订单"| supplier
    supplier -->|"发送交付事件"| procurement
    procurement -->|"请求付款"| bank
    bank -->|"异步回传付款结果"| procurement

    classDef person fill:#e8f0fa,stroke:#375a7f,color:#16324f
    classDef internal fill:#daeaff,stroke:#2463a6,color:#16324f
    classDef external fill:#eeeeee,stroke:#666666,color:#222222
    class buyer,support person
    class procurement internal
    class supplier,bank external
```

### 容器视图一：订单发送与交付处理

本公司边界内的节点均为容器级运行单元。数据库访问箭头从访问者指向数据库；消费箭头从消费者指向 Kafka。

```mermaid
flowchart LR
    buyer["采购员<br/>【人员】"]

    subgraph company["本公司 · 采购协同系统"]
        web["Web门户<br/>【容器】"]
        api["采购API<br/>【容器 · 独立部署进程】"]
        orders[("订单库<br/>【数据库容器】<br/>PostgreSQL 实例一")]
        outbox[("Outbox库<br/>【数据库容器】<br/>PostgreSQL 实例二")]
        publisher["事件发布器<br/>【容器】"]
        callback["回调网关<br/>【容器】"]
        kafka[["内部Kafka<br/>【消息容器】"]]
        worker["订单处理器<br/>【容器】"]

        web -->|"HTTPS · 调用"| api
        api -->|"读写订单"| orders
        api -->|"写待发送事件"| outbox
        publisher -->|"读事件"| outbox
        callback -->|"写交付事件"| kafka
        worker -->|"消费交付事件"| kafka
        worker -->|"写订单"| orders
    end

    subgraph supplierOrg["合作供应商"]
        supplier["供应商系统<br/>【外部系统】"]
    end

    buyer -->|"发订单"| web
    publisher -->|"HTTPS · 发送订单"| supplier
    supplier -->|"HTTPS · 发送交付事件"| callback
```

### 容器视图二：付款申请与异步结果

付款处理器同时消费付款申请和付款结果；付款请求由付款处理器发送，异步结果通过回调网关进入 Kafka。

```mermaid
flowchart LR
    subgraph company["本公司 · 采购协同系统"]
        api["采购API<br/>【容器 · 独立部署进程】"]
        kafka[["内部Kafka<br/>【消息容器】"]]
        worker["付款处理器<br/>【容器】"]
        callback["回调网关<br/>【容器】"]
        payments[("付款库<br/>【数据库容器】<br/>PostgreSQL 实例三")]

        api -->|"写付款申请事件"| kafka
        worker -->|"消费付款申请及付款结果"| kafka
        callback -->|"写付款结果"| kafka
        worker -->|"写付款数据"| payments
    end

    subgraph bankOrg["银行"]
        bank["付款系统<br/>【外部系统】"]
    end

    worker -->|"HTTPS · 发送付款请求"| bank
    bank -->|"HTTPS · 异步回传付款结果"| callback
```

### 容器视图三：支持工程师只读查询

支持工程师仅通过管理门户查看处理状态。查询API与采购API为两个独立部署进程。

```mermaid
flowchart LR
    support["支持工程师<br/>【人员】"]

    subgraph company["本公司 · 采购协同系统"]
        admin["管理门户<br/>【容器】"]
        query["查询API<br/>【容器 · 独立部署进程】"]
        orders[("订单库<br/>【数据库容器】<br/>PostgreSQL 实例一")]
        payments[("付款库<br/>【数据库容器】<br/>PostgreSQL 实例三")]

        admin -->|"HTTPS · 调用"| query
        query -->|"只读"| orders
        query -->|"只读"| payments
    end

    support -->|"仅查看处理状态"| admin
```

订单库、Outbox库、付款库是三个独立的 PostgreSQL 实例。未规定的协议、Kafka 主题及供应商／银行内部结构均未展开，也未补入其他服务或通信。

上一版已成功渲染；本版调整后的源码尚未进行解析器检查或实际渲染验证。