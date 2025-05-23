# Function Calling
- 核心过程：模型（经过训练的）接受结构化的json格式的函数声明（api schema），生成结构化的json格式的函数调用指令 
- 模型需要使用了上述输入输出的文本的训练集做微调

本教程将通过在openai的框架下实现Function Calling，来解释下面流程图。
![[Function_Calling.png|500]]
Function_Calling

①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳

## Step0：函数创建与编写函数说明
**注意：函数说明即并不需要向下面这样手写，而是可以自动创建，参见[[自动创建ApiSchema]]**
![[Function_Calling_Function.png|200]]
Function_Calling_Function


```python
for name in dir():
    if not name.startswith('_'):
        del globals()[name]
# 定义工具 schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_sum",
            "description": "Add two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

def get_weather(city):
    # Regardless of the input city, always return sunny weather.
    return {
        "weather": "Sunny",
        "description": "Clear sky",
        "temperature": 26
    }

def calculate_sum(a, b):
    return {"result": a + b}
```

## Step1：微调大模型使得支持Function Calling
对应蓝色箭头红①

## Step2：初始化智能体中枢，配置llm并注册tools
对应红色箭头蓝①-②


```python
from openai import OpenAI
# 创建 DeepSeek 客户端
client = OpenAI(
    base_url="https://api.deepseek.com/v1",
    api_key="sk-2310dcae0744404eb0bbcbd2df4c6759"  # 请替换为你自己的 DeepSeek API Key
)
# 初始化消息历史
messages = [{"role": "user", "content": "北京的温度加10是多少度？"}]
# 发送消息并获取响应
response_1 = client.chat.completions.create(
    model="deepseek-chat",  # DeepSeek 模型名
    messages=messages,
    tools=tools,
    tool_choice="auto"  # 自动决定是否使用工具
)

```

## Step3：解析智能体中枢的输出并调用函数
### 第一轮对话
对应红色箭头蓝③-⑦

模型回复中content为空，但是tool_calls非空，其值表示调用get_weather工具，表现正常。


