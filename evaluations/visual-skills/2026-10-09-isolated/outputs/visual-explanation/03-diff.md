```diff
 on(save)
+  if content is unchanged
+    return cached result
   write content
+  invalidate cache
```

以前每次 `save` 都写；现在未变化就返回缓存，变化则先写入、再失效缓存。图中只表达题目给定的正常流程，写入失败时的处理未提供。

来源：题目给定的新旧逻辑。diff 源文本已检查，未渲染验证。
