```diff
 on(save)
+  if 内容未变化
+    return 缓存
   write 内容
+  失效缓存
```
未变化时跳过写入并返回缓存；变化时先写入，再让缓存失效。
