# 第一轮：十题、五组独立生成对照

逐字汇集未改写的原始文件；语法解析与事实审阅见 [主报告](README.md)。显示效果取决于阅读平台，本轮未验证布局。

## 01-lease

Worker A 领取任务，租约为30秒。A在第35秒提交，期间Worker B在第31秒重新领取。平台会拒绝过期租约的结果提交，但题目没有提供对外部写入的幂等或隔离保证。画出时序并判断“任务只执行一次”是否成立。请简短中文回答，不写项目文档。

### show-me

[原文件](outputs/show-me/01-lease.md)

```mermaid
sequenceDiagram
    participant A as Worker A
    participant P as 平台
    participant B as Worker B
    A->>P: t=0 领取任务（租约30秒）
    Note over A: 执行任务；可能发生外部写入
    Note over P: t=30 A的租约过期
    B->>P: t=31 重新领取任务
    Note over B: 执行任务；可能发生外部写入
    A->>P: t=35 提交结果
    P-->>A: 拒绝：租约已过期
```

“任务只执行一次”不成立：租约校验只能拒绝A的过期结果，不能阻止A、B重复执行或重复产生外部副作用。外部写入是否能防重，题目没有保证。


### mermaid-diagrams

[原文件](outputs/mermaid-diagrams/01-lease.md)

```mermaid
sequenceDiagram
    participant A as Worker A
    participant P as 平台
    participant B as Worker B
    participant E as 外部系统
    A->>P: 第0秒领取任务
    P-->>A: 租约30秒
    Note over A,P: 第30秒租约到期，不代表A已停止
    B->>P: 第31秒重新领取
    P-->>B: 新租约
    Note over A,E: A、B可能继续执行及产生外部写入；实际写入未知
    A->>P: 第35秒提交结果
    P-->>A: 拒绝过期租约的提交
```

“任务只执行一次”不成立为保证：同一任务已被重新领取，可能重复执行。平台拒绝A的结果，只约束结果提交，不能证明外部副作用只发生一次；还需外部写入的幂等或隔离保证。


### visual-v030

[原文件](outputs/visual-v030/01-lease.md)

```mermaid
sequenceDiagram
    participant A as Worker A
    participant P as 平台
    participant B as Worker B
    A->>P: t=0 领取任务
    P-->>A: 租约有效30秒
    Note over A,P: t=30 A的租约过期
    B->>P: t=31 重新领取任务
    P-->>B: 新租约
    A->>P: t=35 提交结果
    P-->>A: 拒绝过期租约提交
    Note over A,B: 外部写入的幂等与隔离保证未提供
```

“任务只执行一次”不成立：拒绝A提交只能保护平台结果提交，不能证明A停止执行，也不能撤销其外部写入。A、B可能重复执行并产生重复副作用；需核实外部写入的幂等或隔离机制。B领取也不等于执行完成。

未渲染验证。


### visual-v031

[原文件](outputs/visual-v031/01-lease.md)

```mermaid
sequenceDiagram
    participant A as Worker A
    participant P as 平台
    participant B as Worker B
    A->>P: t=0 领取任务，租约30秒
    Note over A,P: t=30 A租约到期；不代表A已停止执行
    B->>P: t=31 重新领取同一任务
    P-->>B: 发放新租约
    Note over A,B: 可能重复执行、重复外部写入；未提供隔离/幂等保证
    A->>P: t=35 提交结果
    P-->>A: 拒绝过期租约提交
```

“任务只执行一次”不成立：拒绝A的结果只限制平台接收提交，不能撤销其执行或外部写入，也不能阻止A、B重复执行。B是否完成、实际是否重复写入均未知。

未渲染验证。


### visual-v032-candidate

[原文件](outputs/visual-v032-candidate/01-lease.md)

```mermaid
sequenceDiagram
    participant A as Worker A
    participant P as 平台
    participant B as Worker B
    participant E as 外部系统
    A->>P: t=0 领取任务
    P-->>A: 租约至 t=30
    Note over A,P: t=30 A租约过期，不代表A停止执行
    B->>P: t=31 重新领取
    P-->>B: 新租约
    Note over A,E: A、B可能都执行外部写入；幂等/隔离未知
    A->>P: t=35 提交结果
    P-->>A: 拒绝过期租约提交
```

“任务只执行一次”不成立：重新领取允许重复执行，拒绝A的结果也不能撤销外部副作用。已知保证仅是拒绝过期提交；是否避免重复外部写入，需核实幂等或隔离机制。未渲染验证。


## 02-intent

已知API将订单入队，Worker消费队列并写入数据库；ADR只确认API不直接写数据库。没有吞吐、隔离故障或选择队列原因的资料。画出职责边界，说明哪些是事实，哪些设计原因尚未确认。请简短中文回答，不写项目文档。

### show-me

[原文件](outputs/show-me/02-intent.md)

```mermaid
flowchart LR
    A[API：订单入队] --> Q[队列]
    Q --> W[Worker：消费并写库]
    W --> D[(数据库)]
```

已知：API负责入队，Worker负责消费、写库；ADR明确API不直接写数据库。

未确认：为何选择队列，是否为提高吞吐、隔离故障或其他目的。职责边界是事实，这些设计动机需要补充决策依据。


### mermaid-diagrams

[原文件](outputs/mermaid-diagrams/02-intent.md)

