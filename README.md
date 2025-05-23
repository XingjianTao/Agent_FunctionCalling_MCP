# Agent_FunctionCalling_MCP

这个知识库包含关于大语言模型(LLM)的几个核心技术领域的详细笔记和代码实现。主要分为三个核心部分：Agent、Function Calling和MCP，按照学习发展顺序排列。

## 项目结构

```
.
├── Agent/               # Agent相关知识和实现
├── FunctionCalling/     # Function Calling相关知识和实现 
└── MCP/                 # MCP相关知识和实现
```

## Agent (智能代理)

Agent是封装了大语言模型、工具和记忆的结构化框架，通过组合这些元素来完成复杂任务。

### 核心文档
- Agent - Agent的概念、构建流程和示例实现
- Prompt - Prompt的概念、分类、学习资源
- ReAct - ReAct提示词模版

## Function Calling (函数调用)

Function Calling是大语言模型能够调用外部函数的能力，实现与外部世界的交互。

### 核心内容

- 函数调用的基本概念和OpenAI框架下的实现
- 自动为函数生成API Schema的方法
- API Schema定义
- 函数说明的自动生成
- 函数调用流程
- 迭代式函数调用

## MCP (Model Context Protocol，模型上下文协议)

MCP是一种开放、模型无关的应用层通信协议，旨在统一不同客户端调用工具的接口。

### 核心内容

- MCP的基本概念、痛点和架构
- 如何创建MCP服务器
- 服务器与客户端的交互流程
- 客户端如何与LLM交互 
     - 模型需要使用了上述输入输出的文本的训练集做微调 
     - 核心文件：
       - [[FunctionalCalling]] - 函数调用的基本概念和OpenAI框架下的实现
       - [[自动创建ApiSchema]] - 自动为函数生成API Schema的方法
       - [[FunctionCalling_Code.py]] - FunctionalCalling文件中的纯代码
       - [[IterativeFunctionCalling.py]] - 将[[FunctionCalling_Code]]中只有两轮对话的具体案例扩展成可以循环对话
### 客户端-tools
   - **方式1：自定义函数解析指令** 
   - **方式2：[[MCP]]**  
     - 为解决以下痛点，将编写api schema和调用工具的函数（当然也包括调用在线工具的函数，通讯代码都是在函数中实现的）封装成MCP server，然后由MCP cilent统一调用，这个过程遵循MCP。
      - 统一不同客户端调用工具的接口
      - 简化工具函数代码在不同使用者的agent代码中的重复过程
      - 简化工作流平台上api schema的配置和维护

     - 标准定义（ChatGPT）：MCP（Model Context Protocol） 是一种统一协议，用于将不同模型平台和工具调用封装为标准化的 MCP Server，使得 Agent 无需关心具体模型或工具的通信格式，只需通过 MCP Client 进行统一访问，极大简化了 Tool/API 的集成与调度过程。

     - 核心文档：
      - [[MCP]] - MCP的基本概念、痛点和流程，并说明了分成下面三个部分仔细介绍：
        - [[MCP_Server的创建]] - 创建一个最简的MCP服务器，代码和在cline中的配置文件如下：
          - [[test/MCPServer_test.py]] - MCP服务器测试代码
          - [[test/mcp.json]] - MCP配置文件
        - [[MCP_Server与客户端（MCP_Client）的交互]] - 服务器与客户端的交互流程
        - [[客户端（MCP_Client）与大模型的交互]] - 客户端如何与LLM交互
            - [[Cline客户端的system_prompt]] - Cline客户端使用的系统提示词
      - [[test/minimaxMCP.html]] - minimax MCP 生成三体介绍网页的示例

## 学习路径建议

1. **入门级**：首先了解Agent概念，这是LLM应用的核心框架
2. **进阶**：学习Function Calling基础，理解LLM如何调用外部函数
3. **高级**：深入MCP协议，理解跨模型、跨客户端的工具调用架构

## 常见应用场景

1. **信息检索增强**：使用Function Calling调用搜索API
2. **智能助手开发**：基于Agent架构构建具有工具使用能力的智能助手
3. **跨平台工具集成**：使用MCP协议实现一次开发、多平台复用的工具

## 相关资源

- [OpenAI Function Calling官方文档](https://platform.openai.com/docs/guides/function-calling)
- [LangChain Agent框架](https://python.langchain.com/docs/modules/agents/)
- [Model Context Protocol官方规范](https://github.com/modelcontextprotocol/spec)

