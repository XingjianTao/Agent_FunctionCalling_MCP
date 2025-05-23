# MCP(Model Context Protocol)
我们将按下面的流程介绍MCP(Model Context Protocol)

## 什么是MCP？
### 痛点
- 统一不同客户端调用工具的接口
- 简化工具函数代码在不同使用者的agent代码中的重复过程
- 简化工作流平台上api schema的配置和维护

### 我的理解（接痛点）
- MCP作为客户端调用工具的统一规范
- MCP架构可以独立于大模型存在

### ChatGPT定义
- Model Context Protocol的准确定义
  - 开放、模型无关的应用层通信协议
  - 核心目标
    1. 统一接口
    2. 动态工具发现与调用
    3. 统一消息格式与安全控制
    4. 开放生态

## MCP的工作过程
### MCP工作流程组成
1. MCP_Server的创建与注册
2. MCP_Server与客户端（MCP_Client）的交互
3. 客户端（MCP_Client）与大模型的交互
### MCP工作流程结合流程图介绍
### 完整工作流程解读

## 什么是MCP？
我们下面叙述了对MCP产生前工具调用的痛点，以及对MCP，的个人理解。接着介绍了ChatGPT给出的准确定义，我们在后面结合代码的讲解中会努力让你理解这些要点，
### 痛点
在下图所示的本地工具-客户端-大模型的三者交互中，面对大模型返回的调用工具指令，开发者需要调用本地工具或者在线工具，这个过程每个开发者似乎都要进行手动调试，而且有很多工具是不同的客户端都需要重复调用，如果没有一个统一的规范的话，不同的客户端要调用各种语言的工具似乎会很麻烦，不便于工具的调用和共享。


以下是不同up解释的mcp产生的痛点：

- 统一不同**客户端**调用工具的接口(没有mcp之前客户端也可以调用本地或在线工具，只是交互方式不同)：
https://www.bilibili.com/video/BV1AnQNYxEsy?spm_id_from=333.788.recommend_more_video.1&vd_source=ba16f478e6d7f23888c37746ea6756de [01:30]

![[痛点-技术爬爬虾.png|500]]
痛点

- 简化工具函数代码在不同使用者的agent代码中复制粘贴或者文件拷贝的重复过程（不是所有工具都适合挂在网上用http来请求）：
https://www.bilibili.com/video/BV1aeLqzUE6L/?spm_id_from=333.337.search-card.all.click&vd_source=ba16f478e6d7f23888c37746ea6756de [07:30]

![[痛点1.png|500]]
痛点

- 简化工作流平台上api schema的配置和维护（比如某个api更新了版本，输入的参数有变化，此时就要修改api schema）：
但是要注意这里有个误解，就是在本地编程时api schema是可以不需要手写的，所以复杂的api schema的编写是痛点但不是mcp的痛点，使用第三方装饰器 openai_function_call.openai_function可以自动配置api schema。（参见FunctionCallingipynb）
https://www.bilibili.com/video/BV1sWoMYUEi9/?spm_id_from=333.337.search-card.all.click&vd_source=ba16f478e6d7f23888c37746ea6756de [03:00]


![[痛点2.png|500]]
痛点

在后面的代码实例中我们会尝试解释这一痛点，并不是说必须要有一个统一的贵发，但是有一个统一的规范总是好的。



### 我的理解（接痛点）
MCP就是把客户端调用工具做了一个统一的规范，当大模型返回调用工具的指令时，只要客户端把指令翻译成MCP规定的MCPServer的入口格式，那么MCPServer就能解析指令并调用，实际上就算离开客户端和大模型，只要我们给MCPServer符合其入口格式的输入，MCPServer就能为我们服务！即**MCP架构是可以独立于大模型存在的**

MCP（Model Context Protocol）正是为了解决上述痛点而出现的。
它把“模型调用工具”抽象成一层通用协议：

模型侧：只需按 MCP 格式发出调用请求；

工具侧：通过 MCP Server 统一暴露，无论是本地脚本还是在线 API；

客户端/Agent：不再关心工具实现细节，只负责转译并转发符合 MCP 规范的消息。

### ChatGPT定义
**Model Context Protocol（MCP）的准确定义**

Model Context Protocol（简称 **MCP**）是一种**开放、模型无关的应用层通信协议**，用于基于 LLM 的智能体（MCP 客户端）与外部数据源或功能性代码（MCP 服务器）之间进行**双向、安全、标准化的上下文交换和工具调用**。它的核心目标是：

1. **统一接口**

   * 以类似 USB-C 的方式，为任何 AI 模型提供“即插即用”的标准端口，消除不同应用之间各自定制的函数调用或 API 集成成本。([docs.anthropic.com][1])

