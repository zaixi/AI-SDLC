两张视图分别展示 **C1 系统上下文**与 **C2 容器**。这里的“容器”指独立运行的应用或数据存储，不限定为 Docker 容器。

### C1：系统与组织边界

面向业务负责人：明确系统归属，以及跨组织的业务往来。此层的系统间连线表示整体业务通信，具体执行单元见 C2。

```mermaid
flowchart LR
    buyer["采购员<br/>人员"]
    support["支持工程师<br/>人员"]

    subgraph company["本公司"]
        procurement["采购协同系统<br/>软件系统"]
    end

    subgraph supplierOrg["合作供应商"]
        supplier["供应商系统<br/>软件系统"]
    end

    subgraph bankOrg["银行"]
        bank["付款系统<br/>软件系统"]
    end

    buyer -->|"发订单"| procurement
    support -->|"仅查看处理状态"| procurement
    procurement -->|"发送订单"| supplier
    supplier -->|"发送交付事件"| procurement
    procurement -->|"请求付款"| bank
    bank -->|"异步回传付款结果"| procurement
```

### C2：采购协同系统内部运行单元与通信

面向工程师：展开本公司系统的容器；供应商与银行仍保留为外部软件系统，不推定其内部结构。箭头表示调用、投递或数据访问方向；“读取／消费”箭头从执行该操作的容器指向数据源。

```mermaid
flowchart TB
    buyer["采购员<br/>人员"]
    support["支持工程师<br/>人员"]

    subgraph company["本公司"]
        subgraph procurement["采购协同系统 · 容器视图"]
            web["Web门户<br/>容器：应用"]
            purchaseApi["采购API<br/>容器：独立部署进程"]
            orderDb[("订单库<br/>容器：PostgreSQL 独立实例 1")]
            outboxDb[("Outbox库<br/>容器：PostgreSQL 独立实例 2")]
            publisher["事件发布器<br/>容器：应用"]

            callback["回调网关<br/>容器：应用"]
            kafka[("内部Kafka<br/>容器：事件基础设施")]
            orderProcessor["订单处理器<br/>容器：应用"]
            paymentProcessor["付款处理器<br/>容器：应用"]
            paymentDb[("付款库<br/>容器：PostgreSQL 独立实例 3")]

            admin["管理门户<br/>容器：应用"]
            queryApi["查询API<br/>容器：独立部署进程"]
        end
    end

    subgraph supplierOrg["合作供应商"]
        supplier["供应商系统<br/>外部软件系统"]
    end

    subgraph bankOrg["银行"]
        bank["付款系统<br/>外部软件系统"]
    end

    buyer -->|"发订单"| web
    web -->|"HTTPS：调用"| purchaseApi
    purchaseApi -->|"读写订单"| orderDb
    purchaseApi -->|"写待发送事件"| outboxDb
    publisher -->|"读取事件"| outboxDb
    publisher -->|"HTTPS：发送订单"| supplier

    supplier -->|"HTTPS：发送交付事件"| callback
    bank -->|"HTTPS：异步回传付款结果"| callback
    callback -->|"写事件"| kafka

    orderProcessor -->|"消费交付事件"| kafka
    orderProcessor -->|"写订单"| orderDb

    purchaseApi -->|"写付款申请事件"| kafka
    paymentProcessor -->|"消费付款申请事件及付款结果"| kafka
    paymentProcessor -->|"HTTPS：发送付款请求"| bank
    paymentProcessor -->|"写付款结果"| paymentDb

    support -->|"仅查看处理状态"| admin
    admin -->|"HTTPS：调用"| queryApi
    queryApi -->|"只读"| orderDb
    queryApi -->|"只读"| paymentDb
```

采购API与查询API是两个独立部署进程；三个 PostgreSQL 库分别是独立实例。图中未展开组件层，也未添加未规定的内部容器、主题或通信。