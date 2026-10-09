业务视图把每个组织拥有的系统作为整体；工程视图展开本公司的独立运行单元，供应商和银行系统仍作为外部系统。

### 业务视图：系统与组织边界

```mermaid
C4Context
    title 跨组织采购协作：系统上下文

    Person(buyer, "采购员", "发订单")
    Person(support, "支持工程师", "仅查看处理状态")

    Enterprise_Boundary(company, "本公司") {
        System(procurement, "采购协同系统", "订单协作、付款请求及结果处理")
    }

    Enterprise_Boundary(supplierOrg, "合作供应商") {
        System_Ext(supplier, "供应商系统", "接收订单，发送交付事件")
    }

    Enterprise_Boundary(bankOrg, "银行") {
        System_Ext(bank, "付款系统", "接收付款请求，异步回传付款结果")
    }

    Rel(buyer, procurement, "发订单")
    Rel(support, procurement, "仅查看处理状态")
    Rel(procurement, supplier, "发送订单")
    Rel(supplier, procurement, "发送交付事件")
    Rel(procurement, bank, "请求付款")
    Rel(bank, procurement, "异步回传付款结果")
```

### 工程视图：运行单元与关键通信

每个应用节点表示独立运行单元；三个数据库节点分别表示独立的 PostgreSQL 实例。箭头表示调用或访问方向，因此“读取／消费”的箭头从读取者指向数据源。

```mermaid
C4Container
    title 采购协同系统：容器与通信

    Person(buyer, "采购员", "发订单")
    Person(support, "支持工程师", "仅查看处理状态")

    Container_Boundary(procurement, "本公司 · 采购协同系统") {
        Container(web, "Web门户", "Web应用", "采购员操作入口")
        Container(api, "采购API", "独立部署进程", "处理订单，写入待发送事件及付款申请事件")
        Container(publisher, "事件发布器", "运行进程", "读取待发送事件，发送订单")

        ContainerDb(orders, "订单库", "PostgreSQL · 独立实例一", "保存订单")
        ContainerDb(outbox, "Outbox库", "PostgreSQL · 独立实例二", "保存待发送事件")

        Container(callback, "回调网关", "网关服务", "接收交付事件及付款结果")
        ContainerQueue(kafka, "内部Kafka", "Kafka", "传递交付、付款申请及付款结果事件")
        Container(orderWorker, "订单处理器", "运行进程", "消费交付事件，写入订单库")
        Container(paymentWorker, "付款处理器", "运行进程", "消费付款申请及付款结果，请求付款")

        ContainerDb(payments, "付款库", "PostgreSQL · 独立实例三", "保存付款数据")
        Container(admin, "管理门户", "Web应用", "仅查看处理状态")
        Container(query, "查询API", "独立部署进程", "只读查询订单库与付款库")
    }

    Enterprise_Boundary(supplierOrg, "合作供应商") {
        System_Ext(supplier, "供应商系统", "内部运行单元未规定")
    }

    Enterprise_Boundary(bankOrg, "银行") {
        System_Ext(bank, "付款系统", "内部运行单元未规定")
    }

    Rel(buyer, web, "发订单")
    Rel(web, api, "调用", "HTTPS")
    Rel(api, orders, "读写订单")
    Rel(api, outbox, "写待发送事件")
    Rel(publisher, outbox, "读事件")
    Rel(publisher, supplier, "发送订单", "HTTPS")

    Rel(supplier, callback, "发送交付事件", "HTTPS")
    Rel(bank, callback, "异步回传付款结果", "HTTPS")
    Rel(callback, kafka, "写交付事件及付款结果")
    Rel(orderWorker, kafka, "消费交付事件")
    Rel(orderWorker, orders, "写订单")

    Rel(api, kafka, "写付款申请事件")
    Rel(paymentWorker, kafka, "消费付款申请及付款结果")
    Rel(paymentWorker, bank, "发送付款请求", "HTTPS")
    Rel(paymentWorker, payments, "写付款数据")

    Rel(support, admin, "仅查看处理状态")
    Rel(admin, query, "调用", "HTTPS")
    Rel(query, orders, "只读")
    Rel(query, payments, "只读")
```

除已标明的 HTTPS 外，其余通信协议未规定；Kafka 主题及外部系统内部结构也未规定。以上为可编辑草稿，尚未执行解析器语法检查或实际渲染检查。