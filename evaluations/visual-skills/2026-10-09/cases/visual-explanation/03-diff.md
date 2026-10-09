```diff
 on(save)
-  write content
+  if content is unchanged
+    return cached result
+  write content
+  invalidate cache
```
未变化时返回缓存；变化后写入并失效缓存。依据：题目给出的前后逻辑。
