```diff
 on(save)
+  if content is unchanged
+    return cached result
   write content
+  invalidate cache
```

未变化时直接复用缓存；变化时先写入，再使缓存失效。
