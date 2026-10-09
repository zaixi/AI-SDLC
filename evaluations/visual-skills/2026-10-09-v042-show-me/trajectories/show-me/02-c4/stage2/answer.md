已查看四张渲染图：通信标签可辨，组织边界清楚。以下保留已检查的图源码。

### C1：系统与组织边界

面向业务负责人：展示系统归属与跨组织往来。连线表示系统层面的业务通信，具体执行单元见 C2。

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

面向工程师：将采购协同系统的容器视图按业务链路分成三个局部视图。**同名节点是同一个运行单元，三个视图合起来覆盖全部已确认通信。**

系统边界内的应用、进程和数据存储均为 C4 容器；供应商与银行保持为边界外的软件系统。数据库箭头表示访问方向；“消费”箭头从消费者指向 Kafka，表示读取事件。

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

采购API写入付款申请事件；付款处理器消费申请并请求银行付款。银行异步结果经回调网关写入 Kafka，由付款处理器消费并写入付款库。

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

支持工程师仅通过管理门户查看处理状态；查询API只读订单库与付款库。

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

| 部署边界 | 已确认约束 |
|---|---|
| 采购API、查询API | 两个独立部署进程 |
| 订单库、Outbox库、付款库 | 三个独立 PostgreSQL 实例 |
| 供应商系统、银行付款系统 | 属于各自组织，内部容器未规定 |

视图止于 C2 容器层，未展开组件，也未添加缓存、身份服务、补偿／重试或 Kafka 具体主题。