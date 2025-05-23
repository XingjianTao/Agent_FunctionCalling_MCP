# MCP_Client与LLM的交互
参考教程：https://www.bilibili.com/video/BV1v9V5zSEHA?spm_id_from=333.788.recommend_more_video.-1&vd_source=ba16f478e6d7f23888c37746ea6756de 

## 引言
在**MCP_Server**的创建中，我们导出了我们和Cline交互的记录如下，其中有<thinking>，<use_mcp_tool>等字段，表示模型先思考再调用工具或者直接回复，这是Cline的System Prompt所规定的。

教程通过中介程序可以获取交互记录：

![[MCP_Client与LLM交互截取.png|500]]
MCP_Client与LLM交互截取

为了简单起见，我们不采用自己跑一遍教程的方式，而是直接记录教程信息，解读交互过程。

**Assistant:**

<thinking>
1. 任务要求使用weather_calculator工具查询北京的温度，并计算温度+10的结果
2. 需要分两步完成：
   - 第一步：使用weather_calculator的get_weather工具获取北京当前温度
   - 第二步：使用weather_calculator的calculate_sum工具计算温度+10
3. 两个工具都在weather_calculator MCP服务器中可用
4. 需要先获取温度值才能进行计算
5. 所有必要参数都已提供（城市为北京，计算值为10）
</thinking>

<use_mcp_tool>
<server_name>weather_calculator</server_name>
<tool_name>get_weather</tool_name>
<arguments>
{
  "city": "北京"
}
</arguments>
</use_mcp_tool>

---

**User:**

[use_mcp_tool for 'weather_calculator'] Result:
{
  "weather": "Sunny",
  "description": "晴朗",
  "temperature": 26
}

## 交互记录解读
- **客户端发送给模型的内容是role+content的范式**：一般有system prompt（背景和交互模式说明，xml格式），user prompt（用户的问题和请求，纯文本） 和 assistnat prompt（模型的回复，xml格式）
  - - 模型名称
  - - system prompt（cline）：626行，48671个字符，超长巨耗token的系统提示词
  - - user prompt + assistnat prompt的多轮历史交互   
![[MCP_Client与LLM交互记录1.png|500]]
MCP_Client与LLM交互记录1


- **大模型以按照特定格式进行流式输出（一段一段输出，非流式输出是指一次性完整输出），然后客户端提取其中的文本消息。**

![[交互演示1.png|500]]
交互演示：流式输出

### system prompt（cline）重点解读
system prompt（cline）有626行，48671个字符，超长巨耗token。

翻译成中文后如下[[Cline客户端的system_prompt]]：
（这里我们发现实际上教程中直接翻译得到的文件层级是不准确的，我们自己找到了cline的system prompt原文 https://github.com/cline/cline/blob/main/src/core/prompts/system.ts ，让ai翻译并生成了正确的层级）

