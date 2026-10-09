```diff
 on(save)
+  if content is unchanged
+    return cached result
   write content
+  invalidate cache
```

未变化时复用缓存，省去写入；变化时先写入，再使缓存失效。
