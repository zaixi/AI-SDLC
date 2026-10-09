组织边界用上下文图说明；内部运行单元用三张容器视图展开。三张容器图中的同名节点是同一个运行单元，按业务链路重复展示。箭头表示调用或访问方向，标签区分写入、读取与消费。

### 系统上下文：组织归属与跨组织通信

```mermaid
C4Context
    title 跨组织集成：系统与组织边界

    Person(buyer, "采购员", "发订单")
    Person(support, "支持工程师", "仅查看处理状态")

    Enterprise_Boundary(company, "本公司") {
        System(procurement, "采购协同系统", "订单协同与付款处理")
    }
    Enterprise_Boundary(supplierOrg, "合作供应商") {
        System_Ext(supplier, "供应商系统", "接收订单、发送交付事件")
    }
    Enterprise_Boundary(bankOrg, "银行") {
        System_Ext(bank, "付款系统", "接收付款请求、异步回传结果")
    }

    Rel(buyer, procurement, "发订单")
    Rel(support, procurement, "通过管理门户查看处理状态")
    Rel(procurement, supplier, "发送订单", "HTTPS")
    Rel(supplier, procurement, "发送交付事件", "HTTPS")
    Rel(procurement, bank, "请求付款", "HTTPS")
    Rel(bank, procurement, "异步回传付款结果", "HTTPS")
```

### 容器视图：订单发送与交付处理

供应商系统保持系统级外部节点，不展开其内部容器。

```mermaid
C4Container
    title 采购协同系统：订单与交付链路

    Person(buyer, "采购员", "发订单")
    System_Ext(supplier, "供应商系统（合作供应商）", "接收订单、发送交付事件")

    Container_Boundary(company, "本公司：采购协同系统") {
        Container(web, "Web门户", "Web应用", "采购操作入口")
        Container(api, "采购API", "独立部署进程", "处理订单与付款申请")
        ContainerDb(orders, "订单库", "PostgreSQL实例一", "存储订单")
        ContainerDb(outbox, "Outbox库", "PostgreSQL实例二", "存储待发送事件")
        Container(publisher, "事件发布器", "运行进程", "读取事件并发送订单")
        Container(callback, "回调网关", "运行单元", "接收外部回调")
        ContainerQueue(kafka, "内部Kafka", "Kafka", "传递内部事件")
        Container(orderWorker, "订单处理器", "运行进程", "消费交付事件并更新订单")
    }

    Rel(buyer, web, "使用门户发订单")
    Rel(web, api, "调用", "HTTPS")
    Rel(api, orders, "读写订单")
    Rel(api, outbox, "写入待发送事件")
    Rel(publisher, outbox, "读取事件")
    Rel(publisher, supplier, "发送订单", "HTTPS")
    Rel(supplier, callback, "发送交付事件", "HTTPS")
    Rel(callback, kafka, "写入交付事件")
    Rel(orderWorker, kafka, "消费交付事件")
    Rel(orderWorker, orders, "写入订单")
```

### 容器视图：付款申请与异步结果

付款处理器同时消费付款申请事件和付款结果；付款结果经回调网关进入内部 Kafka。

```mermaid
C4Container
    title 采购协同系统：付款链路

    System_Ext(bank, "付款系统（银行）", "接收请求、异步回传付款结果")

    Container_Boundary(company, "本公司：采购协同系统") {
        Container(api, "采购API", "独立部署进程", "发起付款申请事件")
        ContainerQueue(kafka, "内部Kafka", "Kafka", "传递内部事件")
        Container(paymentWorker, "付款处理器", "运行进程", "处理付款申请与付款结果")
        Container(callback, "回调网关", "运行单元", "接收外部回调")
        ContainerDb(payments, "付款库", "PostgreSQL实例三", "存储付款数据")
    }

    Rel(api, kafka, "写入付款申请事件")
    Rel(paymentWorker, kafka, "消费付款申请事件与付款结果")
    Rel(paymentWorker, bank, "发送付款请求", "HTTPS")
    Rel(bank, callback, "异步回传付款结果", "HTTPS")
    Rel(callback, kafka, "写入付款结果")
    Rel(paymentWorker, payments, "写入付款数据")
```

### 容器视图：支持工程师只读查询

查询API与采购API是两个独立部署进程。订单库、Outbox库、付款库分别是三个独立运行的 PostgreSQL 实例。

```mermaid
C4Container
    title 采购协同系统：处理状态查询

    Person(support, "支持工程师", "仅查看处理状态")

    Container_Boundary(company, "本公司：采购协同系统") {
        Container(admin, "管理门户", "Web应用", "处理状态查看入口")
        Container(query, "查询API", "独立部署进程", "只读查询订单与付款数据")
        ContainerDb(orders, "订单库", "PostgreSQL实例一", "存储订单")
        ContainerDb(payments, "付款库", "PostgreSQL实例三", "存储付款数据")
    }

    Rel(support, admin, "查看处理状态")
    Rel(admin, query, "调用", "HTTPS")
    Rel(query, orders, "只读订单数据")
    Rel(query, payments, "只读付款数据")
```

以上为可编辑初稿，尚未检查实际渲染画面。