# 三套图示指引的独立 Agent 生成比较

日期：2026-10-09。本轮替代此前主Agent手工构造的对照样例。用户已确认 mermaid-diagrams 来自 aiskillstore/marketplace 的 softaworks 目录。

## 先看真实输出

- [第一轮逐题三组对照](comparison.md)：逐字汇集原始回答，支持 Mermaid 的阅读器可直接查看图。
- 第一轮原文件：[show-me](outputs/show-me/)、[visual-explanation](outputs/visual-explanation/)、[mermaid-diagrams](outputs/mermaid-diagrams/)。
- 第二轮原文件：[show-me](repeat-outputs/show-me/)、[visual-explanation](repeat-outputs/visual-explanation/)、[mermaid-diagrams](repeat-outputs/mermaid-diagrams/)。

租约和队列题的图仍然相似，是因为输入本身明确要求时序和职责关系；本轮答案独立生成，没有复用图或答案模板。更容易观察差异的是 03-diff 与 05-scope。

## 方法

每种指引两次全新 Agent 会话，每会话连续回答五题，合计六个生成会话、30份回答。使用 `fork_turns=none`，不继承主Agent对话历史；不指定模型覆盖，均继承相同默认模型和推理设置。每组只读自身 Skill、按需参考文件及相同题目，禁止读取其他组输出。原始回答未被主Agent修改。

六个会话共享文件系统，读取范围靠任务指令限定，不是操作系统级权限隔离。每会话的五题也共享组内上下文。没有固定随机种子，不把这些试验称为严格统计实验。

评审由另一个无对话历史的 Agent 完成，只给它隐藏来源标签的回答、题目与统一准则。主Agent不向评审者提供来源映射，再核对其证据。来源标签隐藏不消除从内容风格推测来源的可能，也不是双盲或用户可读性研究。

生成阶段三组都禁止渲染；之后统一做 Mermaid 语法解析，不据此评价图形布局。这里只测试“显式加载指引后的生成效果”，没有测试客户端安装、自动触发或其他 Skill 的委托调用。

详细记录：[protocol.json](protocol.json)、[rubric.json](rubric.json)、[raw-output-manifest.json](raw-output-manifest.json)、各组 provenance.json。

## 样本和版本

五题：过期租约与外部副作用、架构事实与未知动机、缓存小改动、取消请求与状态变化、支付重试与模块责任。

- show-me：Humanlayer，`ca7c8088db69e315a8b2deea43820270457f8f3c`。
- visual-explanation：本仓 0.2.0 的固定副本；测试期间未修改。
- mermaid-diagrams：aiskillstore/marketplace，`26421118b848d9f1efc0aa169d8a7a9e7e0a877e` 下 skills/softaworks/mermaid-diagrams。

版本副本保存在 inputs/。references 按需读取，具体见每组 provenance。没有假定所有附带文档都会自动进入上下文。

## 执行结果

**26张 Mermaid 图，26/26通过 Mermaid 12.1.0 语法解析。** 另外四份回答使用 diff，没有 Mermaid 块；它们不计入语法解析分母。没有进行本轮视觉渲染，也不宣称图已显示或布局合格。

| 条件 | 独立回答 | 平均字符数（包含图源码） | 小改动题的两次表达 |
|---|---:|---:|---|
| show-me | 10 | 304.1 | 都使用 diff |
| visual-explanation | 10 | 429.8 | 都使用 diff |
| mermaid-diagrams | 10 | 398.9 | 都使用前后流程图 |

字符数只用于观察输出负担，不是 token 数、可读性或质量评分。本地版本在这一组题目中平均比 show-me 多约41%字符，其中来源、确认状态及风险分析贡献了额外内容。

解析记录：[syntax-results.json](syntax-results.json)。可复用解析脚本：[scripts/parse.mjs](scripts/parse.mjs)。用 Node 在单独工具目录安装 mermaid@12.1.0 与 jsdom，然后运行 `node scripts/parse.mjs <本评估目录> <工具目录>`。本次工具依赖装在 /tmp，没有安装到业务仓库或给客户端注册插件。

## 输出差异的具体证据

- **show-me 更紧凑。** 队列题用简单调用关系加文字说明；本地版本增加显式职责分组、ADR约束节点和来源说明。两者都识别未知设计原因，不能声称 show-me 必然会编造原因。
- **mermaid-diagrams 更专注图形。** 小缓存改动也使用前后 flowchart；另外两组使用 diff。这里 diff 更紧凑，但并不是流程图不正确。
- **本地版本展开了更多风险前提。** 支付题两次都讨论外部支付方、并发与本地去重记录和扣款之间的崩溃窗口，且标为待决定/验证。其他两组也提出幂等与结果未知问题，不能把“额外风险分析”全部归功于本地规则。
- **本地版本也有冗余。** 第一轮 diff 回答写“未渲染验证”，第二轮则正确说明伪代码差异无需渲染。可考虑只对需要渲染的图报告渲染状态，避免例行重复。
- **一次 show-me 回答产生无依据的实线关系。** 第二轮支付题画出网关→订单、订单—计费/审计、计费—审计，并称“实线表示已知职责的关联”。输入只确认模块与所有权，没有确认这些关联。应该标为假设/建议，或只把需求映射到受影响模块。该问题不意味着 show-me 总体不可靠；两次试验不足以估计故障概率。
- **常规状态转换的依据标注不一致。** 题目没有逐条给出 queued→running 和 running→failed；本地版本两次解释是按状态名称推断，其他组有的未标。常规推断与编造架构关系严重程度不同，仍值得保持明确。

## 来源标签隐藏的独立评审

[逐份评审记录](anonymous-review.json)、[评审说明](anonymous-review.md)保留了评审Agent的原始结果，[标签映射与覆盖计数](review-summary.json)用于解释来源。

29份回答关键覆盖被评为 adequate；第二轮 show-me 的支付影响题为 partial，原因是将未给定关系声明为已知。此分类不是总分或成功率。状态图中的常规推断缺少限定被列为较轻问题，未与架构事实错误等同。主Agent已核对上述关键引文与原文件。

## 选型判断

本轮支持继续采用 show-me 的表达主体，加本地的意图/依据/保存规则，再用 mermaid-diagrams 的细节参考补充绘图。没有证据证明本地版本全面优于另外两者；它的具体收益是更显式的确认状态与工程风险说明，代价是篇幅。

下一步宜缩减不必要的例行说明，并在真实长输入、现有代码和不同客户端中继续验证。当前五道小题、每组两次、同一默认模型，无法推断跨模型稳定性或自动调用成功率。此轮只测试，未按结果修改 Skill。
