# CodebaseWiki
CodebaseWiki能够为你的项目生成结构化文档，并且持续同步代码改动以更新文档。当你查询开发知识点、解读代码、新增功能特性时，它还会深度解析项目结构与代码实现，结合知识库与对话上下文给出更精准详尽的回答和文档参考，让智能体充分理解你的代码仓库。
CodebaseWiki自带检索工具Knowledge，智能体需要查询CodebaseWiki内容时会自动调用。
#### 约束与限制
表1约束与限制 
| 限制类别 | 具体限制 |
|:---|:---|
| 代码文件数量                          | 代码文件≤10000个                     |
   
#### 生成CodebaseWiki文件
1. 参考[快速启动](https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0002.html)操作，登录码道IDE。
2. 选择IDE左侧菜单栏中的图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002749367515.png)，再单击"生成"，启动CodebaseWiki文档生成任务。
3. 查看生成的CodebaseWiki文档。 
   任务执行完成后，会自动生成如下两个文件夹，同时会在你的项目中新建一个专属目录".codeartsdoer/.codebase/branches/分支名/docs"用于存放上述文件夹。
   - **codebase-knowledge**：存放代码库全局知识，即整个代码仓库的通用信息。
   
   - **project-knowledge**：存放项目专属知识，即本项目业务相关信息，包含业务说明、项目配置、业务流程等。
   
   
   图1文档成功生成   
   ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002749257711.png "点击放大")
   
   
4. 更新已生成的CodebaseWiki文档。 
   CodebaseWiki并非静态文档，而是与代码保持同步。初次生成完成后，系统会持续监控代码改动。当你修改了代码文件后，系统会识别出代码与CodebaseWiki文档存在差异。此时，你只需单击"更新"，即可重新生成受改动影响的文档片段。
   
   
 
