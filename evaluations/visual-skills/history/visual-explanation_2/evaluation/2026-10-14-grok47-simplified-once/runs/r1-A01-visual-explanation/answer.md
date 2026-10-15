我先读取题目要求的 skill 文件，再按其中的规范完成这次改动说明。

`store` 成功之后、`acknowledge` 之前插入 `audit`。`audit` 失败则直接抛出，不调用 `acknowledge`。`decode` 和 `store` 的失败语义不变。

```diff
 ingest(raw)
   record = decode(raw)       # 抛错 → 直接抛出，后续不执行
   store(record)              # 成功后才继续
+  audit(record.id)           # 失败 → 不 acknowledge，直接抛出
   acknowledge(record.id)
```