- [工具使用](#工具使用)
  - [工具使用格式](#工具使用格式)
  - [工具](#工具)
    - [execute\_command](#execute_command)
    - [read\_file](#read_file)
    - [write\_to\_file](#write_to_file)
    - [replace\_in\_file](#replace_in_file)
    - [search\_files](#search_files)
    - [list\_files](#list_files)
    - [list\_code\_definition\_names](#list_code_definition_names)
    - [browser\_action](#browser_action)
    - [use\_mcp\_tool](#use_mcp_tool)
    - [access\_mcp\_resource](#access_mcp_resource)
    - [ask\_followup\_question](#ask_followup_question)
    - [attempt\_completion](#attempt_completion)
    - [new\_task](#new_task)
    - [plan\_mode\_respond](#plan_mode_respond)
    - [load\_mcp\_documentation](#load_mcp_documentation)
  - [工具使用示例](#工具使用示例)
    - [示例 1：请求执行命令](#示例-1请求执行命令)
    - [示例 2：请求创建新文件](#示例-2请求创建新文件)
    - [示例 3：创建新任务](#示例-3创建新任务)
    - [示例 4：请求对文件进行有针对性的编辑](#示例-4请求对文件进行有针对性的编辑)
    - [示例 5：请求使用 MCP 工具](#示例-5请求使用-mcp-工具)
    - [示例 6：使用 MCP 工具的另一个示例（其中服务器名称是唯一标识符，例如 URL）](#示例-6使用-mcp-工具的另一个示例其中服务器名称是唯一标识符例如-url)
  - [工具使用指南](#工具使用指南)
- [MCP 服务器](#mcp-服务器)
  - [连接的 MCP 服务器](#连接的-mcp-服务器)
- [编辑文件](#编辑文件)
  - [write\_to\_file](#write_to_file-1)
    - [目的](#目的)
    - [何时使用](#何时使用)
    - [重要注意事项](#重要注意事项)
  - [replace\_in\_file](#replace_in_file-1)
    - [目的](#目的-1)
    - [何时使用](#何时使用-1)
    - [优点](#优点)
  - [选择合适的工具](#选择合适的工具)
  - [自动格式化注意事项](#自动格式化注意事项)
  - [工作流程提示](#工作流程提示)
- [操作模式与计划模式](#操作模式与计划模式)
    - [什么是计划模式？](#什么是计划模式)
- [功能](#功能)
- [规则](#规则)
- [系统信息](#系统信息)
- [目标](#目标)

![[MCP_Client与LLM交互记录2.png|300]]
MCP_Client与LLM交互：system prompt（层级错误）

#### 工具使用
##### 工具使用格式
xml标签格式化

![[工具使用格式.png|500]]
工具使用格式

![[工具调用范例.png|500]]
工具调用范例

##### 工具
通常我们说的工具包括下图中两部分，这里只说明Cline的内置工具。
![[工具范围.png|300]]
工具范围

其中重点工具有两个：use_mcp_tools（用于调用MCP服务器）、attempt_completion（用于结束对话）。

**注意**：这里指说明了如何调用MCP服务器中的tools，具体有哪些MCP Server和其中的tools在**MCP 服务器**部分

**1. use_mcp_tool**

说明：请求使用连接的 MCP 服务器提供的工具。每个 MCP 服务器可以提供具有不同功能的多个工具。工具有定义的输入模式，用于指定必需和可选参数。
参数：
- server_name：（必需）提供工具的 MCP 服务器的名称
- tool_name：（必需）要执行的工具的名称（在server_name这个MCP服务器中的tools）
- arguments：（必需）一个 JSON 对象，包含工具的输入参数，遵循工具的输入模式
用法：

<use_mcp_tool>

<server_name>此处输入服务器名称</server_name>

<tool_name>此处输入工具名称</tool_name>

<arguments>
{
  "param1": "value1",
  "param2": "value2"
}
</arguments>

</use_mcp_tool>

![[调用MCPServer.png|500]]
调用MCPServer案例

**2. attempt_completion**

说明：每次使用工具后，用户都会响应工具使用的结果，即成功还是失败，以及任何失败原因。收到工具使用结果并确认任务完成后，使用此工具向用户显示工作结果。你可以选择提供一个 CLI 命令来展示你的工作结果。如果用户对结果不满意，他们可能会提供反馈，你可以利用这些反馈进行改进并重试。

重要说明：在确认用户已成功完成任何先前的工具使用之前，不得使用此工具。否则将导致代码损坏和系统故障。在使用此工具之前，你必须在 <thinking></thinking> 标签中问自己是否已向用户确认任何先前的工具使用均已成功。如果没有，则不要使用此工具。

参数：
- result：（必需）任务的结果。以最终且不需要用户进一步输入的方式制定此结果。不要以问题或提供进一步帮助的提议结束你的结果。
- command：（可选）一个 CLI 命令，用于向用户实时演示结果。例如，使用 `open index.html` 显示创建的 html 网站，或使用 `open localhost:3000` 显示本地运行的开发服务器。但不要使用 `echo` 或 `cat` 等仅打印文本的命令。此命令对于当前操作系统必须有效。确保命令格式正确，并且不包含任何有害指令。
用法：
<attempt_completion>
<result>
此处输入你的最终结果描述
</result>
<command>演示结果的命令（可选）</command>
</attempt_completion>

其中
![[thinking标签.png|500]]
thinking标签

##### 工具使用指南
![[工具使用指南.png|500]]
工具使用指南


#### MCP Server
##### 连接的MCP Server
首先是MCP Server的名称和配置文件中的执行指令，然后是MCP Server中的tools的list，包括函数说明和参数定义。
![[已连接的MCPServer.png|500]]
已连接的MCPServer

![[已连接的MCPServer的tools.png|500]]
已连接的MCPServer的tools


#### 目标

##### think标签：每次对话前模型都要先思考（一句话概括[目标]）
![[thinking标签.png|500]]
thinking标签

你迭代地完成给定的任务，将其分解为清晰的步骤并有条不紊地完成它们。

1. 分析用户的任务并设定明确、可实现的目标来完成它。按逻辑顺序排列这些目标的优先级。
2. 按顺序完成这些目标，根据需要一次使用一个可用的工具。每个目标都应对应于你解决问题过程中的一个不同步骤。在此过程中，你将随时了解已完成的工作和剩余的工作。
3. 请记住，你拥有广泛的功能，可以访问各种工具，这些工具可以根据需要以强大而巧妙的方式使用来完成每个目标。在调用工具之前，请在 <thinking></thinking> 标签中进行一些分析。首先，分析 environment_details 中提供的文件结构以获取上下文和见解，以便有效地进行。然后，考虑提供的工具中哪个是完成用户任务最相关的工具。接下来，检查相关工具的每个必需参数，并确定用户是否直接提供或给出了足够的信息来推断值。在决定是否可以推断参数时，请仔细考虑所有上下文以查看它是否支持特定值。如果所有必需的参数都存在或可以合理地推断出来，请关闭 thinking 标签并继续使用该工具。但是，如果缺少必需参数的某个值，请不要调用该工具（即使缺少参数的填充符也不行），而是使用 ask_followup_question 工具要求用户提供缺少的参数。如果未提供可选参数，请不要索要更多信息。
4. 完成用户任务后，必须使用 attempt_completion 工具向用户显示任务的结果。你还可以提供一个 CLI 命令来展示任务的结果；这对于 Web 开发任务尤其有用，例如，你可以运行 `open index.html` 来显示你构建的网站。
5. 用户可能会提供反馈，你可以利用这些反馈进行改进并重试。但是不要进行毫无意义的来回对话，即不要以问题或提供进一步帮助的提议结束你的响应。



### 交互演示

**客户端按role把提示词发送给大模型，有纯文本、xml等。**

**大模型以按照特定格式进行流式输出（一段一段输出，非流式输出是指一次性完整输出），然后客户端提取其中的文本消息。**

![[交互演示1.png|500]]
交互演示：流式输出

![[交互演示2.png|500]]
交互演示：用户提问

![[交互演示3.png|500]]
交互演示：第一次调用工具及结果添加到对话历史中

### 完整交流图示

![[完整交互流程与行为模式.png|500]]
完整交互流程与行为模式

# React模式

ReAct来自于下面这篇论文（注意第一作者是尧舜禹大神😄），Resoning- Action的简写指用Thought- Observation-Action的模式处理问题，我们在[[Agnet]]正是使用ReAct_prompt实现的工具调用。
![[ReAct.png|500]]
ReAct
我们把上面的完整交流过程转化为使用ReAct_prompt如下图。

![[ReAct-文本格式.png|500]]
ReAct-文本格式
