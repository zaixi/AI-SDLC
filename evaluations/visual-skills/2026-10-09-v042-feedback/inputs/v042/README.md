# Visual Explanation

把当前内容转换为更容易理解的视觉表达，适用于编程、业务、教学及其他领域。当前版本为 **0.4.2**。

核心文件是 [SKILL.md](SKILL.md)，保留show-me的完整表达主体，仅补充忠实表达、验证交付和mermaid-diagrams主动加载适配。

## 目标与范围

输入是当前任务已经提供或读取的内容；输出是图、树、时序、状态、伪代码、diff、SVG或HTML，以及必要的简短说明。

本Skill负责选择表达形式、保留原意、控制信息密度并检查图的显示。不独立研究内容、核实现有系统、作领域决策、安排验证任务或制定知识保存策略。这些工作由调用它的任务负责；本Skill按调用者要求展示或保存。

选图、细节深度和可读性沿用show-me，不再维护平行的选图指引或重复示例。

## 接入与交付

- 将本目录安装到客户端支持的Skill位置，保留references。它不绑定某个Agent，也不依赖安装特定绘图包。
- 上层入口可使用指针：**需要用视觉表达帮助理解当前内容时，使用visual-explanation。**
- 未设置仅允许用户手动触发的标志；实际发现、自动匹配和调用方式由客户端决定。
- 默认会话展示；需要文件时保留可编辑源，按当前任务要求交付。环境支持且任务允许时，渲染并检查实际画面，修正明显布局问题后重新检查；调整时保留原有主体、关系和条件。无法渲染或仍有未解决的显示问题时如实说明，不将语法通过当作布局或内容正确性证明。

0.4.1完成了[三组、每组两题的独立生成比较](../../evaluations/visual-skills/2026-10-09-v041/README.md)，未发现实质内容遗漏或错误转换，六张图通过语法解析；当轮没有实际渲染或客户端安装/调用测试。结果不证明普遍质量提升。后续生成比较每组默认2～3份独立输出。

后续[选图、拆图与C4比较](../../evaluations/visual-skills/2026-10-09-challenge/README.md)保留了六份首次回答及14张实际渲染图：语法全部通过，专用C4图仍有标签重叠和连线穿过节点的问题。0.4.2据此补强“验证与交付”，明确检查实际画面、修正明显问题并重新渲染；show-me正文与Mermaid主动加载规则保持原样。该轮没有把渲染结果回传生成器，尚未验证0.4.2的修图效果。

## 来源与更新

复用[Humanlayer show-me固定提交](https://github.com/humanlayer/skills/blob/ca7c8088db69e315a8b2deea43820270457f8f3c/plugins/show-me/skills/show-me/SKILL.md)的完整正文，保留[上游原文件](references/show-me.upstream.md)和[MIT许可证](LICENSE)。更新时比较固定原文件，独立评估上游元数据与本地补充，避免覆盖客户端调用设置；尚无自动拉取上游机制。

## Mermaid 的主动补充

show-me负责表达形式选择；选择Mermaid后，本Skill主动使用环境允许模型调用的mermaid-diagrams，补充图种与语法细节，不需用户另行触发。指引可以直接加载，也可通过客户端支持的调用接口使用。

用户指定的来源是[aiskillstore/marketplace的softaworks/mermaid-diagrams](https://github.com/aiskillstore/marketplace/tree/main/skills/softaworks/mermaid-diagrams)，[固定快照与旧版比较](../../evaluations/visual-skills/2026-10-09-isolated/README.md)已归档。没有把它复制成当前Skill依赖；未安装或只支持手动触发时直接生成Mermaid。语法解析和渲染另用可用工具，不把指引当作渲染器。

本轮0.4.1两题都主动读取了已提供的本地Mermaid指引，show-me也有一次自行读取。这个观察不等同于客户端自动发现或原生委托接口已验证；这些仍未测试。

另做了[每组两题的复杂图比较](../../evaluations/visual-skills/2026-10-09-complex/README.md)：show-me组禁止读取Mermaid指引，仍准确表达了复杂并发时序和领域数量关系；额外指引组提供更多图内细节，未显示明确正确性优势。此结果仅覆盖两种图，不证明指引无用或所有复杂图必须加载。本轮保留现有规则，未执行真实布局验证。

## 历史记录

0.3.x曾混入工程流程与知识管理要求，已从当前指引移除。历史版本、原始输出和结论保留在[evaluations](../../evaluations/visual-skills/)；这些比较针对旧版本，不代表当前版本的效果。

- [旧版工程解释说明](../../evaluations/visual-skills/history/engineering-skill-readme.md)
- [旧版实验设计及示例入口](../../evaluations/visual-skills/history/refinement.md)