```mermaid
flowchart LR
    subgraph Request[请求侧]
        API[API：订单入队]
    end
    Q[队列]
    subgraph Work[消费侧]
        W[Worker：消费并写入]
    end
    DB[(数据库)]
    API --> Q --> W --> DB
    ADR[ADR已确认：API不直接写数据库]
    ADR -.-> API
```

事实是上述职责与调用路径。选择队列是否为了吞吐、故障隔离或其他目标，尚未确认；不能从“API不直接写库”推导这些设计原因，需补充决策记录或指标证据。


### visual-v030

[原文件](outputs/visual-v030/02-intent.md)

```mermaid
flowchart LR
    A[API：订单入队] -->|写入订单消息| Q[队列]
    Q -->|Worker消费| W[Worker：写入数据库]
    W -->|写入| D[数据库]
    R[ADR确认：API不直接写数据库]
```

事实是上述职责与消息、写入关系，ADR确认了API的写入边界。采用队列是否为了吞吐、故障隔离或其他目标，尚未确认；不能从当前结构倒推设计原因。下一步查原始决策记录及其约束依据。

未渲染验证。


### visual-v031

[原文件](outputs/visual-v031/02-intent.md)

```mermaid
flowchart LR
    subgraph 接入职责
        A[API：订单入队]
    end
    Q[队列]
    subgraph 消费职责
        W[Worker：消费并写数据库]
    end
    D[(数据库)]
    A -->|入队| Q
    Q -->|消费| W
    W -->|写入| D
    N[ADR确认：API不直接写数据库]
    R[采用队列的原因待核实：查原决策记录]
```

图中行为来自题目；ADR确认API的写入边界。吞吐优化、故障隔离等只能作为候选解释，不能当作已确认的设计原因；需核对原决策及相关约束。

未渲染验证。


### visual-v032-candidate

[原文件](outputs/visual-v032-candidate/02-intent.md)

```mermaid
flowchart LR
    subgraph API边界
        A[API：将订单入队]
    end
    Q[队列]
    subgraph Worker边界
        W[Worker：消费并写库]
    end
    D[(数据库)]
    A -->|订单入队| Q
    Q -->|消费| W
    W -->|写入| D
    N[ADR确认：API不直接写数据库]
```

图中处理关系来自题目，ADR确认写库职责不在API。吞吐优化、故障隔离及选择队列的原因均未确认，不能从现有结构推导；需查原决策记录，缺失时再确认设计意图。未渲染验证。


## 03-diff

旧逻辑：每次save都write。新逻辑：内容未变化时直接返回缓存；变化时write再失效缓存。用最容易看懂的方式说明改动。请简短中文回答，不写项目文档。

### show-me

[原文件](outputs/show-me/03-diff.md)

```diff
 on(save)
+  if 内容未变化
+    return 缓存
   write 内容
+  失效缓存
```

原来每次都写；现在未变化就直接返回缓存，变化时仍写入，并在写入后失效缓存。


### mermaid-diagrams

[原文件](outputs/mermaid-diagrams/03-diff.md)

```mermaid
flowchart LR
    subgraph Old[旧逻辑]
        O[save] --> OW[每次write]
    end
    subgraph New[新逻辑]
        N[save] --> C{内容变化？}
        C -->|否| R[直接返回缓存]
        C -->|是| W[write] --> I[失效缓存]
    end
```

改动是增加“内容是否变化”的判断：未变化跳过写入并返回缓存；变化时先写入，再失效缓存。


### visual-v030

[原文件](outputs/visual-v030/03-diff.md)

```diff
 on(save)
+  if content is unchanged
+    return cached result
   write content
+  invalidate cache
```

未变化时直接返回缓存，跳过写入；变化时先写入，再使缓存失效。


### visual-v031

[原文件](outputs/visual-v031/03-diff.md)

```diff
 on(save)
+  if content is unchanged
+    return cached result
   write content
+  invalidate cache
```

未变化时复用缓存，省去写入；变化时先写入，再使缓存失效。


### visual-v032-candidate

[原文件](outputs/visual-v032-candidate/03-diff.md)

```diff
 on(save)
+  if content is unchanged
+    return cached result
   write content
+  invalidate cache
```

未变化时跳过写入，直接返回缓存；变化时先写入，再失效缓存。


## 04-state

一个任务有 queued、running、succeeded、failed、cancelled 五种状态。queued 可取消；running 收到取消请求后，只记录取消意图，只有 Worker 确认停止才进入 cancelled。running 也可能先完成并进入 succeeded。failed 可重新排队。没有规定 succeeded 能否再次重试。请画状态关系并解释取消请求与取消完成的区别。简短中文，不写项目文档。

### show-me

[原文件](outputs/show-me/04-state.md)

```mermaid
stateDiagram-v2
    queued --> running: Worker开始执行
    queued --> cancelled: 取消
    running --> running: 收到取消请求，仅记录意图
    running --> cancelled: Worker确认停止
    running --> succeeded: 执行完成（可能先于停止确认）
    running --> failed: 执行失败
    failed --> queued: 重新排队
```

取消请求表示“希望停止”，此时仍是running；取消完成需要Worker确认停止，才进入cancelled。若先完成，任务可进入succeeded。succeeded能否重试尚未规定，图中不补这条边。


### mermaid-diagrams

[原文件](outputs/mermaid-diagrams/04-state.md)

```mermaid
stateDiagram-v2
    queued --> running: Worker开始执行
    queued --> cancelled: 取消
    running --> running: 收到取消请求，仅记录意图
    running --> cancelled: Worker确认停止
    running --> succeeded: 先完成
    running --> failed: 执行失败
    failed --> queued: 重新排队
    note right of running
        取消请求后仍为running
        可能先完成并成功
    end note
    note right of succeeded
        是否允许重试尚未规定
    end note
```

