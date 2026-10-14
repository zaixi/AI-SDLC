连续相同的字符串压成一段，段与段按原顺序排。比较用 `==`，区分大小写，空白也算字符，不合并不相邻的相同串。

```text
encode_runs(items)
  if items is empty
    return []
  current ← items[0]
  count ← 1
  for each next item
    if next == current
      count ← count + 1
    else
      emit (current, count)
      current ← next
      count ← 1
  emit (current, count)
```

以 `['a','a','b','a']` 为例：

```text
encode_runs
  start run 'a'
    'a' == 'a'  → count 2
    'b' != 'a'  → emit ('a', 2)，另开 'b'
    'a' != 'b'  → emit ('b', 1)，另开 'a'
  end           → emit ('a', 1)
```

结果是 `[('a', 2), ('b', 1), ('a', 1)]`。空列表没有段，直接返回 `[]`。

```python
def encode_runs(items):
    if not items:
        return []
    runs = []
    current = items[0]
    count = 1
    for item in items[1:]:
        if item == current:
            count += 1
        else:
            runs.append((current, count))
            current = item
            count = 1
    runs.append((current, count))
    return runs
```

| 输入 | 输出 |
|---|---|
| `['a','a','b','a']` | `[('a', 2), ('b', 1), ('a', 1)]` |
| `[]` | `[]` |
| `['A','a','a']` | `[('A', 1), ('a', 2)]` |
| `['a ','a']` | `[('a ', 1), ('a', 1)]` |