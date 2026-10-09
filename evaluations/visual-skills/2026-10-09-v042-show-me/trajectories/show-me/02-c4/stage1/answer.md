### C1：系统与组织边界

业务负责人关注系统归属与跨组织往来。系统间的连线表示业务通信，内部执行单元在 C2 展开。

```mermaid
---
config:
  flowchart:
    nodeSpacing: 70
    rankSpacing: 90
    curve: basis
---
flowchart TB
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
    supplier -->|"交付事件"| procurement
    procurement -->|"请求付款"| bank
    bank -->|"异步付款结果"| procurement
```

### C2：内部运行单元与关键通信

为减少交叉线，将同一容器视图按业务链路拆为三个局部视图。**同名节点代表同一个运行单元**；外部系统保持系统层级，位于本公司边界之外。

容器指运行中的应用或数据存储，不限定为 Docker 容器。数据库箭头表示访问方向；Kafka 的“消费”箭头从消费者指向 Kafka，表示读取事件。

#### 订单发送与交付处理

```mermaid
---
config:
  flowchart:
    nodeSpacing: 45
    rankSpacing: 65
---
flowchart TB
    buyer["采购员<br/>人员"]

    subgraph company["本公司"]
        subgraph procurement["采购协同系统 · 容器"]
            web["Web门户<br/>应用"]
            api["采购API<br/>独立部署进程"]
            orders[("订单库<br/>PostgreSQL 实例 1")]
            outbox[("Outbox库<br/>PostgreSQL 实例 2")]
            publisher["事件发布器<br/>应用"]
            gateway["回调网关<br/>应用"]
            kafka[("内部Kafka<br/>事件基础设施")]
            processor["订单处理器<br/>应用"]

            web -->|"HTTPS：调用"| api
            api -->|"读写订单"| orders
            api -->|"写待发送事件"| outbox
            publisher -->|"读取事件"| outbox
            gateway -->|"写事件"| kafka
            processor -->|"消费交付事件"| kafka
            processor -->|"写订单"| orders
        end
    end

    subgraph supplierOrg["合作供应商"]
        supplier["供应商系统<br/>外部软件系统"]
    end

    buyer -->|"发订单"| web
    publisher -->|"HTTPS：发送订单"| supplier
    supplier -->|"HTTPS：交付事件"| gateway
```

#### 付款申请与异步结果

采购API写入付款申请事件；付款处理器消费申请并向银行请求付款。银行结果经回调网关进入 Kafka，由付款处理器消费并落库。

```mermaid
---
config:
  flowchart:
    nodeSpacing: 55
    rankSpacing: 70
---
flowchart TB
    subgraph company["本公司"]
        subgraph procurement["采购协同系统 · 容器"]
            api["采购API<br/>独立部署进程"]
            kafka[("内部Kafka<br/>事件基础设施")]
            processor["付款处理器<br/>应用"]
            gateway["回调网关<br/>应用"]
            payments[("付款库<br/>PostgreSQL 实例 3")]

            api -->|"写付款申请事件"| kafka
            processor -->|"消费付款申请事件<br/>及付款结果"| kafka
            gateway -->|"写事件"| kafka
            processor -->|"写付款结果"| payments
        end
    end

    subgraph bankOrg["银行"]
        bank["付款系统<br/>外部软件系统"]
    end

    processor -->|"HTTPS：付款请求"| bank
    bank -->|"HTTPS：异步付款结果"| gateway
```

#### 处理状态查询

支持工程师仅通过管理门户查看状态，查询API只读订单库与付款库。

```mermaid
flowchart TB
    support["支持工程师<br/>人员"]

    subgraph company["本公司"]
        subgraph procurement["采购协同系统 · 容器"]
            admin["管理门户<br/>应用"]
            query["查询API<br/>独立部署进程"]
            orders[("订单库<br/>PostgreSQL 实例 1")]
            payments[("付款库<br/>PostgreSQL 实例 3")]

            admin -->|"HTTPS：调用"| query
            query -->|"只读"| orders
            query -->|"只读"| payments
        end
    end

    support -->|"仅查看处理状态"| admin
```

采购API与查询API分别独立部署；订单库、Outbox库、付款库是三个独立 PostgreSQL 实例。以上视图只展开到容器层，不引入组件、外部系统内部结构或 Kafka 主题。