取消请求表示“希望停止”，取消完成表示“Worker已确认停止”。两者之间任务仍在运行，不能提前标记 cancelled；成功后的重试关系需另行明确。


### visual-v030

[原文件](outputs/visual-v030/04-state.md)

```mermaid
stateDiagram-v2
    queued --> running: 开始执行
    queued --> cancelled: 取消
    running --> running: 取消请求 / 仅记录取消意图
    running --> cancelled: Worker确认停止
    running --> succeeded: 执行完成（也可能先于停止确认）
    running --> failed: 执行失败
    failed --> queued: 重新排队
    note right of succeeded
        能否再次重试：未规定
    end note
```

取消请求表达意图，任务仍是running；Worker确认停止才是取消完成。完成可能抢先发生并进入succeeded，因此请求取消不保证最终cancelled。图未为succeeded补出重试路径，需核实相应规则。

未渲染验证。


### visual-v031

[原文件](outputs/visual-v031/04-state.md)

```mermaid
stateDiagram-v2
    queued --> running: Worker开始执行
    queued --> cancelled: 取消
    running --> running: 取消请求 / 仅记录取消意图
    running --> cancelled: Worker确认停止
    running --> succeeded: 先完成
    running --> failed: 执行失败
    failed --> queued: 重新排队
    note right of running
        已请求取消，仍可能完成
    end note
    note right of succeeded
        能否重试未规定，需核对状态契约
    end note
```

取消请求只表达意图，任务仍是running；Worker确认停止才表示取消完成。若先完成则进入succeeded，不能因已发取消请求就认定cancelled。

queued→running、running→failed按状态含义推断；其余转移由题目明确给出。未渲染验证。


### visual-v032-candidate

[原文件](outputs/visual-v032-candidate/04-state.md)

```mermaid
stateDiagram-v2
    queued --> running: 开始执行
    queued --> cancelled: 取消
    running --> running: 收到取消请求 / 记录取消意图
    running --> cancelled: Worker确认停止
    running --> succeeded: 完成（可先于停止确认）
    running --> failed: 执行失败
    failed --> queued: 重新排队
    note right of succeeded
        能否再次重试：未规定
    end note
```

取消请求只记录意图，任务仍是running；Worker确认停止才是取消完成。期间可能先完成进入succeeded，不能把请求取消当成成功停止。succeeded的重试规则需补充确认。未渲染验证。


## 05-scope

系统有入口网关、订单模块、计费模块和审计模块。已有决定：订单拥有订单状态，计费拥有扣款状态，审计记录结果。新需求允许支付超时后重试，必须防止重复扣款。没有现成的幂等设计资料。请用图帮助评审影响边界，区分已知职责和需要决定/验证的地方。简短中文，不写项目文档。

### show-me

[原文件](outputs/show-me/05-scope.md)

```mermaid
flowchart TB
    G[入口网关] --- R{支付超时后重试：影响评审}
    R --- O[订单：拥有订单状态]
    R --- B[计费：拥有扣款状态]
    R --- A[审计：记录结果]
    R -. 待决定 .-> I[重试标识、幂等责任与防重机制]
    R -. 待验证 .-> V[并发重试、扣款结果未知、崩溃恢复]
```

实线展示影响范围和已知职责，不代表已确认的调用链。

需决定：同一笔支付如何跨重试识别、在哪里保证不重复扣款，订单超时后如何表达未知结果，审计如何关联多次尝试。计费拥有扣款状态，但现有幂等方案尚无资料；防重效果需用并发与故障场景验证。


### mermaid-diagrams

[原文件](outputs/mermaid-diagrams/05-scope.md)

```mermaid
flowchart TB
    subgraph Known[已知职责]
        G[入口网关]
        O[订单：拥有订单状态]
        B[计费：拥有扣款状态]
        A[审计：记录结果]
    end
    subgraph Review[支付超时重试：待决定或验证]
        ID[网关与订单：重试身份如何传递？]
        OS[订单：结果未知时如何处理状态？]
        BS[计费：如何识别同次支付并防重复扣款？]
        AS[审计：如何关联重试与最终结果？]
    end
    G -.-> ID
    O -.-> ID
    O -.-> OS
    B -.-> BS
    A -.-> AS
```

虚线表示评审影响，不代表已有调用路径或幂等方案。优先明确支付身份、幂等责任及原子性边界，再验证并发重试、超时后实际已扣款、崩溃恢复时是否仍只扣一次；订单与审计需一致反映最终结果。


### visual-v030

[原文件](outputs/visual-v030/05-scope.md)

```mermaid
flowchart TB
    R[新需求：支付超时可重试，防止重复扣款]
    G[入口网关]
    O[订单：拥有订单状态]
    B[计费：拥有扣款状态]
    A[审计：记录结果]
    R -.->|评审关注：重试标识与请求契约| G
    R -.->|评审关注：结果未知时的状态| O
    R -.->|评审关注：扣款去重与并发| B
    R -.->|评审关注：重复或迟到结果记录| A
```

图中边表示评审关注，模块调用与事件链路尚未提供。已确认的是三项状态/记录职责；超时也不证明扣款失败。

先核实现有重试与幂等契约，包括标识传递、扣款去重和外部副作用保护；不足时再决定契约及责任分配。验证超时后实际已扣款、并发重试和迟到结果场景，检查是否仍只产生一次扣款。

