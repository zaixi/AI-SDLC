```diff
 on(save)
-  write content
+  if content is unchanged
+    return cached result
+  write content
+  invalidate cache
```
未变化时跳过写入；变化后写入并失效缓存。
