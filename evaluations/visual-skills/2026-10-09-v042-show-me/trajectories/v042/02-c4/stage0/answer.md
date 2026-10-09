以下按 C4 的系统上下文层和容器层展开。容器指独立运行单元；重复出现的同名容器是同一单元。容器图箭头表示调用或读写的发起方向，“消费”表示从 Kafka 读取事件。

### 1. 系统上下文：组织归属与跨组织通信

采购协同系统属于本公司；供应商系统和付款系统分别属于合作供应商和银行。

```mermaid
C4Context
    title 系统上下文：组织边界

    Person(buyer, "采购员", "发订单")
    Person(support, "支持工程师", "只查看处理状态")

    Enterprise_Boundary(company, "本公司") {
        System(procurement, "采购协同系统", "订单协同与付款处理")
    }
    Enterprise_Boundary(supplierOrg, "合作供应商") {
        System(supplier, "供应商系统", "接收订单、发送交付事件")
    }
    Enterprise_Boundary(bankOrg, "银行") {
        System(bank, "付款系统", "接收付款请求、异步回传结果")
    }

    Rel(buyer, procurement, "发订单")
    Rel(support, procurement, "只查看处理状态")
    Rel(procurement, supplier, "发送订单")
    Rel(supplier, procurement, "发送交付事件")
    Rel(procurement, bank, "请求付款")
    Rel(bank, procurement, "异步回传付款结果")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="3")
```

### 2. 容器视图：订单发送与交付处理

订单库与 Outbox 库是两个独立 PostgreSQL 实例。事件发布器读取 Outbox；交付事件经过回调网关与 Kafka，由订单处理器写入订单库。

```mermaid
C4Container
    title 容器视图：订单发送与交付处理

    Person(buyer, "采购员", "发订单")
    System_Ext(supplier, "供应商系统", "归属合作供应商；内部未展开")

    Container_Boundary(procurement, "本公司 · 采购协同系统") {
        Container(web, "Web门户", "技术未指定", "采购员操作入口")
        Container(api, "采购API", "独立部署进程", "订单读写、写待发送事件")
        ContainerDb(orderDb, "订单库", "PostgreSQL · 独立实例①", "存储订单")
        ContainerDb(outboxDb, "Outbox库", "PostgreSQL · 独立实例②", "存储待发送事件")
        Container(publisher, "事件发布器", "技术未指定", "读取事件并发送订单")
        Container(callback, "回调网关", "技术未指定", "接收外部回调并写事件")
        ContainerQueue(kafka, "内部Kafka", "Kafka", "承载内部事件")
        Container(orderWorker, "订单处理器", "技术未指定", "消费交付事件并写订单")
    }

    Rel(buyer, web, "发订单")
    Rel(web, api, "调用", "HTTPS")
    Rel(api, orderDb, "读写订单")
    Rel(api, outboxDb, "写待发送事件")
    Rel(publisher, outboxDb, "读事件")
    Rel(publisher, supplier, "发送订单", "HTTPS")
    Rel(supplier, callback, "发送交付事件", "HTTPS")
    Rel(callback, kafka, "写交付事件")
    Rel(orderWorker, kafka, "消费交付事件")
    Rel(orderWorker, orderDb, "写订单")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

### 3. 容器视图：付款申请与异步结果

采购API写付款申请事件，付款处理器消费后向银行请求付款。银行异步回传结果，经回调网关与 Kafka，由付款处理器写入第三个独立 PostgreSQL 实例。

```mermaid
C4Container
    title 容器视图：付款申请与异步结果

    System_Ext(bank, "付款系统", "归属银行；内部未展开")

    Container_Boundary(procurement, "本公司 · 采购协同系统") {
        Container(api, "采购API", "独立部署进程", "写付款申请事件")
        ContainerQueue(kafka, "内部Kafka", "Kafka", "承载内部事件")
        Container(paymentWorker, "付款处理器", "技术未指定", "消费付款申请和付款结果")
        Container(callback, "回调网关", "技术未指定", "接收外部回调并写事件")
        ContainerDb(paymentDb, "付款库", "PostgreSQL · 独立实例③", "存储付款处理数据")
    }

    Rel(api, kafka, "写付款申请事件")
    Rel(paymentWorker, kafka, "消费付款申请事件及付款结果")
    Rel(paymentWorker, bank, "发送付款请求", "HTTPS")
    Rel(bank, callback, "异步回传付款结果", "HTTPS")
    Rel(callback, kafka, "写付款结果事件")
    Rel(paymentWorker, paymentDb, "写付款数据")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

### 4. 容器视图：支持工程师只读查询

支持工程师只通过管理门户查看处理状态。查询API与采购API是两个独立部署进程；查询API只读订单库和付款库。

```mermaid
C4Container
    title 容器视图：处理状态查询

    Person(support, "支持工程师", "只查看处理状态")

    Container_Boundary(procurement, "本公司 · 采购协同系统") {
        Container(admin, "管理门户", "技术未指定", "处理状态查看入口")
        Container(queryApi, "查询API", "独立部署进程", "与采购API分别部署；只读查询")
        ContainerDb(orderDb, "订单库", "PostgreSQL · 独立实例①", "存储订单")
        ContainerDb(paymentDb, "付款库", "PostgreSQL · 独立实例③", "存储付款处理数据")
    }

    Rel(support, admin, "查看处理状态")
    Rel(admin, queryApi, "调用", "HTTPS")
    Rel(queryApi, orderDb, "只读")
    Rel(queryApi, paymentDb, "只读")

    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")
```

以上为可编辑草稿，尚未检查实际渲染画面。