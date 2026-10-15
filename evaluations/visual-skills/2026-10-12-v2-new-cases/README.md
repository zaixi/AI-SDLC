# 内层 visual-explanation_2 与 0.4.2：新案例实测

固定仓库提交 `c39ff86918bf896c7d156a2ee5cf204fa779bc34`。候选使用内层 `skills/visual-explanation_2/visual-explanation/`，不是内容与 0.4.2 相同的外层目录。原始输入完整保留，未改任一 Skill。

[画面对照与结论](comparison.md) · [协议](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/protocol.json) · [原始运行记录](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-12-v2-new-cases/runs.json)

每版两个案例、每题一条新容器/新会话轨迹，共四条轨迹。每条轨迹初稿后给予两次同样措辞的真实图片反馈，三个阶段不算三个独立样本。病例为分页导出状态/授权/去重与 P95 延迟绝对值比较；前者迁移此前状态任务，后者增加不同验收上限的数值尺度问题。顺序按题反转，不固定随机种子。

生成器只见自己的任务、固定 Skill 输入和自己图片，不挂载仓库、父会话或其他组回答；CLI read-only sandbox、临时独立用户目录，共享只读登录卷仅用于认证。模型不调用工具。候选主文件及语义参考全文注入，0.4.2 主文件含完整 show-me；不测试真实客户端自动发现和按需读取。

本轮两组均声明无可选 mermaid-diagrams、diagram-design、answer-me-with-html/am。测试直接生成/回退路径，不证明可选 Skill 接入有效，也不能据此评估 am 的成本或绘图质量。图形渲染由相同外部控制器提供。

使用此前固定浏览器镜像、Node/npm 锁、Mermaid 12.1.0 / CLI 12.0.0、Chromium 154.0.8037.92；HTML 禁用脚本与网络，在 1600×1000 桌面视口截图主 SVG 和整页，390×844 移动视口另供评审检查。模型获得桌面真实图片，移动图不作为额外反馈。Mermaid 实际生成 SVG/PNG；最后若改源，评审再渲染，不给予第三次反馈。

渲染容器无网络，不挂载凭据、Docker socket，根目录和输入只读；浏览器 Puppeteer 的 --no-sandbox 隔离由外层容器提供。HTML 的离线自检和几何脚本来自此前固定 diagram-design 快照，作为额外结构检查并原样回传；不代表加载 diagram-design Skill。几何脚本存在跨独立 SVG 误报及 CSS 箭头识别缺口，退出码不能代替实际看图。

保留原始三阶段回答、CLI 事件、提示、状态、源码、图片与哈希；不人工修改原始回答、不择优替换。实际模型以本轨迹 turn_context 为准。用量及源码规模是本次生成的线索，不是价格、人工维护工时或真实需求修改成本。

主 Agent 知道组别后评审，无独立盲评或阅读实验。每题每组一个样本，结论限定于这两题及此运行方式。

实际完成4条独立轨迹、12次模型调用，turn_context均为 gpt-6.1-sol，没有模型工具调用。最终7张图均实际渲染（5张Mermaid、2张HTML内嵌SVG），5张Mermaid最终源均通过12.1.0语法解析，两份最终HTML离线自检通过。两版流程图最后仍变更图源，模型如实标未检查，评审随后查看最终图；两版数值图保持已反馈版本。
