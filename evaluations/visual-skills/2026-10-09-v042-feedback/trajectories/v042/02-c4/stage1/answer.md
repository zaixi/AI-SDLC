实际画面中，双向通信标签重叠，部分跨组织连线穿过节点。下面保留原有架构，改用 Mermaid 流程图表达 C4 层级，并将订单发送与交付回调拆开。

**阅读规则：**上下文图只展示人员、系统和组织；容器图只展开本公司系统的运行单元，外部系统保持整体。箭头表示调用或访问方向，读取、写入和消费由标签说明。同名节点在不同视图中代表同一运行单元。

### 1. 系统上下文：组织边界

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

订单库与 Outbox 库分别是独立运行的 PostgreSQL 实例。

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

供应商向回调网关发送交付事件；订单处理器消费内部事件并写订单库。

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

付款处理器消费付款申请和付款结果，向银行发送付款请求，并写入第三个独立 PostgreSQL 实例。

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

支持工程师只通过管理门户查看处理状态。查询API与采购API是两个独立部署进程。

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

未展开供应商或银行内部容器，也未补充未规定的服务、机制或 Kafka 主题。本次修改后的实际排版仍待渲染确认。