未渲染验证。


### visual-v031

[原文件](outputs/visual-v031/05-scope.md)

```mermaid
flowchart TB
    R[支付超时后重试：必须防止重复扣款]
    G[入口网关：重试标识的接入契约待核实]
    O[订单：拥有订单状态；超时结果如何表达待核实]
    B[计费：拥有扣款状态；去重与扣款边界待核实]
    A[审计：记录结果；重复/未知结果的记录语义待核实]
    R -.->|评审关注| G
    R -.->|评审关注| O
    R -.->|评审关注| B
    R -.->|评审关注| A
    C[建议：先查现有重试/幂等契约；不足时决定标识、去重及外部扣款协调方案]
    R -.->|下一步| C
    V[待验证：并发重试、已扣款但响应超时、扣款后崩溃]
    R -.->|验收关注| V
```

边表示评审关注，不代表模块调用。超时可能已扣款；订单和审计的状态/记录不能替代计费扣款的防重保证。没有资料不等于没有幂等方案，先核实现状，再补决策与证据。

未渲染验证。


### visual-v032-candidate

[原文件](outputs/visual-v032-candidate/05-scope.md)

```mermaid
flowchart TB
    R[新需求：支付超时后重试；防止重复扣款]
    G[入口网关]
    O[订单：拥有订单状态]
    B[计费：拥有扣款状态]
    A[审计：记录结果]
    R -.->|评审关注：重试标识如何进入系统| G
    R -.->|评审关注：超时后的订单状态| O
    R -.->|评审关注：重复扣款防护| B
    R -.->|评审关注：重试结果如何记录| A
```

节点职责已知；虚线仅表示评审关注，模块调用关系尚未提供。超时不证明扣款失败。

先核实现有重试/幂等契约，包括标识传递、去重范围与并发保证；若不足，再决定防重复扣款方案及未知结果的处理方式。验证“已扣款但响应超时”和并发重试场景，审计应能追踪最终结果。未渲染验证。


## 06-existing

评审支付超时重试需求。已有设计记录明确：入口网关向订单模块传递客户端payment_id；订单调用计费，计费负责扣款和幂等，已有数据库唯一键覆盖payment_id；审计订阅计费的结果事件。订单在支付结果未知时保持pending。尚未提供“外部已扣款但本地提交前崩溃”和“并发重试”的测试结果。请用图解释当前职责和本次需要做的工作，不重新设计已确认机制。简短中文，不写项目文档。

### show-me

[原文件](outputs/show-me/06-existing.md)

```mermaid
flowchart LR
    G[网关] -->|客户端payment_id| O[订单：结果未知时保持pending]
    O -->|调用计费| B[计费：扣款与幂等]
    B --- D[(数据库：payment_id唯一键)]
    B -->|结果事件| A[审计：订阅并记录]
    B -. 待测试 .-> T[外部已扣款、本地提交前崩溃]
    B -. 待测试 .-> C[并发重试]
```

上述职责与唯一键已确认，本次沿用。需要补齐两类测试：崩溃后重试是否避免再次扣款并恢复结果；并发重试是否只产生一次扣款并返回一致结果。也应核对订单pending能否随结果收敛、审计事件能否对应最终结果。

唯一键已存在，但它对外部扣款故障窗口的保护效果，仍需测试证据。


### mermaid-diagrams

[原文件](outputs/mermaid-diagrams/06-existing.md)

```mermaid
flowchart LR
    G[入口网关] -->|客户端payment_id| O[订单：结果未知保持pending]
    O -->|调用计费| B[计费：扣款与幂等]
    B --> D[(已有唯一键：payment_id)]
    B -->|结果事件| A[审计：订阅结果]
    T[待验证：外部已扣款后本地提交前崩溃；并发重试]
    T -.-> B
    T -.-> O
```

职责、payment_id传递和唯一键机制已确认，本次应沿用并补充上述两类测试，检查实际扣款次数、恢复后的结果、订单状态及审计事件一致性。唯一键约束本地记录，并不能单凭它证明外部扣款在崩溃窗口也不会重复；需测试与实现证据。


### visual-v030

[原文件](outputs/visual-v030/06-existing.md)

```mermaid
flowchart LR
    G[入口网关] -->|传递客户端payment_id| O[订单：结果未知时保持pending]
    O -->|调用计费| B[计费：负责扣款与幂等]
    B -->|payment_id唯一键约束| D[数据库]
    B -->|结果事件| A[审计：订阅计费结果]
    T[待验证：外部已扣款后、本地提交前崩溃；并发重试]
    T -.->|验证关注：副作用与去重边界| B
```

以上职责与唯一键机制已有设计记录，本次复用。待做的是补齐两类测试及证据：崩溃后恢复/重试不重复扣款，且订单最终能收敛；并发重试只产生一次扣款并获得一致结果。数据库唯一键不能单独证明外部扣款也具备相同保证；先按已有实现验证，发现缺口再评审修正。

未渲染验证。


### visual-v031

[原文件](outputs/visual-v031/06-existing.md)

```mermaid
flowchart LR
    G[入口网关] -->|传递客户端payment_id| O[订单：结果未知保持pending]
    O -->|调用；payment_id| B[计费：负责扣款和幂等]
    B -->|已有唯一键覆盖payment_id| D[(数据库)]
    B -->|发布扣款结果事件| E[结果事件]
    E -->|订阅| A[审计：记录结果]
    T[待验证：并发重试；外部已扣款、本地提交前崩溃]
    T -.->|验证扣款及幂等边界| B
```

