# 原生输出比较：diagram-design、show-me 与 visual-explanation 0.4.2

每组两题、每题一条独立生成轨迹，共六条新轨迹。每条保留初稿、第一次图片反馈后的修订稿、第二次反馈后的最终稿；三阶段不算三个独立样本。不复用之前两轮的回答。

[实际画面对照](comparison.md) · [运行记录](runs.json) · [协议](protocol.json) · [输入哈希](input-manifest.json) · [内容评审](content-review.json)

## 输入与原生表达

题目沿用发布体系和跨组织 C4，三组均可选择 Mermaid、HTML＋inline SVG、必要的文字、表格或伪代码。HTML 必须是静态、单文件、离线可用，不限制 diagram-design 为 Mermaid。两题反转三组执行顺序，没有固定随机种子。

- show-me：Humanlayer 固定提交 ca7c8088db69e315a8b2deea43820270457f8f3c 原文件；输入和挂载没有另外两组的指引。
- 0.4.2：当前 visual-explanation，按现有适配提供 Mermaid 指引及所需参考。
- diagram-design：cathrynlavery/diagram-design 固定提交 cdfdc9686cd7465da70b68b036581833b503810c；提供主文件、样式、布局、SVG primitives、语义模式、输出规范、相关图型参考及原始模板。

全文注入，不测客户端原生发现、按需读取或自动触发。这是三组完整使用方式比较，指引、模板及生成策略同时不同，不能单独归因于某条规则。

## 评测样式配置

diagram-design 原始目录完整保留在 inputs/diagram-design-upstream，评测工作副本 inputs/diagram-design 仅把 style-guide.md 的 `Font source: web` 改为 `system`，颜色不变。profiles.md 明确将仅修改字体来源的工作副本识别为 custom-unsaved，支持离线配置，不触发默认未配置状态的首次设置流程。本轮不创建或保存用户 profile，不修改安装源。

操作者预先选择默认配色、离线字体、HTML 默认 doc-wide 画布，并在三组相同提示中声明。这是对授权评测的配置，不代表用户实际品牌偏好；字体比较不声称品牌字体已加载。浏览器记录的是 computed CSS 字体栈，实际系统回退由固定镜像提供中文字体。上述交互流程未作为用户体验测试。

## 隔离与图片反馈

每条轨迹使用新容器、新临时用户目录、新会话，只挂载自己输入、自己图片与只读登录卷；没有仓库、父会话、其他组输出或 Docker socket。CLI read-only sandbox，生成器不调用工具；后续图片只 resume 本条会话。实际模型从该会话 turn_context 读取。

每组都获得两次真实图片及渲染状态反馈，不给人工修图意见。最后若改源码，评审阶段再渲染，不再回传第三次图片，区分生成器检查与评审检查。渲染由外部控制器提供，不证明自主发现渲染器或客户端原生调用。

Mermaid 12.1.0、Mermaid CLI 12.0.0、Chromium 154.0.8037.92。Mermaid 输出实际 SVG/PNG；HTML 在 1600×1000 桌面视口截图每张主 SVG 与完整页面，390×844 移动视口另截图并记录局部滚动。HTML 回传主 SVG 图及完整桌面页面，移动画面用于评审，不作为额外修图机会。原生 HTML 不经过 Mermaid 布局，HTML 文件本身即可编辑源。

渲染容器无网络、不挂载登录卷，根目录/输入/工具只读、cap-drop ALL、no-new-privileges；Chromium 使用已验证的 Puppeteer --no-sandbox 配置，隔离由外层容器提供。HTML 页面脚本禁用，外部请求阻止并记录；本轮无动画。HTML 的 self_check.py --offline 与 verify-geometry.py 在独立无网络只读 Python 容器运行，诊断一起回传；对所有选择 HTML 的组规则相同。脚本通过与实际画面正确、内容正确分别判断。

## 修改成本的观测范围

比较原生可编辑源的规模、本轮实际修图改动量、CLI 报告的 token 使用和工具依赖。这些是修改与生成成本的线索，不是实际需求变更实验、人工维护工时或价格测量。全文注入的输入 token 不代表客户端正常按需加载的最低成本。

## 保留证据与限制

inputs/ 原始来源、评测字体副本、题目和检查脚本；trajectories/ 各阶段原始回答、传入文本、CLI 事件、状态、实际图片与原生源码；outputs/ 是最终回答的逐字副本；scripts/ 是实际驱动和渲染辅助。原始回答与图片不人工编辑，不择优替换。运行驱动拒绝覆盖已有输出目录，依赖本环境 CLI、正常登录卷、Node、Docker 及本地路径；凭据内容不入库。

浏览器镜像与 npm 锁沿用上一轮。Python 检查器镜像固定为 python@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258。

每题每组一个样本，主 Agent 知道组别后评审，没有盲评或用户阅读实验。仅覆盖静态离线中文表达，未验证品牌设置、交互动画、导入流程、真实客户端接入或其他领域。不同格式截图遵循各自原生画布，不能只用 PNG 像素面积推断可读性胜负。

## 运行中断及恢复

diagram-design 第一题首次启动在模型进程创建前因提示文本超过系统单参数长度限制失败，没有产生模型回答；保留 runs.json 失败项及 failed-attempts/。恢复脚本改用 CLI 支持的标准输入传入同一提示，跳过已完成的两条轨迹，不重复抽样。原始驱动与实际恢复驱动均保留在 scripts/。失败启动不计作独立模型样本。

实际完成六条轨迹、18 次模型调用，各次 turn_context 均为 gpt-6.1-sol。最终 19 张图均实际渲染（9 张 Mermaid，10 张 HTML 内嵌 SVG），9 张 Mermaid 最终源通过 12.1.0 语法解析。HTML 三份最终交付的自检均通过；几何检查覆盖范围见 geometry-scope-review.json，不能将零条识别的返回通过称作连线验证。0.4.2 的 C4 最终稿仅更新 HTML 验证说明，SVG/CSS 不变，因此不列作未看过的新图；runs.json 仍保留整个 HTML 变动的事实。

独立 Mermaid 语法检查使用已有 /tmp/ai-sdlc-isolated-tools（Mermaid 12.1.0 与 jsdom），其 package.json/lock 在 scripts/syntax-package*.json 保留；浏览器渲染使用 render-package-lock.json，是另一组运行依赖。
