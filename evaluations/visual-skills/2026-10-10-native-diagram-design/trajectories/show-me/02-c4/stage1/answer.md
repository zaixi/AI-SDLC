采用 **C1 系统上下文图 + C2 容器图的三个局部视图**，均为文档宽度、自适应高度。将订单、付款、状态查询分别展开，改善上一版标签重叠与容器图文字过小的问题。各局部视图中的同名节点表示同一个运行单元。

### C1 · 系统与组织边界

面向业务负责人：本公司、合作供应商、银行各自拥有自己的系统。

```mermaid
flowchart TB
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
    support -->|"通过管理门户查看处理状态"| procurement

    procurement -->|"发送订单"| supplier
    supplier -->|"交付事件"| procurement
    procurement -->|"付款请求"| bank
    bank -->|"异步付款结果"| procurement
```

### C2 · 订单发送与交付处理

面向工程师：采购 API 写入订单与待发送事件；事件发布器读取 Outbox，向供应商发送订单。交付事件经回调网关、Kafka 到达订单处理器。

```mermaid
flowchart TB
    buyer["采购员<br/>【人员】"]

    subgraph company["本公司"]
        subgraph procurement["采购协同系统 · 订单局部视图"]
            web["Web门户<br/>【容器：应用】"]
            api["采购API<br/>【容器：独立部署进程】"]
            orders[("订单库<br/>【容器：PostgreSQL实例 1】")]
            outbox[("Outbox库<br/>【容器：PostgreSQL实例 2】")]
            publisher["事件发布器<br/>【容器：应用】"]
            gateway["回调网关<br/>【容器：应用】"]
            kafka[("内部Kafka<br/>【容器：事件平台】")]
            worker["订单处理器<br/>【容器：应用】"]

            web -->|"HTTPS：调用"| api
            api -->|"读写订单"| orders
            api -->|"写待发送事件"| outbox
            publisher -->|"读取事件"| outbox
            gateway -->|"写事件"| kafka
            kafka -->|"消费交付事件"| worker
            worker -->|"写订单"| orders
        end
    end

    subgraph supplierOrg["合作供应商"]
        supplier["供应商系统<br/>【外部软件系统】"]
    end

    buyer -->|"发订单"| web
    publisher -->|"HTTPS：发送订单"| supplier
    supplier -->|"HTTPS：交付事件"| gateway
```

### C2 · 付款申请与异步结果

采购 API 向 Kafka 写付款申请事件；付款处理器消费申请并调用银行。银行异步回传结果，经回调网关与 Kafka 交给付款处理器写入付款库。

```mermaid
flowchart TB
    subgraph company["本公司"]
        subgraph procurement["采购协同系统 · 付款局部视图"]
            api["采购API<br/>【容器：独立部署进程】"]
            kafka[("内部Kafka<br/>【容器：事件平台】")]
            worker["付款处理器<br/>【容器：应用】"]
            gateway["回调网关<br/>【容器：应用】"]
            payments[("付款库<br/>【容器：PostgreSQL实例 3】")]

            api -->|"写付款申请事件"| kafka
            kafka -->|"消费付款申请事件"| worker
            gateway -->|"写事件"| kafka
            kafka -->|"消费付款结果"| worker
            worker -->|"写付款结果"| payments
        end
    end

    subgraph bankOrg["银行"]
        bank["付款系统<br/>【外部软件系统】"]
    end

    worker -->|"HTTPS：付款请求"| bank
    bank -->|"HTTPS：异步付款结果"| gateway
```

### C2 · 处理状态查询

支持工程师只通过管理门户查看处理状态；查询 API 只读订单库与付款库。

```mermaid
flowchart TB
    support["支持工程师<br/>【人员】"]

    subgraph company["本公司"]
        subgraph procurement["采购协同系统 · 查询局部视图"]
            admin["管理门户<br/>【容器：应用】"]
            query["查询API<br/>【容器：独立部署进程】"]
            orders[("订单库<br/>【容器：PostgreSQL实例 1】")]
            payments[("付款库<br/>【容器：PostgreSQL实例 3】")]

            admin -->|"HTTPS：调用"| query
            query -->|"只读"| orders
            query -->|"只读"| payments
        end
    end

    support -->|"查看处理状态"| admin
```

C2 中的“容器”表示独立运行的应用或数据存储。**订单库、Outbox 库、付款库是三个独立 PostgreSQL 实例；采购 API 与查询 API 是两个独立部署进程。**读取箭头由读取方指向数据库；Kafka 箭头指向消费者。供应商与银行保留在系统级，未展开其内部容器。