# 图形约定与示例

这些图只示范表达方式；实际画图时使用当前内容给出的主体、关系和条件。

## 边界与所有权

```mermaid
flowchart LR
    Caller[调用方]
    subgraph Session[会话模块：拥有会话状态]
        Gate[写入门禁]
        Store[当前会话数据]
    end
    Caller -->|携带会话版本的响应| Gate
    Gate -->|版本匹配才写入| Store
    Constraint[设计约束：旧响应不能污染新会话]
    Constraint -.->|约束| Gate
```

虚线含义必须由标签说明；不能默认所有虚线都表示假设。保留内容原有的确认状态。

## 时序中的竞争

```mermaid
sequenceDiagram
    participant U as 用户
    participant S as 会话模块
    participant N as 网络请求
    U->>S: 在会话 A 发起请求
    S->>N: 请求携带版本 A
    U->>S: 切换到会话 B
    N-->>S: 返回版本 A 的响应
    alt 响应版本与当前会话一致
        S->>S: 更新数据
    else 版本不一致
        S->>S: 丢弃响应
    end
```

这是候选设计，不能据此断言某个真实系统已具备门禁。

## 大图拆分

先用总览呈现职责和边界，复杂时序或状态另画局部图。总览引用局部图，局部图沿用总览术语。每张图解释一个问题，避免展开不相关的实现细节。

离线 HTML 优先内嵌 SVG 和必要样式。使用 CDN 时明确外部依赖，不称其为完全离线自包含文件。
