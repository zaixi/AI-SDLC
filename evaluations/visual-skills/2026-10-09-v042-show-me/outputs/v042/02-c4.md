已检查本轮五张实际画面：文字可读，通信标签没有明显重叠，连线未遮挡关键节点。以下保留已检查的图源码。

图按 **C4 系统上下文层、容器层**组织，以 Mermaid 流程图语法表达。容器是独立运行单元；不同图中的同名容器代表同一个单元。容器图箭头表示调用或读写的发起方向，“读”和“消费”指向数据源。

### 1. 系统上下文：组织边界

采购协同系统属于本公司；供应商系统、付款系统分别属于合作供应商和银行。

```mermaid
flowchart TB
    buyer["采购员<br/>【人员】"]
    support["支持工程师<br/>【人员】"]

    subgraph company["本公司"]
        procurement["采购协同系统<br/>【系统】"]
    end
    subgraph supplierOrg["合作供应商"]
        supplier["供应商系统<br/>【系统】"]
    end
    subgraph bankOrg["银行"]
        bank["付款系统<br/>【系统】"]
    end

    buyer -->|"发订单"| procurement
    support -->|"只查看处理状态"| procurement
    procurement -->|"发送订单"| supplier
    supplier -->|"发送交付事件"| procurement
    procurement -->|"请求付款"| bank
    bank -->|"异步回传付款结果"| procurement

    classDef person fill:#08427b,color:#fff,stroke:#052e56
    classDef system fill:#1168bd,color:#fff,stroke:#08427b
    class buyer,support person
    class procurement,supplier,bank system
```

### 2. 容器视图：订单发送

采购API读写订单库，向 Outbox 库写待发送事件；事件发布器读取 Outbox 后向供应商发送订单。订单库与 Outbox 库是两个独立 PostgreSQL 实例。

```mermaid
flowchart TB
    buyer["采购员<br/>【人员】"]

    subgraph company["本公司 · 采购协同系统边界"]
        web["Web门户<br/>【容器】"]
        api["采购API<br/>【容器 · 独立部署进程】"]
        orderDb[("订单库<br/>【容器 · PostgreSQL实例①】")]
        outboxDb[("Outbox库<br/>【容器 · PostgreSQL实例②】")]
        publisher["事件发布器<br/>【容器】"]

        web -->|"HTTPS · 调用"| api
        api -->|"读写订单"| orderDb
        api -->|"写待发送事件"| outboxDb
        publisher -->|"读事件"| outboxDb
    end

    subgraph supplierOrg["合作供应商"]
        supplier["供应商系统<br/>【外部系统】"]
    end

    buyer -->|"发订单"| web
    publisher -->|"HTTPS · 发送订单"| supplier

    classDef person fill:#08427b,color:#fff,stroke:#052e56
    classDef container fill:#e8f1fb,color:#16324f,stroke:#3978b8
    classDef external fill:#eeeeee,color:#333,stroke:#777
    class buyer person
    class web,api,orderDb,outboxDb,publisher container
    class supplier external
```

### 3. 容器视图：交付事件处理

供应商向回调网关发送交付事件；网关写入 Kafka，订单处理器消费事件并写订单库。

```mermaid
flowchart LR
    subgraph supplierOrg["合作供应商"]
        supplier["供应商系统<br/>【外部系统】"]
    end

    subgraph company["本公司 · 采购协同系统边界"]
        callback["回调网关<br/>【容器】"]
        kafka[("内部Kafka<br/>【容器 · 消息基础设施】")]
        orderWorker["订单处理器<br/>【容器】"]
        orderDb[("订单库<br/>【容器 · PostgreSQL实例①】")]

        callback -->|"写交付事件"| kafka
        orderWorker -->|"消费交付事件"| kafka
        orderWorker -->|"写订单"| orderDb
    end

    supplier -->|"HTTPS · 发送交付事件"| callback

    classDef container fill:#e8f1fb,color:#16324f,stroke:#3978b8
    classDef external fill:#eeeeee,color:#333,stroke:#777
    class callback,kafka,orderWorker,orderDb container
    class supplier external
```

### 4. 容器视图：付款申请与异步结果

付款处理器消费采购API写入的付款申请，向银行请求付款。银行异步回传结果，经回调网关写入 Kafka，由付款处理器消费并写付款库。

```mermaid
flowchart TB
    subgraph company["本公司 · 采购协同系统边界"]
        api["采购API<br/>【容器 · 独立部署进程】"]
        kafka[("内部Kafka<br/>【容器 · 消息基础设施】")]
        paymentWorker["付款处理器<br/>【容器】"]
        callback["回调网关<br/>【容器】"]
        paymentDb[("付款库<br/>【容器 · PostgreSQL实例③】")]

        api -->|"写付款申请事件"| kafka
        paymentWorker -->|"消费付款申请事件<br/>及付款结果"| kafka
        callback -->|"写付款结果事件"| kafka
        paymentWorker -->|"写付款数据"| paymentDb
    end

    subgraph bankOrg["银行"]
        bank["付款系统<br/>【外部系统】"]
    end

    paymentWorker -->|"HTTPS · 发送付款请求"| bank
    bank -->|"HTTPS · 异步回传付款结果"| callback

    classDef container fill:#e8f1fb,color:#16324f,stroke:#3978b8
    classDef external fill:#eeeeee,color:#333,stroke:#777
    class api,kafka,paymentWorker,callback,paymentDb container
    class bank external
```

### 5. 容器视图：只读查看处理状态

支持工程师只通过管理门户查看状态。查询API与采购API分别部署，只读订单库与付款库。

```mermaid
flowchart TB
    support["支持工程师<br/>【人员】"]

    subgraph company["本公司 · 采购协同系统边界"]
        admin["管理门户<br/>【容器】"]
        queryApi["查询API<br/>【容器 · 独立部署进程】<br/>与采购API分别部署"]
        orderDb[("订单库<br/>【容器 · PostgreSQL实例①】")]
        paymentDb[("付款库<br/>【容器 · PostgreSQL实例③】")]

        admin -->|"HTTPS · 调用"| queryApi
        queryApi -->|"只读"| orderDb
        queryApi -->|"只读"| paymentDb
    end

    support -->|"查看处理状态"| admin

    classDef person fill:#08427b,color:#fff,stroke:#052e56
    classDef container fill:#e8f1fb,color:#16324f,stroke:#3978b8
    class support person
    class admin,queryApi,orderDb,paymentDb container
```

三个 PostgreSQL 实例彼此独立。供应商和银行的内部结构保持未展开；未指定的内部协议、Kafka 主题及其他机制均未补充。