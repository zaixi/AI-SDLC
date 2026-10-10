选择两张 C4 视图：**C1 系统上下文图**面向业务负责人，**C2 容器图**面向工程师。均采用文档宽度、自适应高度；以下 Mermaid 块可编辑。

### C1 · 系统与组织边界

此视图把采购协同系统作为整体，展示跨组织通信；不展开内部运行单元。

```mermaid
flowchart LR
    buyer["采购员<br/>【人员】"]
    support["支持工程师<br/>【人员】"]

    subgraph company["本公司"]
        procurement["采购协同系统<br/>【软件系统】"]
    end

    subgraph supplierOrg["合作供应商"]
        supplier["供应商系统<br/>【软件系统】"]
    end

    subgraph bankOrg["银行"]
        bank["付款系统<br/>【软件系统】"]
    end

    buyer -->|"发订单"| procurement
    support -->|"仅通过管理门户查看处理状态"| procurement
    procurement -->|"发送订单"| supplier
    supplier -->|"发送交付事件"| procurement
    procurement -->|"请求付款"| bank
    bank -->|"异步回传付款结果"| procurement
```

### C2 · 本公司系统内部运行单元与关键通信

C4 中的“容器”指独立运行的应用或数据存储，不特指 Docker。系统边界内均为容器级元素；供应商与银行仍以外部系统表示，不展开其内部结构。箭头表示调用、写入或事件传递方向；消费箭头从 Kafka 指向消费者。

```mermaid
flowchart LR
    buyer["采购员<br/>【人员】"]
    support["支持工程师<br/>【人员】"]

    subgraph company["本公司"]
        subgraph procurement["采购协同系统 · 容器边界"]
            web["Web门户<br/>【容器：应用】"]
            api["采购API<br/>【容器：独立部署进程】"]
            orders[("订单库<br/>【容器：PostgreSQL实例 1】")]
            outbox[("Outbox库<br/>【容器：PostgreSQL实例 2】")]
            publisher["事件发布器<br/>【容器：应用】"]

            gateway["回调网关<br/>【容器：应用】"]
            kafka[("内部Kafka<br/>【容器：事件平台】")]
            orderWorker["订单处理器<br/>【容器：应用】"]
            paymentWorker["付款处理器<br/>【容器：应用】"]
            payments[("付款库<br/>【容器：PostgreSQL实例 3】")]

            admin["管理门户<br/>【容器：应用】"]
            query["查询API<br/>【容器：独立部署进程】"]
        end
    end

    subgraph supplierOrg["合作供应商"]
        supplier["供应商系统<br/>【外部软件系统】"]
    end

    subgraph bankOrg["银行"]
        bank["付款系统<br/>【外部软件系统】"]
    end

    buyer -->|"发订单"| web
    web -->|"HTTPS：调用"| api
    api -->|"读写订单"| orders
    api -->|"写待发送事件"| outbox
    publisher -->|"读取事件"| outbox
    publisher -->|"HTTPS：发送订单"| supplier

    supplier -->|"HTTPS：交付事件"| gateway
    bank -->|"HTTPS：异步付款结果"| gateway
    gateway -->|"写事件"| kafka

    kafka -->|"交付事件：订单处理器消费"| orderWorker
    orderWorker -->|"写订单"| orders

    api -->|"写付款申请事件"| kafka
    kafka -->|"付款申请事件：付款处理器消费"| paymentWorker
    paymentWorker -->|"HTTPS：付款请求"| bank
    kafka -->|"付款结果：付款处理器消费"| paymentWorker
    paymentWorker -->|"写付款结果"| payments

    support -->|"仅查看处理状态"| admin
    admin -->|"HTTPS：调用"| query
    query -->|"只读"| orders
    query -->|"只读"| payments
```

三座 PostgreSQL 数据库是**三个独立实例**；采购 API 与查询 API 是**两个独立部署进程**。此处不增加组件级视图，也不补充未规定的协议、Kafka 主题或其他运行单元。