已有职责、payment_id和唯一键机制继续复用。本次重点是补两类测试：并发相同payment_id时不重复扣款；外部扣款成功后本地提交前崩溃，重试能恢复并避免再次扣款。数据库唯一键本身不能证明外部副作用只发生一次；若测试暴露缺口，再针对缺口修正。

来源：题目中的既有设计记录。未渲染验证。


### visual-v032-candidate

[原文件](outputs/visual-v032-candidate/06-existing.md)

```mermaid
flowchart LR
    G[入口网关] -->|客户端payment_id| O[订单：未知结果保持pending]
    O -->|调用计费| B[计费：扣款及幂等]
    B -->|唯一键覆盖payment_id| D[(数据库)]
    B -->|发布结果事件| A[审计：订阅结果]
    T[待验证：外部扣款后、本地提交前崩溃；并发重试]
    T -.->|验证关注| B
```

现有设计已确认幂等归属和唯一键，本次应补充两类测试证据：崩溃恢复后重试是否重复扣款、结果能否最终收敛；相同payment_id并发重试是否只产生一次扣款并返回一致结果。数据库唯一键本身不足以证明外部扣款与本地提交间的故障安全。失败时再定位现有机制的缺口。未渲染验证。


## 07-incident

一次请求在10:00命中API缓存并返回价格100元；10:01数据库价格改为120元，更新事件成功写入队列；10:02消费者报告该事件处理失败，随后没有提供重试或缓存失效记录；10:03请求仍从缓存读到100元。缓存TTL为10分钟。请用图解释已知过程、候选原因和下一步排查，不把时间先后当作已证明的因果。简短中文，不写项目文档。

### show-me

[原文件](outputs/show-me/07-incident.md)

```mermaid
sequenceDiagram
    participant R as 请求
    participant C as API缓存
    participant D as 数据库
    participant Q as 队列
    participant W as 消费者
    R->>C: 10:00 读价格
    C-->>R: 100元
    Note over D: 10:01 价格改为120元
    D->>Q: 更新事件写入成功
    Q->>W: 消费事件
    Note over W: 10:02 报告处理失败
    Note over W,C: 后续重试、失效记录未提供
    R->>C: 10:03 读价格
    C-->>R: 100元
```

候选原因：处理失败可能阻断失效；也可能失效了错误的键或实例，或旧值被再次写入。时间顺序不能证明哪一种发生了。

下一步：按事件ID查失败阶段、重试/死信和失效记录，再核对缓存键、实例、写入时间及实际TTL。TTL为10分钟，但10:00只是命中时间，不能据此推算何时过期。


### mermaid-diagrams

[原文件](outputs/mermaid-diagrams/07-incident.md)

```mermaid
sequenceDiagram
    participant R as 请求
    participant C as API缓存
    participant D as 数据库
    participant Q as 队列
    participant W as 消费者
    R->>C: 10:00查询价格
    C-->>R: 命中，100元
    Note over D: 10:01价格改为120元
    D-)Q: 更新事件成功入队
    Note over W: 10:02报告该事件处理失败
    Note over Q,W: 此后重试与缓存失效记录未提供
    R->>C: 10:03查询价格
    C-->>R: 仍命中，100元
    Note over C: TTL为10分钟；写入与到期时间未知
```

候选原因是事件处理失败导致失效未执行、重试尚未成功，或失效键不匹配、旧值被重新写入；均未证实。TTL允许旧值暂存，但不能从10:00命中推定到期为10:10。

下一步按事件ID查失败位置、确认与重试记录，再核对缓存键、失效执行、写入时间和剩余TTL。时间先后本身不能证明消费者失败导致此次旧值命中。


### visual-v030

[原文件](outputs/visual-v030/07-incident.md)

```text
已知时间线
10:00  请求 → API缓存命中 → 返回100元
10:01  数据库价格改为120元；更新事件成功入队
10:02  消费者报告该事件处理失败
        后续重试、缓存失效记录：未提供
10:03  请求 → API缓存命中 → 仍返回100元
约束：缓存TTL为10分钟；缓存实际写入时间未知

候选解释                         验证证据
失效处理失败且未成功补偿       → 消费错误、重试/死信及失效日志
失效键或缓存层不匹配           → 事件标识、目标键、请求实际命中层
失效后被旧值重新填充           → 删除、写入及读取来源的时间记录
```

消费者失败是线索，尚不能证明它导致10:03的旧值。TTL也不从10:00命中时重新起算；先串联该事件、实际缓存键的处理/写入日志，并查实际到期时间，定位旧值保留或回填的路径。


### visual-v031

[原文件](outputs/visual-v031/07-incident.md)

```mermaid
sequenceDiagram
    participant R as 请求
    participant C as API缓存
    participant D as 数据库
    participant Q as 队列
    participant W as 消费者
    R->>C: 10:00 读取
    C-->>R: 100元
    Note over D: 10:01 价格改为120元
    D->>Q: 更新事件成功入队
    Q->>W: 事件交付
    Note over W: 10:02 报告处理失败
    Note over W,C: 后续重试/失效记录未提供，不等于未发生
    R->>C: 10:03 读取
    C-->>R: 仍为100元
    Note over C: TTL=10分钟；写入时间、剩余TTL待核实
```

