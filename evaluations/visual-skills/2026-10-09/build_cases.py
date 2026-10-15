from pathlib import Path
import json,re
p=Path('/tmp/ai-sdlc-visual-bench');out=p/'cases';out.mkdir(exist_ok=True)
prompts={
 '01-lease':'Worker A 领取任务，租约为30秒。A在第35秒提交，期间Worker B在第31秒重新领取。平台会拒绝过期租约的结果提交，但题目没有提供对外部写入的幂等或隔离保证。画出时序并判断“任务只执行一次”是否成立。请简短中文回答，不写项目文档。',
 '02-intent':'已知API将订单入队，Worker消费队列并写入数据库；ADR只确认API不直接写数据库。没有吞吐、隔离故障或选择队列原因的资料。画出职责边界，说明哪些是事实，哪些设计原因尚未确认。请简短中文回答，不写项目文档。',
 '03-diff':'旧逻辑：每次save都write。新逻辑：内容未变化时直接返回缓存；变化时write再失效缓存。用最容易看懂的方式说明改动。请简短中文回答，不写项目文档。'}
lease='''sequenceDiagram
    participant A as Worker A
    participant P as 任务平台
    participant B as Worker B
    participant E as 外部系统
    A->>P: t=0 领取任务（租约30秒）
    B->>P: t=31 重新领取已过期任务
    Note over A,B: 同一任务可能有两次执行尝试
    A->>P: t=35 提交旧租约结果
    P-->>A: 拒绝过期租约提交
    Note over A,E: 外部写入的去重和隔离保证未提供
'''
intent='''flowchart LR
    subgraph Ingress[接入边界]
        API[API]
    end
    Q[订单队列]
    subgraph Processing[消费边界]
        W[Worker]
    end
    DB[(数据库)]
    API -->|订单入队：事实| Q
    Q -->|消费：事实| W
    W -->|写入：事实| DB
    C[已确认约束：API不直接写数据库]
    C -.->|约束| API
'''
diff=''' on(save)
-  write content
+  if content is unchanged
+    return cached result
+  write content
+  invalidate cache
'''
flow='''flowchart LR
    subgraph Before[改动前]
        A[save] --> B[write]
    end
    subgraph After[改动后]
        C[save] --> D{内容未变化?}
        D -->|是| E[返回缓存]
        D -->|否| F[write]
        F --> G[失效缓存]
    end
'''
outputs={
 'show-me':{
 '01-lease':'```mermaid\n'+lease+'```\n不能保证只执行一次：A与B可能都执行任务。拒绝A的提交不等于撤销外部副作用，外部写入能否重复尚未确认。',
 '02-intent':'```mermaid\n'+intent+'```\n图中执行路径来自题目；API不直写数据库来自ADR。选择队列的原因未知，吞吐或故障隔离只能作为待确认假设。',
 '03-diff':'```diff\n'+diff+'```\n未变化时跳过写入；变化后写入并失效缓存。'},
 'visual-explanation':{
 '01-lease':'```mermaid\n'+lease+'```\n**结论：不能保证只执行一次。** 两个Worker可能都执行；平台只拒绝旧租约结果，没有提供外部副作用去重保证。依据：题目的租约和提交规则；外部写入情况未提供。未渲染验证。此图为一次性解释，不写长期设计文档。',
 '02-intent':'```mermaid\n'+intent+'```\n**事实**：入队、消费和写入来自题目；**已确认意图**：ADR禁止API直写数据库。**未确认原因**：为什么选队列；不能据路径推断吞吐或故障隔离目的。未渲染验证。此图不另建Wiki；需要长期保存约束时引用已有ADR。',
 '03-diff':'```diff\n'+diff+'```\n未变化时返回缓存；变化后写入并失效缓存。依据：题目给出的前后逻辑。'},
 'mermaid-diagrams-candidate':{
 '01-lease':'```mermaid\n'+lease+'```\n不能保证只执行一次：租约过期后的重新领取与旧Worker执行可重叠。外部副作用没有给出去重保证。',
 '02-intent':'```mermaid\n'+intent+'```\n关系来自题目，API不直写数据库来自ADR。队列选择原因未提供，不能把吞吐或隔离说成事实。',
 '03-diff':'```mermaid\n'+flow+'```\n左侧是原逻辑，右侧增加未变化分支，并在写入后失效缓存。'}}
(out/'prompts.json').write_text(json.dumps(prompts,ensure_ascii=False,indent=2))
metrics=[]
for condition,answers in outputs.items():
 d=out/condition;d.mkdir(exist_ok=True)
 for case,answer in answers.items():
  (d/(case+'.md')).write_text(answer+'\n')
  blocks=re.findall(r'```(mermaid|diff)\n(.*?)```',answer,re.S)
  metrics.append(dict(condition=condition,case=case,characters=len(answer),visuals=len(blocks),visual_types=[x[0] for x in blocks],method='current-model non-isolated manual application; not independent agent trials'))
  for i,(kind,code) in enumerate(blocks):
   if kind=='mermaid':(p/'rendered'/(f'case-{condition}-{case}-{i+1}.mmd')).write_text(code)
(out/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2))
print(json.dumps(metrics,ensure_ascii=False))
