
# 技能
技能（Skill）是一种能力封装机制，用于将专业知识（如编码经验、常见问题、解决方案等）组织为可复用的模块。技能本质上是由指令、脚本和资源构成的集合，智能体可按需动态加载这些专业化的"技能包"，从而提升特定任务的执行能力与执行效率。
表1技能与其他功能的对比 
| 对比维度     | 规则（Rule）                                                                      | 技能（Skill）                                                                    | MCP Server                                                        |
|:---|:---|:---|:---|
| **定义**   | 用于约束智能体的行为方式。                                                                 | 用于描述如何完成特定任务。                                                                | 提供外部工具的调用能力。                                                      |
| **加载方式** | 在对话开始时加载到上下文中，持续参与推理。                                                         | 按需加载，减少上下文占用。                                                                | 不参与推理过程，按需调用外部接口。                                                 |
| **使用场景** | 定义代码规范、输出格式、团队协作约定等。 例如：代码必须符合PEP8规范。 | 封装测试流程、开发任务、复杂业务逻辑等。 例如：执行UI自动化测试。 | 连接外部系统，执行具体操作。 例如：控制浏览器操作。 |
| **关键区别** | 控制智能体"应该怎么做"，是行为边界。                                                           | 解决"如何完成任务"，是流程指导。                                                            | 提供"调用工具的能力"，是执行能力。                                                |
   