候选原因是事件失败后失效未完成，或重试/失效命中了错误键；时间顺序还不能证明因果。建议沿同一事件ID查失败步骤、确认及重试/死信记录，再核对缓存键、失效日志、写入时间和实际TTL。10:00命中不代表此时刚写入，不能据此推定10:10过期。

未渲染验证。


### visual-v032-candidate

[原文件](outputs/visual-v032-candidate/07-incident.md)

```text
时间     已知观测
10:00    API命中缓存，返回100元
10:01    数据库改为120元；更新事件成功入队
10:02    消费者报告事件处理失败
         └─ 后续重试、缓存失效：未提供记录
10:03    API仍命中缓存，返回100元

候选原因（未证实）             建议验证
事件未成功完成失效 ─────────→ 查事件ID、失败阶段、重试/死信及失效记录
失效作用于错误键或缓存层 ───→ 比对写入、失效、读取的键与实例
失效后又写回旧值 ───────────→ 查失效前后缓存写入与并发请求轨迹
```

时间先后不能证明消费失败导致旧价；失败也不等于失效步骤未执行。TTL为10分钟，但缓存创建时间、是否续期未知；若10:00才写入且不续期，10:03仍可在有效期内。先串联同一事件及缓存键的日志，再用复现验证候选原因。


## 08-tradeoff

团队要为报表选择实时查询主库或异步物化视图。已有约束：用户能接受最多5分钟的数据延迟，主库在业务高峰接近容量上限，团队只有两名维护者。实时查询不需新增同步链路；物化视图需要处理积压、重放和对账。没有负载测试、报表查询成本和运维成本数据。请用图帮助比较这两个方案，给出有条件的建议与所需证据，不把候选方案当成已决定。简短中文，不写项目文档。

### show-me

[原文件](outputs/show-me/08-tradeoff.md)

```mermaid
flowchart LR
    R[报表] -. 候选A .-> D[(实时查询主库)]
    D --- L[无新增同步链路；占用主库容量]
    R -. 候选B .-> V[异步物化视图]
    S[业务数据] -->|新增同步链路| V
    V --- M[需维护积压、重放、对账]
```

| 比较点 | 实时主库 | 异步物化视图 |
|---|---|---|
| 数据延迟 | 查询当前数据 | 必须控制在5分钟内 |
| 高峰容量 | 主库接近上限，需证明承载能力 | 可分担查询，仍需量化同步开销 |
| 两人维护 | 链路较少 | 额外运维负担需评估 |

有条件地优先验证物化视图：若能满足5分钟延迟且两人能维护，较适合缓解高峰压力。若报表实测开销很小、主库仍有安全余量，实时查询也可成立。

决策前需要：报表成本与高峰负载测试、物化视图积压恢复时间、重放/对账演练及维护成本。两者目前都是候选。


### mermaid-diagrams

[原文件](outputs/mermaid-diagrams/08-tradeoff.md)

```mermaid
flowchart TB
    C[约束：延迟最多5分钟；高峰主库接近容量；两名维护者]
    C --> R[候选：实时查询主库]
    C --> M[候选：异步物化视图]
    R --> RP[无需新增同步链路]
    R --> RR[需验证报表查询对主库的负载]
    M --> MP[可将报表读取移出主库；需确认实际收益]
    M --> MR[需维护积压、重放、对账；延迟须满足5分钟]
    RR --> E[负载测试、查询成本、运维成本证据]
    MR --> E
```

倾向先验证物化视图：若同步与回放负载可控、积压恢复仍满足5分钟且两人能维护，则采用。若实测实时查询足够轻、主库仍有安全余量，则实时方案更省维护。当前缺少成本与测试数据，两种方案都尚未决定。


### visual-v030

[原文件](outputs/visual-v030/08-tradeoff.md)

```text
候选A：实时查询主库             候选B：异步物化视图
报表 → 主库实时查询            主库变更 → 异步同步 → 物化视图 ← 报表
       ↑高峰接近容量上限                   ↑积压、重放、对账
无需新增同步链路               须验证数据延迟≤5分钟
两名维护者：新增链路的维护负担需要量化
```

建议先验证B：允许5分钟延迟且主库接近容量，使它更值得评估，但同步链路也可能增加主库负载和维护成本，尚未决定。

决策证据集中在两组：真实报表查询的高峰压测与成本；物化方案的端到端延迟、积压恢复/重放/对账演练及维护工时。若A在高峰仍有足够容量且成本低，可选A；若B满足延迟、减轻总负载且两人能维护，可选B。两者均不满足时继续调整范围或方案。


### visual-v031

[原文件](outputs/visual-v031/08-tradeoff.md)

```mermaid
flowchart TB
    C[选择未定：延迟≤5分钟；主库高峰近容量上限；维护者2人]
    C -->|候选A| A[实时查询主库：无新增同步链路；新增查询负载需测]
    C -->|候选B| B[异步物化视图：同步链路需维护；积压、重放、对账不可省]
    A --> VA[待验证：真实报表成本、高峰负载、主库余量]
    B --> VB[待验证：端到端延迟≤5分钟、积压恢复、维护成本]
    VA --> D[依据测量结果作决定]
    VB --> D
```

建议优先验证物化视图，因可接受延迟且主库余量紧张；前提是它能减少主库压力，并由两人维持延迟与恢复目标。若报表成本很低、实测主库有余量，而同步运维负担过高，则实时查询更合适。先以代表性报表做高峰负载测试，再测同步积压、重放及对账成本，当前证据不足以定案。

未渲染验证。


### visual-v032-candidate

