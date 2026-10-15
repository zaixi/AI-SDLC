当前目录没有源码，按题目给出的模块边界画职责移动示意。这种“哪些挪走、哪些留在原处”用 diff 形的文件树最紧凑。

```diff
  cli/main.py                 # 仍只解析命令行，调用 importer
  web/handler.py              # 仍接收网页上传，调用 importer
  core/importer.py            # 编排入口保留：读 → 洗 → 写
-   # 读取 CSV
-   # 清洗字段
    # 写入数据库              # 留在 importer
+ formats/csv_reader.py       # 承接 CSV 读取
+ core/cleaner.py             # 承接字段清洗
```

调用关系不变：`cli/main.py` 和 `web/handler.py` 都只进 `core/importer.py`。Importer 把读取交给 `formats/csv_reader.py`、清洗交给 `core/cleaner.py`，数据库写入仍由自己完成。