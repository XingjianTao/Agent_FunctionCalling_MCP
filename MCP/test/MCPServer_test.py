#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MCP服务器实现

本脚本基于MCP标准实现了一个服务器，提供两个工具函数：
1. get_weather - 获取指定城市的天气
2. calculate_sum - 计算两个数字的和
"""

from mcp.server.fastmcp import FastMCP
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 创建MCP服务器实例
mcp = FastMCP(
    name="WeatherCalculator",
    description="提供天气查询和简单计算功能的MCP服务器"
)

# 添加获取天气工具
@mcp.tool(description="获取指定城市的天气信息")
def get_weather(city: str) -> dict:
    """获取城市天气信息
    
    Args:
        city: 城市名称，如"北京"、"上海"、"广州"等
        
    Returns:
        包含天气信息的字典，格式为 {"weather": str, "description": str, "temperature": int}
    """
    logger.info(f"调用get_weather函数，参数: {city}")
    # 这里简化实现，返回固定的天气信息
    # 实际应用中应该调用真实的天气API
    weather_data = {
        "北京": {"weather": "Sunny", "description": "晴朗", "temperature": 26},
        "上海": {"weather": "Cloudy", "description": "多云", "temperature": 24},
        "广州": {"weather": "Rainy", "description": "小雨", "temperature": 28}
    }
    
    # 如果城市不存在，返回默认数据
    return weather_data.get(city, {
        "weather": "Unknown",
        "description": f"无法获取{city}的天气",
        "temperature": 20
    })

# 添加计算和工具
@mcp.tool(description="计算两个数字的和并返回结果")
def calculate_sum(a: float, b: float) -> dict:
    """计算两个数的和
    
    Args:
        a: 第一个数字（可以是整数或浮点数）
        b: 第二个数字（可以是整数或浮点数）
        
    Returns:
        包含计算结果的字典，格式为 {"result": float, "input_a": float, "input_b": float}
    """
    logger.info(f"调用calculate_sum函数，参数: a={a}, b={b}")
    result = a + b
    return {
        "result": result,
        "input_a": a,
        "input_b": b,
        "operation": "addition"
    }



if __name__ == "__main__":
    print("MCP服务器以stdio模式启动...")
    mcp.run(transport="stdio")