[原文件](outputs/visual-v032-candidate/08-tradeoff.md)

```text
候选A：报表 ──实时查询──→ 主库
                         ↑ 高峰接近容量上限
       优点：无新增同步链路
       关键未知：报表查询增加多少负载？

候选B：数据更新 ──异步同步──→ 物化视图 ←──查询── 报表
                  ↑                 ↑
       积压、重放、对账       端到端延迟须≤5分钟
       关键未知：两名维护者能否承担运维？
```

| 比较点 | 实时查询主库 | 异步物化视图 |
|---|---|---|
| 时效 | 直接查询当前数据 | 需证明延迟不超过5分钟 |
| 主库压力 | 增加报表查询负载 | 可转移报表查询，但同步仍有成本 |
| 维护成本 | 少一条同步链路 | 需维护积压、重放和对账 |

建议优先验证物化视图候选：延迟容忍度与主库压力支持这一方向，但两名维护者是约束。需测报表查询成本及高峰主库余量、同步峰值与积压恢复时间，并演练重放/对账、估算维护投入。若主库能安全承载且同步维护成本过高，可选实时查询；证据不足前不定案。


## 09-domain

业务规则：一个订单包含一个或多个订单项；每个订单项属于且只属于一个订单；每个订单项引用一个商品，同一商品可被多个订单项引用，商品可以从未被下单。订单项保存下单时的单价快照；商品当前价格变化不能改写历史订单项价格。还没有数据库表、外键、级联删除或ORM设计。请用图解释领域关系、数量关系和价格约束，不将领域规则写成已有数据库实现。简短中文，不写项目文档。

### show-me

[原文件](outputs/show-me/09-domain.md)

```mermaid
classDiagram
    订单 "1" *-- "1..*" 订单项 : 包含
    订单项 "0..*" --> "1" 商品 : 引用
    class 订单项 {
        下单单价快照
    }
    class 商品 {
        当前价格
    }
```

每个订单至少有一个订单项；每个订单项只属于一个订单，并引用一个商品。一个商品可以被零个或多个订单项引用。

订单项使用下单时的单价快照；商品当前价格变化不能改写历史快照。图表达领域归属与引用，不规定表、外键、级联删除或ORM实现。


### mermaid-diagrams

[原文件](outputs/mermaid-diagrams/09-domain.md)

```mermaid
classDiagram
    class Order[订单]
    class Item[订单项] {
        下单单价快照
    }
    class Product[商品] {
        当前价格
    }
    Order "1" -- "1..*" Item : 包含
    Item "0..*" --> "1" Product : 引用
    note for Item "商品当前价格变化，不得改写下单单价快照"
```

每个订单至少有一个订单项，每项只属于一个订单；每项引用一个商品，商品可以被零个或多个订单项引用。历史单价以订单项快照为准。图表达领域规则，表结构、外键、级联删除与ORM映射尚未设计。


### visual-v030

[原文件](outputs/visual-v030/09-domain.md)

```mermaid
classDiagram
    class 订单
    class 订单项 {
        下单单价快照
    }
    class 商品 {
        当前价格
    }
    订单 "1" -- "1..*" 订单项 : 包含
    订单项 "0..*" --> "1" 商品 : 引用
```

这是领域关系：每个订单有至少一个订单项，每项只属于一个订单且引用一个商品；商品可被零个或多个订单项引用。订单项单价保存下单时快照，商品当前价格变化不得改写历史快照。

图未决定数据库表、外键、级联删除或ORM实现。

未渲染验证。


### visual-v031

[原文件](outputs/visual-v031/09-domain.md)

```mermaid
classDiagram
    class 订单
    class 订单项 {
        下单单价快照
    }
    class 商品 {
        当前价格
    }
    订单 "1" -- "1..*" 订单项 : 包含 / 归属
    订单项 "0..*" --> "1" 商品 : 引用
    note for 订单项 "历史单价取下单时快照；商品当前价格变化不得改写它"
```

这是领域关系：每项只属一个订单、引用一个商品；商品可被零到多个订单项引用。单价快照与当前价格是两个不同语义的值。图不规定数据库表、外键、级联删除或ORM实现，这些尚未设计。

未渲染验证。


### visual-v032-candidate

[原文件](outputs/visual-v032-candidate/09-domain.md)

```mermaid
classDiagram
    class 订单
    class 订单项 {
        下单时单价快照
    }
    class 商品 {
        当前价格
    }
    订单 "1" -- "1..*" 订单项 : 包含
    订单项 "0..*" --> "1" 商品 : 引用
    note for 订单项 "历史单价不随商品当前价格变化"
```

这是领域关系：订单至少有一个订单项，每项只属于一个订单、引用一个商品；商品可以没有订单项引用。下单时保存单价快照，之后商品调价不能改写历史价格。数据库表、外键、级联删除及ORM映射尚未设计，图中不作实现承诺。未渲染验证。


## 10-rollout

当前v1服务读写users.name。计划v2使用users.display_name，发布期间v1与v2实例会并存，v1不会写display_name。拟议步骤是新增可空display_name、回填历史值、切换v2、删除name；没有决定并存期间如何同步两字段。请用图审阅发布与回滚风险，指出什么时候能删除name以及还缺哪些条件。不替团队假定已有双写方案，简短中文，不写项目文档。

### show-me

[原文件](outputs/show-me/10-rollout.md)

