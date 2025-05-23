import json
from openai import OpenAI

# 创建 OpenAI 客户端（使用 DeepSeek API）
client = OpenAI(
    base_url="https://api.deepseek.com/v1",
    api_key="sk-2310dcae0744404eb0bbcbd2df4c6759"  # 请替换为你自己的 DeepSeek API Key
)

# 定义两个工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的当前天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如北京、上海等"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行基本的数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "计算操作，如 add（加法）、subtract（减法）、multiply（乘法）、divide（除法）",
                        "enum": ["add", "subtract", "multiply", "divide"]
                    },
                    "a": {
                        "type": "number",
                        "description": "第一个数字"
                    },
                    "b": {
                        "type": "number",
                        "description": "第二个数字"
                    }
                },
                "required": ["operation", "a", "b"]
            }
        }
    }
]

# 工具实现
def get_weather(city):
    """模拟天气 API"""
    weather_data = {
        "北京": {"temperature": 26, "weather": "晴朗", "humidity": 40},
        "上海": {"temperature": 28, "weather": "多云", "humidity": 65},
        "广州": {"temperature": 30, "weather": "阵雨", "humidity": 80},
        "深圳": {"temperature": 29, "weather": "晴朗", "humidity": 70}
    }
    
    # 返回查询城市的天气，如果城市不存在则返回默认值
    return weather_data.get(city, {"temperature": 25, "weather": "未知", "humidity": 50})

def calculate(operation, a, b):
    """执行数学计算"""
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else "除数不能为零"
    }
    
    if operation in operations:
        result = operations[operation](a, b)
        return {"result": result}
    else:
        return {"error": "不支持的操作"}

# 主要的对话处理函数
def handle_conversation(user_input):
    """处理用户输入，支持多轮函数调用"""
    messages = [{"role": "user", "content": user_input}]
    
    # 开始对话循环
    while True:
        # 发送请求给模型
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        # 获取模型回复
        assistant_message = response.choices[0].message
        
        # 将助手回复添加到消息历史
        messages.append(assistant_message.model_dump())
        
        # 检查是否有工具调用
        if not assistant_message.tool_calls:
            # 没有工具调用，直接返回模型回复
            return assistant_message.content
        
        # 处理所有工具调用
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # 执行相应的工具
            if function_name == "get_weather":
                function_response = get_weather(**function_args)
            elif function_name == "calculate":
                function_response = calculate(**function_args)
            else:
                function_response = {"error": "未知工具"}
            
            # 将工具执行结果添加到消息历史
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": json.dumps(function_response)
            })
            
            print(f"执行工具: {function_name}{function_args}")
            print(f"工具返回: {function_response}")
        
        # 如果进行了工具调用，继续循环让模型处理工具返回结果
        # 如果模型决定已经解决了用户问题，将不再调用工具，而是返回最终回答

# 测试示例
if __name__ == "__main__":
    # 测试自动解析和连续工具调用的能力
    queries = [
        "北京今天的天气怎么样？",
        "北京的温度是多少？",
        "北京的温度+10是多少度？",
        "广州的温度是深圳的温度的几倍？",
        "帮我计算 (北京温度 + 上海温度) ÷ 2"
    ]
    
    for query in queries:
        print("\n" + "=" * 60)
        print(f"用户问题: {query}")
        answer = handle_conversation(query)
        print(f"最终回答: {answer}")
        print("=" * 60)
