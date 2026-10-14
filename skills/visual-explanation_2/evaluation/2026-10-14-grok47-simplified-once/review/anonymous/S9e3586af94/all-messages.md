The rule now retries only the notification, so I’ll retarget the failure path from “发送通知” back to itself and update that label, leaving the happy path and style unchanged.

The previous diagram is the source of truth, so I’ll only retarget the failure loop onto “发送通知” and change its label.

I’ll render the SVG and check that the failure loop returns only to the notification step.

The screenshot tool rejected that viewport, so I’ll retry with a supported size.

The CLI takes a positional size, so I’ll render the SVG that way.

The failure arrow still leaves the notification step and points toward “结束”. I’ll bring that loop back into “发送通知” only.

已按新规则改好失败路径：通知失败时只回到「发送通知」重试，不再返回「执行任务」。正常路径和其他文字、样式未改。

文件：`/work/answer.svg`
