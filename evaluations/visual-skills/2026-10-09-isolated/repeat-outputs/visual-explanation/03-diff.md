```diff
 on(save)
+  if content is unchanged
+    return cached result
   write content
+  invalidate cache
```

旧逻辑每次保存都写入；新逻辑未变化时返回缓存，变化时先写入、再使缓存失效。

依据：题目给定的新旧逻辑；此为伪代码差异，无需渲染。
