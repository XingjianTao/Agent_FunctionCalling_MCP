#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Function Calling 演示

本脚本演示了如何使用 OpenAI 风格的 Function Calling 功能，通过大语言模型进行多轮迭代对话，
完成一个需要多个工具调用的复合查询："北京的温度加10是多少度？"

执行流程：
1. 定义两个函数工具：get_weather 和 calculate_sum
2. 构建工具的 schema 描述，让大语言模型知道如何调用它们
3. 第一轮对话：用户询问北京温度+10的问题
   - 模型分析需要先获取北京温度，调用 get_weather 函数
4. 第二轮对话：将天气数据反馈给模型
   - 模型获取温度值后，决定进行加法计算，调用 calculate_sum 函数
5. 第三轮对话：模型生成最终答案
   - 根据前两轮的函数调用结果，生成人类可读的回答

本示例展示了 Function Calling 的核心优势：
- 自动决策调用顺序：模型自主决定先查询天气再计算
- 数据传递：从第一个函数获取温度，传递给第二个函数
- 上下文保持：多轮对话中保持查询目标和中间结果
- 自然语言接口：用户只需提出自然语言问题，无需了解函数细节

"""

import json
from openai import OpenAI

# 清理变量空间
# for name in dir():
#     if not name.startswith('_'):
#         del globals()[name]

# ================================================================
# Step 0: 定义工具 schema
# ================================================================
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
    """获取城市天气，这里简化为固定返回晴天"""
    # Regardless of the input city, always return sunny weather.
    return {
        "weather": "Sunny",
        "description": "Clear sky",
        "temperature": 26
    }

def calculate_sum(a, b):
    """计算两个数的和"""
    return {"result": a + b}

# ================================================================
# Step 1 & 2: 配置客户端并发送初始请求
# ================================================================
def run_function_calling_demo():
    """运行完整的Function Calling演示"""
    # 创建 DeepSeek 客户端
    client = OpenAI(
        base_url="https://api.deepseek.com/v1",
        api_key="sk-2310dcae0744404eb0bbcbd2df4c6759"  # 请替换为你自己的 DeepSeek API Key
    )
    
    print("=" * 50)
    print("📝 演示：北京的温度加10是多少度？")
    print("=" * 50)
    
    # 初始化消息历史
    messages = [{"role": "user", "content": "北京的温度加10是多少度？"}]
    
    # ================================================================
    # Step 3: 第一轮对话 - 请求天气信息
    # ================================================================
    print("\n" + "=" * 50)
    print("🔄 第一轮对话：用户询问北京温度+10")
    print("=" * 50)
    
    # 发送消息并获取响应
    response_1 = client.chat.completions.create(
        model="deepseek-chat",  # DeepSeek 模型名
        messages=messages,
        tools=tools,
        tool_choice="auto"  # 自动决定是否使用工具
    )
    
    # 解析第一轮响应
    assistant_message_1 = response_1.choices[0].message
    print("\n🤖 模型第一次回应：")
    print("完整消息对象:", assistant_message_1)
    print(f"内容: {assistant_message_1.content}")
    print(f"是否调用工具: {assistant_message_1.tool_calls is not None}")
    if assistant_message_1.tool_calls:
        print("工具调用:", json.loads(assistant_message_1.tool_calls[0].function.arguments))
    
    # 处理第一轮工具调用
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
        return
    
    # ================================================================
    # Step 4: 第二轮对话 - 计算温度+10
    # ================================================================
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
    
    # 处理第二轮工具调用
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
        return
    
    # ================================================================
    # Step 5: 第三轮对话 - 生成最终答案
    # ================================================================
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

if __name__ == "__main__":
    run_function_calling_demo()