2. **动态工具发现与调用**

   * MCP 服务器通过 `list_tools` 等消息暴露自身可用工具（函数、检索接口、文件系统等）；
   * MCP 客户端可在对话过程中即时获取、选择并以结构化方式 `call_tool` 执行这些工具；
   * 协议还支持运行时增删工具及变更通知（`notifications/tools/list_changed`）。([modelcontextprotocol.io][2])

3. **统一消息格式与安全控制**

   * 标准化的 JSON-Schema / JTD 描述工具参数与返回值；
   * 规定用户授权、权限边界以及对潜在任意代码执行的安全约束。([modelcontextprotocol.io][3])

4. **开放生态**

   * 由 Anthropic 于 2024-11-25 首次开源发布，并在 2025 年陆续被 OpenAI、Google DeepMind 等主流厂商采纳，形成跨平台的公共标准。([anthropic.com][4], [维基百科][5])

**一句话概括**

> MCP 是为 AI 模型“插上”外部世界的统一协议插口，使模型能够安全、动态地发现和调用各种工具或数据源，并把结果纳入推理上下文，从而实现可扩展的、上下文感知的智能应用。

[1]: https://docs.anthropic.com/en/docs/agents-and-tools/mcp?utm_source=chatgpt.com "Model Context Protocol (MCP) - Anthropic API"
[2]: https://modelcontextprotocol.io/docs/concepts/tools?utm_source=chatgpt.com "Tools - Model Context Protocol"
[3]: https://modelcontextprotocol.io/specification/2025-03-26?utm_source=chatgpt.com "Specification - Model Context Protocol"
[4]: https://www.anthropic.com/news/model-context-protocol?utm_source=chatgpt.com "Introducing the Model Context Protocol - Anthropic"
[5]: https://en.wikipedia.org/wiki/Model_Context_Protocol?utm_source=chatgpt.com "Model Context Protocol"


## MCP的工作过程
![[MCP工作过程1.png|500]]
MCP工作过程1（模块版）

### MCP工作流程组成
MCP的工作过程可以分为三个部分（我们分别在三个文件中介绍）：
1. [[MCP_Server的创建与注册]]
2. [[MCP_Server与客户端（MCP_Client）的交互]]
3. [[客户端（MCP_Client）与大模型的交互]]

**注意**其中3是和MCP协议无关的，可以是Agent中提到的ReAct的SystemPrompt，也可以是xml格式或者JSON格式（应该对应Function Calling，这里需要确认FunctionCalling在微调过程中是否内置了ReAct模式），但是**无论是什么格式都要让LLM使用ReAct（Thought- Observation-Action）的模式处理问题，ReAct是 Resoning- Action的简写。**


### MCP工作流程结合流程图介绍
我们将结合流程图简单介绍：
![[MCP工作过程2.png|500]]
MCP工作过程2（清晰流程）
https://www.bilibili.com/video/BV1aeLqzUE6L/?spm_id_from=333.337.search-card.all.click&vd_source=ba16f478e6d7f23888c37746ea6756de [10:00]

![[MCP工作流程3.png|500]]
MCP工作过程3（完整流程）

https://www.bilibili.com/video/BV19wGozhEQb?spm_id_from=333.788.videopod.sections&vd_source=ba16f478e6d7f23888c37746ea6756de

工作流程图1和图2非常清楚，所以这里解读一下完整版的工作流程图3：
首先创建MCP_Server（黑1），然后MCP_Server和MCP_Client注册（黑2），这里应该对应开始的握手和工具告知list_tools；
执行工作开始：
- 红1：用户首先将指令发送给MCP_Client
- 红2：MCP_Client将指令和工具说明发给LLM，工具说明的部分可以是SystemPrompt也可以是FunctionCalling的JSON格式（但只有经过微调支持FunctionCalling的模型才能识别）
- 红3：LLM把回复返回给MCP_Client，内容中包括需要调用工具的请求，或者不需要调用工具直接返回答案文本
- 红5：MCP_Client把工具请求发送给MCP_Server
- 红6-红7-绿1-绿2：MCP_Server调用tools并执行（通常一个MCP_Server里面可以包括一系列的函数，MCP_Server的名称是这些函数的主题，比如file system这个MCP_Server里面就用很多文件操作的tools）
- 绿3：MCP_Server把tools的执行结果返回给MCP_Client
- 绿4：MCP_Client把结果添加到聊天记录中，**和历史聊天记录一起发送给LLM**（这一点很重要，LLM是没有记忆的）
- 绿5：LLM根据返回结果和历史记录判断是否要继续调用工具（重复红2到绿4）还是已经得到答案可以输出结果（给MCP_Client发送结束标志）
- 绿6：MCP_Client收到LLM的结束标志后，将最终答案发给用户

