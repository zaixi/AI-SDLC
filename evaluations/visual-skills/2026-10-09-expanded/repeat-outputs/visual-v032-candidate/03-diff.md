```diff
 on(save)
+  if content is unchanged
+    return cached result
   write content
+  invalidate cache
```

未变化时省去写入并返回缓存；变化时先写入，再让缓存失效。
