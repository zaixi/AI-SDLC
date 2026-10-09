采用 C4 的两层视图：**系统上下文**展示组织归属和跨组织协作；**容器视图**展示本公司内部运行单元，按三个通信场景分别展开。同名节点代表同一个运行单元。

### 系统上下文：组织与系统边界

此层只展示人员和系统，不展开内部容器。

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

### 容器视图：订单发送与交付处理

内部节点均为容器级运行单元，供应商仍以外部系统呈现。箭头表示调用或访问方向：读取指向数据库，消费指向 Kafka；边上的文字说明具体操作。

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

### 容器视图：付款申请与异步结果

采购API写入付款申请事件，付款处理器消费申请并请求银行付款。银行异步结果经回调网关写入 Kafka，再由付款处理器消费并写付款库。

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

### 容器视图：处理状态只读查询

支持工程师只通过管理门户查看处理状态；查询API只读订单库和付款库。

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

订单库、Outbox库、付款库是**三个独立 PostgreSQL 实例**；采购API与查询API是**两个独立部署进程**。未规定的通信协议、Kafka主题和外部系统内部容器未展开，也未添加其他服务或连接。

这四个图块的源码与本轮已看到的渲染版本一致；画面中的关系标签可辨识，未见上一版的文字重叠或过度狭长问题。