华为云码道代码智能体支持创建**本地** 和**云端**两种类型的技能：本地技能在客户端创建，云端技能在控制台创建。
本章节介绍在客户端管理技能的操作，如需在控制台管理云端技能，请参考[管理技能和规则中心](https://support.huaweicloud.com/usermanual-enterprise/codeartsagent_enterprise_0028.html)。
 #### 技能的目录结构
技能是一个包含**必需的SKILL.md文件** 和其他**可选的捆绑资源** 的结构化目录，打包完成特定任务所需的知识和工具。
```
skill-name/
├── SKILL.md (必填)
│   ├── YAML frontmatter 元数据 (必填)
│   │   ├── name: (必填)
│   │   └── description: (必填)
│   └── Markdown 指令 (必填)
└── Bundled Resources/ 捆绑资源 (选填)
    ├── scripts/      - 可执行代码 (Python/Bash 等)
    ├── references/   - 旨在根据需要加载到上下文中的文档
    └── assets/       - 输出中使用的文件 (模板、图标、字体等)
```
表2技能参数说明 
| 参数名称                  | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|:---|:---|
| skill-name            | 整个技能的根目录，skill-name需要替换成实际的技能名称（比如data-analysis-skill）。技能名称由小写字母、数字和连字符（-）组成，开头和结尾不能是连字符，且连字符不可连续使用，长度1\~64字符。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| SKILL.md              | **SKILL.md文件名不可修改。**它是技能的核心描述文件，相当于技能的"说明书"，必须包含以下两部分： - **YAML frontmatter元数据** ：放在SKILL.md文件的最顶部，以"---"首尾包裹，是AI可解析的结构化信息。包含name和description两个字段。 - **name** ：技能名称，由小写字母、数字和连字符（-）组成，开头和结尾不能是连字符，且连字符不可连续使用，长度1\~64字符。**name必须与skill-name保持一致**。  - **description**：技能描述，长度不超过1024字符。该字段对华为云码道代码智能体识别技能的使用场景至关重要，需清晰描述技能功能及适用触发条件。    - **Markdown指令**：YAML元数据下方的Markdown内容，用于详细说明技能的使用方法、参数、示例和依赖等。   |
| Bundled Resources（可选） | 存放技能配套资源的目录，非必填，但能让技能更完整。 - **scripts/** ：存放技能的可执行脚本，例如Python脚本、Shell脚本等，实现**确定性操作**。  - **references/** ：存放技能依赖的参考文档，例如API文档、领域知识、公司政策等，是给智能体的**知识库**，这些文档会在技能执行时按需加载到上下文。  - **assets/**：存放资源文件，例如字体资源、公司Logo、PPT模板等，直接在智能体生成的输出中使用，不需要被加载到上下文窗口。                                                                                                                                                                                                                                                                  |
   
 #### 编写SKILL.md
创建一个带有YAML frontmatter和Markdown内容的SKILL.md文件，样例如下：
```
---
name: safe-file-reader
description: Read files without making changes. Use when you need read-only files access.
---
# Safe File Reader
This Skill provides read-only file access.
## Instructions
1. Use Read to view file contents
2. Use Grep to search within files
3. Use Glob to find files by pattern
```
#### 添加支持文件
在SKILL.md同级目录下创建其他文件，样例如下：
```
my-skill/
├── SKILL.md
├── reference.md
├── examples.md
├── scripts/
│   └── helper.py
└── templates/
    └── template.txt
```
在SKILL.md中写明引用这些支持文件，样例如下：
```
For advanced usage, see [reference.md](reference.md).
Run the helper script:
```bash
python scripts/helper.py input.txt
```
```
#### 技能分类
技能分为**系统内置** 、**市场内置** 与**自定义**三大类型，分别对应开箱即用的底层基础能力、经过实战验证的行业专业能力，以及灵活可定制的拓展能力，全方位满足智能体在各类场景下的任务处理需求。
表3技能分类 
| 分类   | 说明                                                                                                             |
|:---|:---|
| 系统内置 | 系统预置基础技能，全局可用且开箱即用。无需额外配置，即可享受稳定、持续的基础功能支持。 **如果停用内置技能，会限制智能体处理相关任务的能力。** |
| 市场内置 | 系统预置专家技能，涵盖单元测试、代码评审、文档生成、安全检查、编译构建及代码重构等核心领域。所有技能均经过自动化测试与规范审查，旨在为开发者提供专业、可靠的能力支撑，助力高效开发。                     |
| 自定义  | 支持用户根据业务需求自主开发或导入技能，实现高度定制化扩展。自定义技能的具体分类见[表4]。                    |
   
#### 本地自定义技能分类
 表4本地自定义技能分类 
| 作用范围 | 说明                                                                                                       |
|:---|:---|
| 项目级  | 仅针对当前项目生效，存储在本地。 存储路径：项目根目录的"./.codeartsdoer/skills/"           |
| 个人级  | 针对当前用户下的所有项目生效，存储在本地。 存储路径：本地"%USERPROFILE%/.codeartsdoer/skills" |
   
#### 约束与限制
若存在**名称相同**的技能，调用优先级为：云端企业级 \> 云端团队级 \> 本地项目级 \> 本地个人级 \> 云端个人级 \> 系统内置。
#### 创建本地技能
华为云码道代码智能体客户端支持创建**项目级** 与**个人** **级** 两种类型的技能，存储在本地。除直接创建技能外，您还可通过**导入现有文件** 或**从** **技能市场安装**来快速集成技能。多种途径灵活高效，助您轻松扩展开发能力。
- [通过npx命令安装技能]
- [从技能市场添加技能]
- [手动创建本地项目级技能]
- [手动创建本地个人级技能]
- [通过导入方式添加技能]
华为云码道代码智能体支持通过npx命令安装**个人级** 或**项目级**技能。
1. 参考[官方文档](https://docs.npmjs.com/cli/v11/configuring-npm/install)，安装Node.js、npm。
   
   安装完成后，在终端中执行如下命令，验证Node.js、npm是否安装成功。
   ```
   npx -v
   ```
   回显信息中显示版本号，表示已成功安装Node.js和npm。
   
   
2. 执行如下命令，安装技能。 
   本步骤以安装**个人级** 的vercel-react-best-practices技能为例进行介绍。
   ```
   npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-best-practices -a codearts-agent
   ```
   其中，*https://github.com/vercel-labs/agent-skills* 为待安装技能包所在的地址，*vercel-react-best-practices*为待安装技能的名称。
   
   
3. 选择技能的作用范围（Project为项目级技能，Global为个人级技能），此处以**个人级** 技能为例。
   
   图1选择技能的作用范围
   ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002625203483.png "点击放大")
   
   
4. 根据提示，选择Yes并继续回车，等待技能安装完成。 
   提示"Installed 1 skill"回显信息时，说明技能安装成功。
   图2安装成功的回显
   ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002594684126.png "点击放大")
   
   
5. 查看已安装的技能。 
   - 进入本地"%USERPROFILE%/.codeartsdoer/skills"目录下，可查看到目标技能vercel-react-best-practices。
   
   - 在华为云码道代码智能体IDE设置页面的"技能与规则 \> 个人级"页签中，可查看到目标技能vercel-react-best-practices，且状态为已开启。
   
   
   
   
6. 使用技能。 
   在华为云码道代码智能体聊天窗口的输入框中，输入以下内容，单击发送图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002625165910.png)。
   ```
   使用vercel-react-best-practices技能重构代码
   ```
   若返回信息中提示技能已加载，说明技能已被成功调用，AI将通过此技能重构该项目下的React和Next.js代码。
   
   
 
市场上已上线多款开箱即用的技能，可帮助您快速提升开发效率。以下将介绍如何查找并添加这些技能。
1. 参考[快速启动](https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0002.html)操作，登录华为云码道代码智能体IDE。
2. 单击华为云码道代码智能体IDE右上角的设置图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002608528733.png)，进入全局设置页面。
3. 在左侧导航栏中单击"技能与规则"，进入"全部已安装"页面。
4. 在"市场"页签中，查找技能。 
   表5查找技能 
   | 查找方式 | 具体步骤                                                                                                                                                                                                                                                                                                                                                                                        |
   |:---|:---|
   | 来源   | 市场中的技能主要来源于**官方** 和**优选**。 - 官方：华为云码道代码智能体提供的技能。  - 优选：经筛选的第三方技能。   在页面顶部的"全部来源"下拉框中，选择技能的来源，查看对应来源的技能列表。您还可以在搜索框中输入技能名称或者关键字快速查找技能。 |
   | 名称   | 在页面右上角单击"按名称"后的排序图标，按名称排序查找技能。                                                                                                                                                                                                                                                                                                                                                              |
   | 更新时间 | 在页面右上角单击"最近更新"后的排序图标，按更新时间排序查找技能。                                                                                                                                                                                                                                                                                                                                                           |
      
   
   
5. 添加技能。 
   1. 通过以下任一方式，弹出选择技能安装位置对话框。
      - 在指定技能后，单击添加图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002608141849.png)。
      
      - 单击指定技能的名称，进入技能详情页面。在技能详情页右上角，单击"添加"。
      
      
      **若已创建/导入的技能名称和市场中已有技能重名，该技能在市场中将显示为"已安装"。**
      
   
   2. 选择该技能的安装位置（**项目级** 或**个人级** ），单击"确定"。
      安装成功后，该技能后的 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002577621966.png) 变为"已安装"。
      
   
   
   
   
6. （可选）根据实际场景，执行更新技能、修改技能安装位置和卸载技能的操作。 
   表6管理技能 
   | 操作       | 具体步骤                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
   |:---|:---|
   | 更新技能     | 若已创建/导入的技能名称和市场中已有技能重名，且二者版本不同，该技能在市场中将显示为"已安装"且"待更新"。**若执行更新操作，会以市场中技能的内容覆盖原先的内容。** 通过以下任一方式，更新技能。 - 将鼠标悬浮在待更新技能上，单击更新图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002577621954.png)。更新成功后，该技能右上角的"待更新"标识将自动消失。  - 单击待更新技能的名称，进入技能详情页面。在右上角单击"更新"。更新成功后，该技能右上角的"待更新"标识将自动消失。                                                         |
   | 修改技能安装位置 | 1. 单击待修改安装位置的技能名称，进入技能详情页面。  2. 单击右上角的"项目级"或"个人级"，在弹出对话框中选择目标安装位置。 当技能安装位置由原先位置变为修改后的位置时，表示修改成功。                                                                                                                                                                                                                                                                                                       |
   | 卸载技能     | 通过以下任一方式，卸载技能。 - 将鼠标悬浮在待卸载技能上，单击卸载图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002577501996.png)。卸载成功后，![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002577501990.png) 变为 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002607981949.png)。  - 单击待卸载技能的名称，进入技能详情页面。在右上角单击"卸载"。卸载成功后，右上角"卸载"和"项目级"/"个人级"按钮变为"添加"。   |
      
   
   
 
为**当前项目** 定制的技能，随代码库一并分发。**本地项目级技能创建后立刻生效，何时使用由智能体决定。**
1. 参考[快速启动](https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0002.html)操作，登录华为云码道代码智能体IDE。
2. 单击华为云码道代码智能体IDE右上角的设置图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002608528733.png)，进入全局设置页面。
3. 在左侧导航栏选择"技能与规则"，进入"全部已安装"页面。
4. 在"项目级"页签中，单击技能后的 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002577501950.png)，进入创建技能页面。
5. 参考[表7]设置本地项目级技能参数。
   
    表7本地项目级技能参数说明 
   | 参数      | 说明                                                                                                                                 |
   |:---|:---|
   | Skill名称 | 新建项目级技能的名称，例如data-cleaner-skill。 命名规则：由小写字母、数字和连字符（-）组成，开头和结尾不能是连字符，且连字符不可连续使用，长度1\~64字符。 |
   | Skill描述 | 技能的描述信息，长度不超过1024字符。                                                                                                               |
   | 指令      | 技能的指令，用于详细说明技能的使用方法、参数、示例和依赖等。长度不超过50000字符。                                                                                        |
      
   
   
6. 单击"确定"，完成技能的创建。 
   在"项目级"页签中，可以查看到新创建的本地项目级技能。技能创建完成后默认处于开启状态，其文件存储于项目根目录的"./.codeartsdoer/skills"。
   
   
 
根据您的使用习惯和偏好设定个人级技能，华为云码道代码智能体将始终遵循这些技能，在**所有项目** 中为您提供更贴合个人风格的输出。**本地个人级技能创建后立刻生效，何时使用由智能体决定。**
1. 参考[快速启动](https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0002.html)操作，登录华为云码道代码智能体IDE。
2. 单击页面右上角的设置图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002724039103.png)，进入IDE模式全局设置页面。
3. 在左侧导航栏选择"技能与规则"，进入"全部已安装"页面。
4. 在"个人级"页签中，单击技能后的 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002577501950.png)，进入创建技能页面。
5. 参考[表8]设置本地个人级技能参数。
   
    表8本地个人级技能参数说明 
   | 参数      | 说明                                                                                                                                   |
   |:---|:---|
   | Skill名称 | 新建个人级技能的名称，例如data-validator-skill。 命名规则：由小写字母、数字和连字符（-）组成，开头和结尾不能是连字符，且连字符不可连续使用，长度1\~64字符。 |
   | Skill描述 | 技能的描述信息，长度不超过1024字符。                                                                                                                 |
   | 指令      | 技能的指令，用于详细说明技能的使用方法、参数、示例和依赖等。长度不超过50000字符。                                                                                          |
      
   
   
6. 单击"确定"，完成技能的创建。 
   在"个人级"页签中，可以查看到新创建的本地个人级技能。技能创建完成后默认处于开启状态，其文件存储于本地的"%USERPROFILE%/.codeartsdoer/skills"。
   
   
 
将已获取的本地技能包导入到本地华为云码道代码智能体中，即可便捷地调用和使用相关功能。
![](https://support.huaweicloud.com/usermanual-codeartsagent/public_sys-resources/caution_3.0-zh-cn.png)
导入前，请对照[技能的目录结构]及[编写SKILL.md]中内容，验证技能包是否符合标准。例如，每个技能文件夹的根目录均须包含对应的SKILL.md文件，此文件中须包含YAML格式的技能名称与描述等。如果技能包不符合规范，请调整后再导入，否则可能会导入失败。
1. 参考[快速启动](https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0002.html)操作，登录华为云码道代码智能体IDE。
2. 单击华为云码道代码智能体IDE右上角的设置图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002608528733.png)，进入全局设置页面。
3. 在左侧导航栏单击"技能与规则"，进入"全部已安装"页面。
4. 在"项目级"或"个人级"页签中，单击技能后的"![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002585490954.png) \> 导入"。
5. 在"上传"对话框中，选择本地的技能zip包，单击"确定"。 
   ![](https://support.huaweicloud.com/usermanual-codeartsagent/public_sys-resources/caution_3.0-zh-cn.png)
   每次仅支持上传一个zip包，包内可存放多个技能文件夹，且包的总大小不能超过5M。
   导入成功后，技能名称将显示在技能列表中。
   例如：如需一次性导入"docx"和"pptx"两类技能至华为云码道代码智能体，可将两类技能文件夹放入同一个zip包中，再上传该zip包，即可实现批量上传功能。
   
   
 
#### 使用技能
1. 参考[快速启动](https://support.huaweicloud.com/usermanual-codeartsagent/codeartsagent_ug_0002.html)操作，登录华为云码道代码智能体IDE。
2. 在聊天界面的输入框下方选择"内置 \> 智能体"，切换到**智能体** 模式。右侧显示当前选用的模型，您可在下拉框中切换不同大语言模型。
   
   ![](https://support.huaweicloud.com/usermanual-codeartsagent/public_sys-resources/note_3.0-zh-cn.png)
   如果没有正常显示华为云码道代码智能体的聊天窗口，请在顶部菜单栏的右上方，单击**展开AI侧栏** 图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002608066869.png)，即可打开华为云码道代码智能体。
   
   
3. 通过以下任意一种方式使用技能。 
   - 方式一：直接输入技能名称，调用技能。
     在聊天窗口的输入框中，输入以下内容，单击发送图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002625165910.png)。
     ```
     使用skill-creator生成一个绘图过程需要遵守的规范，名称为drawing-standards，内容如下：
     - 横轴为x轴
     - 纵轴为y轴
     - 原点O(0,0)必须清晰标注
     - 坐标轴箭头、刻度和单位长度要统一
     - 刻度线是细实线
     - 轴线是稍粗实线
     ```
     
   
   - 方式二：通过"/"命令，调用技能。 通过"/"命令调用技能前，需确保**该技能处于"启用"状态** 。输入框中一次最多支持选择**20个**技能。
     在聊天窗口的输入框中，输入"/"，在弹出的菜单中选择"/skill-creator"，输入以下内容，然后单击发送图标 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002625165910.png)。
     ```
     生成一个绘图过程需要遵守的规范，名称为drawing-standards，内容如下：
     - 横轴为x轴
     - 纵轴为y轴
     - 原点O(0,0)必须清晰标注
     - 坐标轴箭头、刻度和单位长度要统一
     - 刻度线是细实线
     - 轴线是稍粗实线
     ```
     图3通过"/"命令调用技能   
     ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002649960232.png "点击放大") 
   
   
   
   
4. 查看技能调用结果。
 
#### 管理本地技能
华为云码道代码智能体IDE具备完善的技能全生命周期管理体系。用户能够基于实际业务场景，实现对既有技能的精细化管控与持续优化。
表9管理本地技能 
| 操作          | 具体步骤                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|:---|:---|
| 启用或停用本地技能   | 在华为云码道代码智能体IDE设置页面的"技能与规则 \> 项目级 \> 技能"/"技能与规则 \> 个人级 \> 技能"中，可通过开关启用或停用本地技能。 创建**项目级技能** 时，华为云码道代码智能体会在项目根目录的"./.codeartsdoer/skills/"路径下生成一个名为"ProjectSkillStatus.txt"的文件，用于记录项目中各个技能的开关状态。每一行记录一个技能的状态，格式为**技能名=true（表示启用）或技能名=false（表示停用）**。 删除某个技能后，"ProjectSkillStatus.txt"文件中对应的记录也会同步删除，确保文件内容与项目状态保持一致。 图4ProjectSkillStatus文件示例 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002607981945.png "点击放大") |
| 批量启用或停用本地技能 | 1. 在华为云码道代码智能体IDE设置页面的"技能与规则 \> 项目级 \> 技能"/"技能与规则 \> 个人级 \> 技能"中，单击右上角的"![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002585490954.png) \> 批量操作"。  2. 勾选目标技能，选择右上角的"开启"或"关闭"，批量启用或停用本地技能。                                                                                                                                    |
| 编辑本地技能      | 在华为云码道代码智能体IDE设置页面的"技能与规则 \> 项目级 \> 技能"/"技能与规则 \> 个人级 \> 技能"中，将鼠标悬浮在目标技能上，单击 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002608141813.png)，即可对技能进行修改。                                                                                                                                                                                                                                                                                                                                                                               |
| 删除本地技能      | 在华为云码道代码智能体IDE设置页面的"技能与规则 \> 项目级 \> 技能"/"技能与规则 \> 个人级 \> 技能"中，将鼠标悬浮在目标技能上，单击 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002608141825.png)，即可删除技能。 目标技能从技能列表中移除，表示技能删除成功。 注意： 技能删除后，使用该技能的智能体将受到影响，且删除的技能不可恢复，请谨慎操作。                                                                                                                                                                                           |
| 查看本地技能      | 在华为云码道代码智能体IDE设置页面的"技能与规则 \> 项目级 \> 技能"/"技能与规则 \> 个人级 \> 技能"中，将鼠标悬浮在目标技能上，单击 ![](https://support.huaweicloud.com/usermanual-codeartsagent/zh-cn_image_0000002577303620.png)，即可查看技能详情。                                                                                                                                                                                                                                                                                                                                                                                |
   
