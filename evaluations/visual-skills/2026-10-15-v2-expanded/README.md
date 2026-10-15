# 增补三例：visual-explanation_2 与 0.4.2

[实际画面对照](comparison.md) · [协议](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-15-v2-expanded/protocol.json) · [原始运行记录](https://github.com/zaixi/AI-SDLC/blob/b52aa156e6f6a6dca1d0aee0ebf3b227d62f2475/evaluations/visual-skills/2026-10-15-v2-expanded/runs.json) · [前两例比较](../2026-10-14-v2-v042/comparison.md)

固定仓库提交 `be90ca2390a34d8246318f77de6c0479bd746e18`。两组 Skill 与上一轮完全相同；本轮只增加案例，不更改规则、不复用旧回答。每版三题、每题一个独立容器/会话，共六条新轨迹；每条初稿后两次同等真实桌面图片反馈，三阶段不当作三个独立样本。

原题来自冻结版维护题库：C03缺失数据趋势、B03两站独立实例与补传反向关系、D04已有SVG只改通知失败环路。D04完整源内联提供，并在 inputs/fixtures 保存原文件。模型不见评审标准、旧答案、其他组结果或维护材料。主文件全文注入，没有真实客户端自动发现测试。

两组均无可选 mermaid-diagrams、diagram-design、answer-me-with-html/am；模型不调用工具，外部控制器同等提供渲染。因此测试直接生成/回退质量，不验证可选后端接入、绘图库选择或自动工具发现。趋势题按任务要求静态离线HTML；架构题允许Mermaid/HTML/SVG；局部修改题交付原生SVG。标准绘图库的自主使用不在此协议范围内。

每条轨迹独立临时home、容器和会话，仅挂载自己的输入、图片和只读登录卷；CLI read-only sandbox，不挂载仓库、父会话、其他组产出、Docker socket。条件执行顺序按题交替，不固定采样种子。实际模型以本轨迹turn_context为准。

渲染版本沿用前轮固定镜像、锁文件：Mermaid 12.1.0、CLI 12.0.0、Chromium 154.0.8037.92。渲染容器网络禁用、无凭据、根目录/输入/工具只读；Puppeteer --no-sandbox隔离由外层容器提供。HTML/原生SVG禁用脚本和远程请求。桌面1600×1000截图主SVG及完整页面回传；390×844移动截图仅供评审，不多给模型一轮反馈。Mermaid渲染SVG/PNG。最终修改的源另渲染查看，不提供第三次图片反馈。

本轮增加原生SVG路径：直接打开完整SVG，不转成HTML、不改其内容。运行前用原始fixture验证了SVG渲染支持，临时环境检查不算模型样本。SVG XML解析与原始源同时保留。局部修改的核对比较原SVG，区分路径语义、正常路径/文字/样式保留及纯空白格式变化。

HTML离线自检和几何脚本来自既有快照，不作为加载diagram-design的证据。脚本存在跨独立SVG、CSS箭头覆盖缺口，不能代替实际看图；数据比例、缺失值和实例/关系需对照原题。

原始三阶段回答、提示、CLI事件、状态、源文件和图片逐字保留；不手工修答案、不择优替换。主Agent知道组别后评审，没有独立盲评或真人阅读实验。理解效果、忠实性、交付和成本分别说明，不用机械总分。token是本轮调用累计；源码规模受格式影响，不等于价格、人工维护工时或长期效率。

前轮两题与本轮三题可逐题并看，共覆盖五种任务；它们不是同题重复样本，不合并宣称稳定胜率。已有评测和Skill保持不变。

原始通知SVG在模型生成前的渲染截图保存在reference-render，仅供环境验证和评审对照，不作为模型输入图片。模型得到的是相同完整原始SVG源码。

实际完成6条独立轨迹、18次调用，turn_context均为gpt-6.1-sol，无模型工具调用。最终6张图全部实际渲染：4份HTML各含1个SVG，另2份原生SVG。4份HTML离线自检通过，2份原生SVG XML解析通过。没有最终Mermaid源，因此syntax-results.json为0个适用对象，不算Mermaid验证通过。所有最终答复与stage2原始回复逐字一致、输入哈希及原生源哈希核对通过。