```mermaid
flowchart LR
    A[新增可空display_name] --> B[回填历史值]
    B --> C[v1与v2并存]
    C --> D[v1退出；验证数据与回滚条件]
    D -. 条件满足后 .-> E[删除name]
    C --- V1[v1读写name]
    C --- V2[v2使用display_name]
    V1 -. 同步机制未决定 .-> V2
    V2 -. 回滚数据兼容未确认 .-> V1
```

回填只覆盖历史时点：并存期间v1新增或修改name，display_name可能为空或过时；v2更新若未同步回name，回滚到v1也可能读到旧值。

还缺：两字段的权威值、同步方式与冲突规则，v2遇到空值的行为，回填期间并发写入的处理，以及并存和回滚测试。不能假定已有双写。

只有v1及其他name读写方全部退出、数据完整一致、同步迁移验证通过，且不再需要直接回滚到依赖name的版本（或已有验证过的恢复方案），才能删除name。


### mermaid-diagrams

[原文件](outputs/mermaid-diagrams/10-rollout.md)

```mermaid
flowchart TD
    A[当前：v1读写name] --> B[拟议：新增可空display_name]
    B --> C[拟议：回填历史值]
    C --> D{并存期同步规则已决定并验证？}
    D -->|否| X[暂停切换：v1新写入可能使display_name落后]
    D -->|是| E[逐步切换v2；v1与v2并存]
    E --> F{旧实例退出、数据一致且无需回滚v1？}
    F -->|否| K[保留name，继续兼容与验证]
    F -->|是| H[可删除name]
    E -.-> R[回滚v1：name必须保留且包含v2期间的最新写入]
```

一次回填不能覆盖并存期v1持续写入。还需决定字段同步、冲突处理、v2遇到空值的行为，并验证并发写入及回滚时的数据一致性；不能假定已有双写。

只有所有依赖name的实例与任务退出、display_name完整且一致、v1回滚窗口关闭后，才能删除name；否则回滚可能读到旧值，删列后v1甚至无法运行。


### visual-v030

[原文件](outputs/visual-v030/10-rollout.md)

```mermaid
flowchart TB
    A[当前：v1读写users.name] -->|拟议| B[新增可空display_name并回填]
    B --> C[发布期间：v1与v2并存]
    C --> D[仅v2：读写display_name]
    D -->|须满足删除门槛| E[删除name]
    C -.->|风险：v1仍只写name| R[回填后display_name再次落后]
    C -.->|风险：v2写display_name，回滚读取name| S[回滚可能读到旧值]
    Q[待决策：并存及回滚期间的字段同步契约] -.->|发布前置条件| C
```

一次回填不能覆盖之后的v1写入，新增字段可空也不能保证v2读到有效值。先决定同步方向、冲突/空值处理、回填与并发写入的衔接，以及回滚时如何保留v2的新数据；当前不能假定双写已存在。

删除name前须确认：v1及其他读写name的依赖全部退出，历史与增量数据已对账，新路径和并发/回滚场景验证通过，并已结束回滚到依赖name版本的窗口，或建立验证过的恢复方案。仍需回滚到v1时保留name及有效同步能力。

未渲染验证。


### visual-v031

[原文件](outputs/visual-v031/10-rollout.md)

```mermaid
flowchart TB
    A[现状：v1读写users.name] --> B[拟议：新增可空display_name并回填]
    B --> C{进入v1/v2并存前：同步与冲突规则是否已决定并验证？}
    C -->|尚未决定：当前阻塞| X[风险：回填后v1继续写name，display_name再次落后]
    C -->|条件满足后才可继续| D[分批切换v2：观察空值、两字段差异及写入一致性]
    D --> E{v1及旧字段依赖已退出？回滚窗口已结束？}
    E -->|否| K[保留name及兼容机制]
    E -->|是，且迁移验证通过| F[才可删除name]
    D -.->|拟议回滚：需name保持最新且旧版可运行| A
    F -.->|直接回滚v1会缺列，需恢复数据与兼容结构| R[另备恢复方案]
```

回填只是历史快照，不能解决并存期写入。需决定两字段同步、权威值与冲突规则，并明确v2读取空值的行为；不能假定已有双写。用并发更新、回填期间写入和实际回滚演练验证一致性。只有旧实例与依赖全部退出、display_name完整且最新、旧版回滚需求结束后，才进入删列步骤；否则必须保留name。

图中流程是建议的发布门槛，并非已完成部署。未渲染验证。


### visual-v032-candidate

[原文件](outputs/visual-v032-candidate/10-rollout.md)

```mermaid
flowchart LR
    A[现状：v1读写name] -->|拟议| B[新增可空display_name]
    B -->|拟议| C[回填历史值]
    C -->|拟议切换| D[v1/v2并存]
    D -->|须先满足退出条件| E[v2独占读写]
    E -->|须先满足删除条件| F[删除name]
    R[风险：v1仍只写name；回填后两字段可能分叉]
    R -.->|并存期风险| D
    K[回滚v1需要name保留且数据可用]
    K -.->|回滚条件| E
```

回填只是某时点的数据复制，不能覆盖之后的v1写入；当前拟议步骤缺少并存期同步决定，直接切换可能让v2读到空值或旧值。v2的新写入若未同步name，回滚v1也可能读到旧值。

先决定两字段的写入权威、同步方式、冲突处理及v2空值读取策略，再验证并发写、回填期间更新与回滚的数据一致性。仅在v1及其他name依赖全部退出、同步与迁移核对通过、回滚窗口结束或替代恢复方案验证完成后，才可删除name；删列后不能直接回滚v1。未渲染验证。

