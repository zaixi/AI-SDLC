采用 **Markdown + 可编辑 Mermaid**：区域总览、处理时序、查询与通知三组视图，另附失败影响表。建议展示宽度 **1100 px**，高度随内容自适应；使用中性色与系统字体。

## 1. 先看全貌

平台内部共 **14 个单元**，按职责分为四个区域。下图概括成功主链；箭头表示业务推进，具体读写和先后顺序见后续时序图。区域不代表部署边界。

```mermaid
%%{init: {"theme":"neutral","fontFamily":"system-ui, sans-serif","flowchart":{"curve":"linear"}}}%%
flowchart TB
    subgraph A["接入｜接收并保存原件"]
        direction LR
        U["上传页"] --> R["接收 API"]
        R --> O[("原件库")]
    end

    subgraph B["处理｜管理作业并识别文本"]
        direction LR
        J[("作业表")]
        D["调度器"] --> W["OCR 工作者"]
        W --> T[("文本库")]
    end

    subgraph C["检索｜建立索引并提供查询"]
        direction LR
        I["索引工作者"] --> X[("搜索索引")]
        S["搜索页"] --> Q["查询 API"]
        Q -->|"只读"| X
    end

    subgraph E["运维｜查看状态并发送通知"]
        direction LR
        SP["状态页"] --> SA["状态 API"]
        N["通知器"]
    end

    R -->|"建立待处理作业"| J
    J -->|"待处理作业"| D
    O -->|"原件"| W
    W -->|"通知索引"| I
    T -->|"文本"| I
    W -->|"更新状态"| J
    I -->|"成功后标记已完成"| J
    SA -->|"只读"| J
    J -->|"已完成作业"| N
    N --> M["外部邮件服务<br/>平台之外"]

    style M fill:#fff,stroke:#666,stroke-dasharray:5 5
```

**成功状态链：** 待处理 → 处理中 → 待索引 → 已完成。  
搜索读取搜索索引，状态查询读取作业表；邮件通知以作业已完成为前提。

## 2. 处理明细：读写方向与先后约束

以下按成功路径展开。每条消息按从上到下的顺序发生；“通知”与“派发”不指定协议或传输方式。

```mermaid
%%{init: {"theme":"neutral","fontFamily":"system-ui, sans-serif"}}%%
sequenceDiagram
    participant U as 上传页
    participant A as 接收 API
    participant O as 原件库
    participant J as 作业表
    participant D as 调度器
    participant W as OCR 工作者
    participant T as 文本库
    participant I as 索引工作者
    participant X as 搜索索引

    U->>A: 提交原件
    A->>O: ① 写入原件
    A->>J: ② 建立待处理作业

    D->>J: 读取待处理作业
    D->>J: ① 状态改为处理中
    D->>W: ② 派发 OCR

    W->>O: 读取原件
    W->>T: ① 写入识别文本
    W->>J: ② 状态改为待索引
    W->>I: ③ 通知索引

    I->>T: 读取文本
    I->>X: 写入搜索索引
    I->>J: 索引成功后，状态改为已完成
```

## 3. 查询与通知：各自依赖什么

三条路径分别展开，**不表示它们之间存在执行顺序**。查询 API 和状态 API 均只读；通知器读取已完成作业后调用平台外的邮件服务。

```mermaid
%%{init: {"theme":"neutral","fontFamily":"system-ui, sans-serif"}}%%
flowchart TB
    subgraph Q["搜索路径"]
        direction LR
        S["搜索页"] -->|"调用"| API["查询 API"]
        API -->|"只读"| X[("搜索索引")]
    end

    subgraph ST["状态查看路径"]
        direction LR
        P["状态页"] -->|"调用"| A["状态 API"]
        A -->|"只读"| J1[("作业表")]
    end

    subgraph N["完成通知路径"]
        direction LR
        NT["通知器"] -->|"读取已完成作业"| J2[("作业表")]
        NT -->|"调用：发送完成通知"| M["外部邮件服务<br/>平台之外"]
    end

    style M fill:#fff,stroke:#666,stroke-dasharray:5 5
```

图中两处“作业表”是同一个内部单元的重复展示。

## 4. 值班定位：三类失败的影响边界

下表针对**发生失败的这份作业**。“未保证”表示给定事实不足以断言其具体数据状态。

| 失败点 | 作业状态与写入责任 | 本作业受影响的部分 | 保留或不重跑的部分 | 再次处理规则与未知项 |
|---|---|---|---|---|
| **OCR 失败** | OCR 工作者将作业表改为 **失败** | 未进入后续索引成功与完成通知路径；不能保证本作业可搜索 | 原件此前已保存；失败时是否已有文本未说明 | 需要**人工重新排队**；人工操作入口未确定 |
| **索引失败** | 作业保持 **待索引** | 本作业尚未完成；搜索索引更新未成功，不能保证可搜索；通知器不会按已完成作业处理它 | **已写入文本保留，不重跑 OCR** | **只重试索引**；由谁、何时调度未确定 |
| **邮件发送失败** | 作业仍为 **已完成** | 完成邮件发送失败 | OCR 与索引已成功；**不重跑 OCR 或索引**，搜索路径不因该邮件失败而回退 | **通知器只重试邮件发送**；重试时机未确定 |

状态页通过只读作业表，可分别看到 **失败、待索引、已完成**。因此，**“已完成”不能用来判断邮件是否发送成功**；材料没有提供邮件结果的查询入口。

```mermaid
%%{init: {"theme":"neutral","fontFamily":"system-ui, sans-serif","flowchart":{"curve":"linear"}}}%%
flowchart LR
    P["待处理"] -->|"调度器先改状态"| R["处理中"]
    R -->|"OCR 成功：文本已写入"| I["待索引"]
    R -->|"OCR 工作者写失败状态"| F["失败"]
    I -->|"索引成功后更新状态"| C["已完成"]

    I -->|"索引失败：保持待索引<br/>只重试索引，保留文本"| I
    C -->|"邮件失败：仍已完成<br/>通知器只重试邮件"| C

    F -.->|"需人工重新排队<br/>入口未确定"| P
```

虚线仅表示已知的人工重新排队要求，不表示已存在操作入口。以上视图未添加协议、消息队列、重试调度方式或额外故障处理入口。