# Agent

# 目录

- [什么是Agent](#什么是agent)
- [测试api（案例来自OpenAI API平台）](#测试api案例来自openai-api平台)
    - 配置 OpenAI API 客户端
- [创建一个 AI Agent](#创建一个-ai-agent)
    - [创建 llm](#创建-llm)
    - [创建本地 tools，编写 API schema](#创建本地-tools编写-api-schema)
    - [通过提示词实现工具调用流程](#通过提示词实现工具调用流程)
    - [构建执行器并执行](#构建执行器并执行)
- [在上述 agent 的基础上增加记忆](#在上述-agent-的基础上增加记忆)


## 什么是Agent
**“Agent 是封装了大语言模型 + Tools + Memory 的结构”**

✔️ 对的，Agent 并不是语言模型本身，而是一个**调度框架**，让语言模型能“用工具完成任务”。



**“在 Agent 内部，它可以按照 prompt 的逻辑链条，通过内部工具帮助大语言模型完成任务。”**

✔️ 非常到位。Agent 的核心就是：

* 指定一个结构化的 **Prompt**；
* 让 LLM 按照“思考 → 行动 → 观察 → 再思考”的 **链式推理方式**（如 ReAct）运行；
* 并在过程中调用工具、引用记忆、完成任务。



## 🧠 标准定义（简明回顾版）：

**Agent（智能体）是基于大语言模型（LLM）的执行架构，它结合了 Prompt、工具（Tools）、记忆（Memory）和控制逻辑，使得语言模型能够感知上下文、调用外部资源、完成复杂任务。**

换句话说：

> 🧠 LLM 是“大脑”，🛠 Tools 是“手”，🧾 Memory 是“记忆”，而 Agent 是“协调所有器官完成任务的意识”。

## 测试api（案例来自OpenAI API平台）
https://platform.openai.com/docs/quickstart?api-mode=responses 
由于我们使用的是中转api，并不支持最新的调用方法，所以案例和官网有所不同


```python
from openai import OpenAI

# 指向自定义服务商（示例：MCP Server）
client = OpenAI(
    base_url = "https://api.hopeai.cc/v1",  # 👈 关键修改点
    api_key = "sk-42bry6ZXNNkAvs91Kzm5aDWrmvc3f3mw1u2sRfCOlIuihf6J"  # 服务商提供的认证密钥
)
print(client.api_key)  # 检查是否正确设置了 API 密钥

completion = client.chat.completions.create( 
    model="gpt-4o-mini",
    store=True,
    messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
  
)

# 提取生成的消息内容
message = completion.choices[0].message.content
print("Generated Message:", message)

```

    sk-42bry6ZXNNkAvs91Kzm5aDWrmvc3f3mw1u2sRfCOlIuihf6J
    Generated Message: Lines of code and code,  
    Whispers of thought intertwined,  
    Dreams in silicon.


## 创建一个ai agent
采用gpt-4o-mini作为大语言模型，通过[系统提示词]调用自己创建的tool：get_current_time


```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain import hub
from langchain_openai import ChatOpenAI
```

### 创建llm


```python
# 使用 langchain 的 OpenAI 模块
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key="sk-42bry6ZXNNkAvs91Kzm5aDWrmvc3f3mw1u2sRfCOlIuihf6J",
    openai_api_base="https://api.hopeai.cc/v1"
)
# print(llm.invoke("你好，你是怎么工作的？"))
```

### 创建本地tools，编写api schema


```python
def get_current_time(input=None):  # 添加一个默认参数
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
## 下面这一段似乎就是所谓的api schema
time_tool = Tool(
    name="get_current_time",
    func=get_current_time,
    description="获取当前的日期和时间。"
)
```

### 通过提示词实现工具调用流程


```python
prompt = hub.pull("hwchase17/react")

# 查看提示模板的内容
print(prompt)
```

    /opt/anaconda3/envs/aiagent/lib/python3.12/site-packages/langsmith/client.py:272: LangSmithMissingAPIKeyWarning: API key must be provided when using hosted LangSmith API
      warnings.warn(


    input_variables=['agent_scratchpad', 'input', 'tool_names', 'tools'] input_types={} partial_variables={} metadata={'lc_hub_owner': 'hwchase17', 'lc_hub_repo': 'react', 'lc_hub_commit_hash': 'd15fe3c426f1c4b3f37c9198853e4a86e20c425ca7f4752ec0c9b0e97ca7ea4d'} template='Answer the following questions as best you can. You have access to the following tools:\n\n{tools}\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin!\n\nQuestion: {input}\nThought:{agent_scratchpad}'


### 构建执行器并执行


```python
agent = create_react_agent(llm=llm, tools=[time_tool], prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=[time_tool], verbose=True)
response = agent_executor.invoke({"input": "请告诉我现在的时间。"})
print(response["output"])
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m我需要获取当前的日期和时间来回答这个问题。  
    Action: get_current_time  
    Action Input: None  [0m[36;1m[1;3m2025-05-13 22:28:16[0m[32;1m[1;3m我现在知道了当前的日期和时间是2025年5月13日22点28分16秒。  
    Final Answer: 现在的时间是2025年5月13日22点28分16秒。[0m
    
    [1m> Finished chain.[0m
    现在的时间是2025年5月13日22点28分16秒。


## 在上述agent的基础上增加记忆


```python
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
```


```python
# 会话记忆：保留对话历史
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# === 构建 Agent 和执行器 ===
executor = initialize_agent(
    tools=[time_tool],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
)
# === 多轮对话 ===
while True:
    user_input = input("\n🧑 你说：")
    if user_input.lower() in ["exit", "quit", "再见", "bye"]:
        break
    response = executor.invoke({"input": user_input})
    print("\n🤖 智能体回答：", response["output"])

# === 对话案例 ===
# 1. 用户输入：请告诉我现在的时间。
# 2. 智能体回答：2023-10-01 12:34:56
# 3. 用户输入：你能告诉我今天的天气吗？
# 4. 智能体回答：抱歉，我无法提供天气信息，但我可以告诉你现在的时间。
# 5. 用户输入：再见
```

    
    
    [1m> Entering new AgentExecutor chain...[0m
    [32;1m[1;3m```
    Thought: Do I need to use a tool? No
    AI: Hello! How can I assist you today?
    ```[0m
    
    [1m> Finished chain.[0m
    
    🤖 智能体回答： Hello! How can I assist you today?
    ```

