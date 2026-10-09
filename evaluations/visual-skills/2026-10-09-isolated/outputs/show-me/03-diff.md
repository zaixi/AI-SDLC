```diff
 on(save)
-  write(content)
+  if content is unchanged
+    return cached result
+  write(content)
+  invalidate cache
```

未变化时复用缓存，跳过写入；变化时先写入，再让缓存失效。
