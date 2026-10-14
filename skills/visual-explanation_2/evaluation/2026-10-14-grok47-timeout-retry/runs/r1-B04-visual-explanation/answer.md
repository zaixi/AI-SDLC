The three optional cases are the point of the diagram, so a plain cardinality ER would hide them. I’ll draw a conceptual ER plus three concrete examples: a course with no sessions, a session taught by two instructors, and a session with no room. No fields, keys, or conflict rules — those are still undesigned. Style stays the default editorial skin.

The model is only three entities, so the diagram is split: cardinality on top, and three worked examples underneath so empty courses, co-teaching, and unused rooms stay visible. No fields or keys.

I’ll put the relationship model and the three concrete cases in one page so schedulers can see cardinality and the empty cases together.

The model itself is small. The page shows the three cardinalities, then three concrete situations so “no session,” “two instructors,” and “no room” are visible rather than only written as 0..1 or 0..*.

The page is written. I’ll render it and check that the three cases and the cardinality labels stay readable.


The screenshot tool rejected that size. I’ll check its usage and the diagram scripts, then retry.

The screenshot tool takes width and height as separate arguments. I’ll rerun it that way and read the page back.


The page rendered and the accessibility check passed. I’ll look at the image to catch overlapping labels or cramped boxes.

The first drawing put 1..2 on the wrong end of the instructor line, so a session looked limited instead of the instructors. I’m correcting the cardinalities and lining each number up with the thing it counts.

Cardinality now sits on the thing being counted. I’ll render again and check the labels against the boxes.

The numbers sit on the right ends now. The “包含” label still covers its line, and the “授课” chips sit on the example arrows. I’ll lift those labels off the strokes.

Labels are clear of the lines. One more render to confirm nothing else collides.

课次是四者的汇合点。一门课可以还没有课次；一节课恰好属于一门课，由 1 到 2 名讲师讲，教室则可以不用。图在 `/work/scheduling-object-relations.html`。

数字写在被计数的那一端：

| 关系 | 靠近这一侧 | 含义 |
|---|---|---|
| 课程 — 课次 | 课程是 1，课次是 0..\* | 每节课只属于一门课；一门课可以没课次，也可以有很多节 |
| 课次 — 讲师 | 课次是 0..\*，讲师是 1..2 | 讲师可以没课，也可以讲很多节；每节课一名或两名，不能没人，也不能三人合讲 |
| 课次 — 教室 | 课次是 0..\*，教室是 0..1 | 一间教室可对应很多节；每节课不占房间，或只占一间 |

下半页用三个例子把空的一侧画出来：线性代数还没有课次，林老师本学期无课；周三第 3 节由周、陈合讲；周五研讨只记了赵老师，不使用教室。教室这条线只记归属，不判断那个时间空不空。字段、主键和冲突策略都还没设计。
