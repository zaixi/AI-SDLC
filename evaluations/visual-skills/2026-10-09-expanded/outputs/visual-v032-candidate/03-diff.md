```diff
 on(save)
+  if content is unchanged
+    return cached result
   write content
+  invalidate cache
```

未变化时跳过写入，直接返回缓存；变化时先写入，再失效缓存。