```python
import json
# 解析第一轮响应
assistant_message_1 = response_1.choices[0].message
print("\n🤖 模型第一次回应：")
print("完整消息对象:", assistant_message_1)
print(f"内容: {assistant_message_1.content}")
print(f"是否调用工具: {assistant_message_1.tool_calls is not None}")
if assistant_message_1.tool_calls:
    print("工具调用:", json.loads(assistant_message_1.tool_calls[0].function.arguments))
```

    
    🤖 模型第一次回应：
    完整消息对象: ChatCompletionMessage(content='', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_0_87a1a338-9f57-490a-946b-20cffc4edae6', function=Function(arguments='{"city": "北京"}', name='get_weather'), type='function', index=0)])
    内容: 
    是否调用工具: True
    工具调用: {'city': '北京'}



```python
# 如果模型调用了工具（应该是调用 get_weather）
if assistant_message_1.tool_calls:
    tool_call_1 = assistant_message_1.tool_calls[0]
    function_name_1 = tool_call_1.function.name
    arguments_1 = json.loads(tool_call_1.function.arguments)
    
    print(f"\n🔧 模型调用函数：{function_name_1}({arguments_1})")
    
    # 执行函数
    if function_name_1 == "get_weather":
        result_1 = get_weather(**arguments_1)
    elif function_name_1 == "calculate_sum":
        result_1 = calculate_sum(**arguments_1)
    else:
        result_1 = {"error": "Unknown function"}
        
    print(f"\n📊 函数执行结果：{result_1}")
    
    # 添加助手回复到消息历史（包含工具调用）
    messages.append({"role": "assistant", "tool_calls": assistant_message_1.tool_calls})
    
    # 添加工具响应到消息历史
    messages.append({
        "role": "tool", 
        "tool_call_id": tool_call_1.id, 
        "name": function_name_1, 
        "content": json.dumps(result_1)
    })
    
    # 打印当前消息历史，方便理解
    print("\n📝 当前消息历史:")
    for i, msg in enumerate(messages):
        print(f"  {i+1}. 角色: {msg['role']}, " + 
              (f"内容: {msg['content']}" if 'content' in msg else "工具调用"))
else:
    # 模型没有调用任何函数，直接给出答案
    print("\n🎉 模型没有调用工具，直接给出答案:", assistant_message_1.content)

```

    
    🔧 模型调用函数：get_weather({'city': '北京'})
    
    📊 函数执行结果：{'weather': 'Sunny', 'description': 'Clear sky', 'temperature': 26}
    
    📝 当前消息历史:
      1. 角色: user, 内容: 北京的温度加10是多少度？
      2. 角色: assistant, 工具调用
      3. 角色: tool, 内容: {"weather": "Sunny", "description": "Clear sky", "temperature": 26}


### 第二轮对话
对应红色箭头蓝⑧⑨-④⑤⑥⑦

注意第二轮返回给模型的对话messages是第一轮的对话历史！

模型回复中content为空，但是tool_calls非空，其值表示调用get_weather工具，表现正常。


```python
# 第二轮对话：将天气信息给回模型，让模型进行计算
print("\n" + "="*50)
print("🔄 第二轮对话：将天气信息反馈给模型")
print("="*50)

# 第二轮对话 - 让模型处理函数返回的温度信息
response_2 = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# 解析第二轮响应
assistant_message_2 = response_2.choices[0].message
print("\n🤖 模型第二次回应：")
print(f"内容: {assistant_message_2.content}")
print(f"是否调用工具: {assistant_message_2.tool_calls is not None}")

# 如果模型还调用了工具（应该是调用 calculate_sum）
if assistant_message_2.tool_calls:
    tool_call_2 = assistant_message_2.tool_calls[0]
    function_name_2 = tool_call_2.function.name
    arguments_2 = json.loads(tool_call_2.function.arguments)
    
    print(f"\n🔧 模型调用第二个函数：{function_name_2}({arguments_2})")
    
    # 执行第二个函数
    if function_name_2 == "get_weather":
        result_2 = get_weather(**arguments_2)
    elif function_name_2 == "calculate_sum":
        result_2 = calculate_sum(**arguments_2)
    else:
        result_2 = {"error": "Unknown function"}
        
    print(f"\n📊 第二个函数执行结果：{result_2}")
    
    # 添加第二个助手回复到消息历史
    messages.append(assistant_message_2.model_dump())
    
    # 添加第二个工具响应到消息历史
    messages.append({
        "role": "tool", 
        "tool_call_id": tool_call_2.id, 
        "name": function_name_2, 
        "content": json.dumps(result_2)
    })
    
    # 打印更新后的消息历史
    print("\n📝 更新后的消息历史:")
    for i, msg in enumerate(messages):
        print(f"  {i+1}. 角色: {msg['role']}, " + 
              (f"内容: {msg['content']}" if 'content' in msg else "工具调用"))
else:
    print("\n🎉 模型直接给出答案:", assistant_message_2.content)
```

    
    ==================================================
    🔄 第二轮对话：将天气信息反馈给模型
    ==================================================
    
    🤖 模型第二次回应：
    内容: 
    是否调用工具: True
    
    🔧 模型调用第二个函数：calculate_sum({'a': 26, 'b': 10})
    
    📊 第二个函数执行结果：{'result': 36}
    
    📝 更新后的消息历史:
      1. 角色: user, 内容: 北京的温度加10是多少度？
      2. 角色: assistant, 工具调用
      3. 角色: tool, 内容: {"weather": "Sunny", "description": "Clear sky", "temperature": 26}
      4. 角色: assistant, 内容: 
      5. 角色: tool, 内容: {"result": 36}


### 第三轮对话
对应红色箭头蓝⑦⑧⑨⑩历史！


```python
# 第三轮对话：生成最终答案
print("\n" + "="*50)
print("🎯 第三轮对话：生成最终答案")
print("="*50)

# 获取最终答案
final_response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)
print("\n🤖 模型最终回应：")
print(f"内容: {final_response.choices[0].message.content}")
print("\n" + "="*50)
print("🎉 完成！")
```

    
    ==================================================
    🎯 第三轮对话：生成最终答案
    ==================================================
    
    🤖 模型最终回应：
    内容: 北京当前的温度是26度，加上10度后是36度。
    
    ==================================================
    🎉 完成！

