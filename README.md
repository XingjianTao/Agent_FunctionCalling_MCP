# Agent、Function Calling和MCP知识库总览

这个知识库包含关于大语言模型(LLM)领域中Agent、Function Calling和MCP三个核心技术的详细笔记和代码实现。

## 项目结构

```
.
├── README.md                       # 项目概述
├── Agent/                          # Agent相关知识和实现
│   ├── Agent.ipynb                 # Agent交互式笔记本
│   ├── Agent.md                    # Agent概念和实现文档
│   ├── Prompt.md                   # Prompt工程指南
│   └── ReAct.md                    # ReAct模式文档
├── FunctionCalling/                # Function Calling相关知识和实现
│   ├── FunctionCalling.ipynb       # Function Calling交互式笔记本
│   ├── FunctionCalling.md          # Function Calling概念和实现文档
│   ├── FunctionCalling_Code.py     # Function Calling代码实现
│   ├── IterativeFunctionCalling.py # 迭代式Function Calling实现
│   ├── 自动创建ApiSchema.md        # API Schema自动生成指南 
│   └── attachments/                # 图片附件目录
│       ├── Function_Calling.png    # Function Calling流程图
│       └── Function_Calling_Function.png  # 函数调用示例图
└── MCP/                            # MCP相关知识和实现
    ├── MCP.ipynb                   # MCP交互式笔记本
    ├── MCP.md                      # MCP概念和架构文档
    ├── MCP_Server的创建.ipynb      # MCP服务器创建笔记本
    ├── MCP_Server的创建.md         # MCP服务器创建指南
    ├── MCP_Server与客户端（MCP_Client）的交互.ipynb  # 服务器与客户端交互笔记本
    ├── MCP_Server与客户端（MCP_Client）的交互.md     # 服务器与客户端交互文档
    ├── 客户端（MCP_Client）与大模型的交互.ipynb     # 客户端与LLM交互笔记本
    ├── 客户端（MCP_Client）与大模型的交互.md        # 客户端与LLM交互文档
    ├── Cline客户端的system_prompt.md               # Cline客户端系统提示词
    ├── test/                                      # 测试代码目录
    │   ├── MCPServer_test.py                      # MCP服务器测试代码
    │   ├── mcp.json                               # MCP配置文件
    │   └── minimaxMCP.html                        # MiniMax MCP Web示例
    └── attachments/                               # 图片附件目录
        └── ...                                    # 各种流程图和截图
```

## **[[Agent]]**  
   - Agent 是封装了大语言模型 + Tools + Memory 等的调度框架，在代码中是一个类。
### 核心文档
- [[Agent]] - Agent的概念、构建流程和示例实现
- [[Prompt]] - Prompt的概念、分类、学习资源
- [[ReAct]] - ReAct提示词模版

## **工具调用**  
### 概述
日常使用大模型的工具调用功能通常通过客户端，客户端是大模型和本地工具之间的桥梁。
- **客户端-大模型**：客户端可以告诉大模型工具内容以及调教大模型具有工具调用功能，这一过程可以用System [[Prompt]]实现，后来为了规范化，开发出来[[FunctionCalling]]的技术。
- **客户端-tools**：客户端可以解析大模型发送的调用工具的指令，让本地或者在线工具执行，这一过程没有统一的规范，是MCP协议打包了这一过程并规范化。
### 客户端-大模型
   - **方式1：System [[Prompt]]驱动**  
     - 使用提示词模板如[[ReAct]]，内容包含：可用工具列表、迭代式调用步骤说明  
   - **方式2：[[FunctionCalling]]**  
     - 核心过程：模型（经过训练的）接受结构化的json格式的函数声明（api schema），生成结构化的json格式的函数调用指令 
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
 
