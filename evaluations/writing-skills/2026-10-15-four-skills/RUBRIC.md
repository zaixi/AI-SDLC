# 预先固定的评审口径

仅评当前读者问题，内容完整、准确优先；长度为诊断数据，不直接当质量分数。

1. 有效信息：是否回答问题并保留必须知道的事实、条件、范围、不确定性。
2. 冗余：套话、同义重复、重复结论、已知背景、无关岔题、无需求的编辑过程。
3. 阅读与行动：重点位置、必要解释是否充分、表述是否易懂、下一步是否确实需要。
4. 语义失真：编造事实、改变可能性、遗漏关键限制、误报完成状态。

记录总输出字数、最终正文长度（可明确分离时）、首次出现实质答案的位置，以及具体冗余片段。输出文件不是用户所要求的交付；本轮任务均为直接回复。分开保留中间文本和最终回复。

按任务逐一比较，不设机械总分；给出每题偏好和原因。评审先使用打乱标签的回答、原题及此口径，完成判断后揭示映射。评审者是设计实验的当前助手，无法保证真正盲评；不调用独立评审模型。无无skill组，不能推出相对无skill的增益。每组合一次，不报告稳定胜率。

## 每题的内容核对项

```json
[
  {
    "id": "C01",
    "language": "zh",
    "type": "explanation",
    "prompt": "我们有个创建订单接口：客户端没收到响应时会重试。服务端可能已经创建成功，只是响应丢了。团队准备让客户端为一次下单生成一个请求 ID，重试沿用它，服务端保存这个 ID 对应的订单；但现在的实现是先查 ID，不存在就插入，并没有唯一约束。\n我刚接触这个设计。重试和幂等分别解决什么问题？加了请求 ID 是不是就不会重复下单了？请解释到我能判断这个方案是否够用。",
    "must_preserve": [
      "重试解决未收到响应后的再次尝试，不代表前次没有成功",
      "幂等关注重复请求的业务效果",
      "同一次业务请求的重试沿用相同ID",
      "先查再插存在并发竞态，不能保证不重复",
      "需要数据库唯一约束或等价原子去重方案",
      "重复请求应关联原有订单，不能再次创建"
    ],
    "risks": [
      "把请求ID本身当作保证",
      "只给结论不解释并发竞态",
      "臆造部署、吞吐量、耗时",
      "偏离到无关完整分布式系统教程"
    ]
  },
  {
    "id": "C02",
    "language": "zh",
    "type": "contextual_decision",
    "prompt": "下面是本轮讨论已有的上下文，不需要重新从概念讲起。\n我：我们已经确认重试要复用请求 ID，也给请求 ID 加了唯一约束。唯一约束解决了并发下创建重复订单的问题。\n助手：接下来检查响应丢失后，客户端使用同一请求 ID 能否取回原订单。\n我：测试结果出来了：同一个 ID 并发 20 次，只生成 1 个订单；创建成功后模拟响应丢失，再用同一 ID 重试，返回了这个订单。还有一项没处理：相同 ID 携带不同金额时，目前也直接返回原订单，不提示冲突。产品要求这种情况必须拒绝。除此之外没有更多测试结论。\n现在能上线了吗？最重要的依据是什么？",
    "must_preserve": [
      "目前不应按现状上线，因为明确产品要求尚未满足",
      "两个已验证场景为去重并发和响应丢失后取回原订单",
      "同ID不同金额应拒绝且当前未实现",
      "没有依据声称其他风险已排除或所有测试通过"
    ],
    "risks": [
      "重新长篇解释重试幂等",
      "把未实现项说成已修好",
      "随意估算修复时间",
      "要求用户做多项无关检查",
      "只说再测一下而未明确决策"
    ]
  },
  {
    "id": "E01",
    "language": "en",
    "type": "rewrite",
    "prompt": "Rewrite the following release note for support engineers. Keep the output in English.\n\nWe are pleased to announce an important and exciting improvement to the export worker, representing a significant step forward in making the export experience more robust and seamless. In version 2.4, the worker now waits 30 seconds for a response from the storage service, rather than the 10 seconds that it waited in version 2.3. This means the response timeout is now longer than before. In other words, the worker allows more time for the storage service to respond.\n\nIf the storage service returns HTTP 503, the worker retries the upload up to two times after the initial attempt, using the same upload ID for all attempts. It does not retry HTTP 400 responses. It is important to note that this change may reduce failures caused by brief storage outages; it does not guarantee that every export will succeed. The timeout change applies only to the upload stage, not to data collection or file generation.\n\nThe change is enabled by default for newly created workspaces. Existing workspaces must set export_worker_v2=true before they use it. Administrators can revert to the previous worker by setting export_worker_v2=false. Files that were already exported remain available after this rollback. We have not measured whether the new worker changes peak memory use. No peak-memory reduction should be claimed.\n\nTo summarize, this enhancement gives the storage service more time to respond, introduces carefully controlled retries, and offers a flexible rollout experience. This is an important improvement. We hope this helps!",
    "must_preserve": [
      "version2.4 timeout30s vs2.3 10s",
      "timeout applies only upload, excludes collection/filegeneration",
      "503 at most2 retries after initial attempt total3",
      "same uploadID allattempts",
      "400 not retried",
      "may reduce briefoutagefailures no successguarantee",
      "newworkspaces enabledbydefault",
      "existingworkspaces require export_worker_v2=true",
      "rollback export_worker_v2=false",
      "alreadyexported files remainavailable afterrollback",
      "peakmemory effect unmeasured no reductionclaim"
    ],
    "risks": [
      "drop scope or uncertainty",
      "turn two retries into two total attempts",
      "invent mechanisms or performance figures",
      "multiple full rewrites or commentary increase reading burden"
    ]
  }
]
```
