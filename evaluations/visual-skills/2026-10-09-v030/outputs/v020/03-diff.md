```diff
 on(save)
+  if content is unchanged
+    return cached result
   write content
+  invalidate cache
```

未变化时直接复用缓存；变化时先写入，再失效缓存。来源：题目给出的新旧逻辑。
