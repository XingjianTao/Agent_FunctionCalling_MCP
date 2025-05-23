# MCP_Server的创建：Python小白友好版本

本文档将详细讲解MCP_Server的Python实现。
参考实现：
https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#quickstart

## MCP服务器实现

### 1. 导入必要模块


```python
from mcp.server.fastmcp import FastMCP
import logging
```

- `FastMCP`：MCP的高级服务器实现，简化了创建MCP服务器的过程
- `logging`：Python的标准日志模块，用于记录程序运行时的信息

### 2. 配置日志


```python
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
```

这段代码配置了日志输出：
- `logging.basicConfig`：配置日志的基本设置
  - `level=logging.INFO`：设置日志级别为INFO，只记录INFO级别及以上的日志
  - `format='...'`：设置日志格式，包括时间、名称、级别和消息
- `logger = logging.getLogger(__name__)`：创建一个与当前模块同名的日志记录器

这样设置后，程序会在控制台输出格式化的日志信息，帮助开发者追踪程序的执行过程。

### 3. 创建MCP服务器实例


```python
mcp = FastMCP(
    name="WeatherCalculator",
    description="提供天气查询和简单计算功能的MCP服务器"
)
```

- `FastMCP`：创建一个MCP服务器实例
  - `name`：服务器名称，这里设为WeatherCalculator

  - `description`：服务器描述，简单说明服务器提供的功能

### 4. 添加工具函数

#### 4.1 天气查询工具


```python
@mcp.tool(description="获取指定城市的天气信息")
def get_weather(city: str) -> dict:
    """获取城市天气信息
    
    Args:
        city: 城市名称
        
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
```

- `@mcp.tool`：装饰器，将普通函数注册为MCP工具
  - `description`：工具描述，说明工具的功能
- `get_weather`：工具函数，接收城市名称参数，返回天气信息
  - 函数文档字符串详细说明了参数和返回值
  - `logger.info`：记录函数调用信息，包括参数值
  - `weather_data`：预定义的天气数据字典（示例数据）
  - `weather_data.get(city, {...})`：获取对应城市的天气，如不存在则返回默认数据

#### 4.2 计算工具


```python
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
```

- `@mcp.tool`：同样使用装饰器注册工具
- `calculate_sum`：计算两个数字之和的函数
  - 接收两个浮点数参数，返回包含计算结果的字典
  - 返回的字典不仅包含结果，还包含输入值和操作类型

### 5. 程序入口


```python
if __name__ == "__main__":
    print("MCP服务器以stdio模式启动...")
    mcp.run(transport="stdio")
```

程序入口部分采用了最简化的实现：
- `if __name__ == "__main__":`：当脚本直接运行时执行的代码块
- `mcp.run(transport="stdio")`：使用标准输入/输出（stdio）模式启动MCP服务器
  - 这是最基本的运行模式，通过标准输入/输出流与客户端通信
  - 适合与其他程序进行管道通信或作为子进程运行

### 6. 在Cline中配置调用MCPServer
##### MCP配置文件


```python
# MCP配置文件
{
    "mcpServers": {
        "weather_calculator": {
            "command": "/opt/anaconda3/envs/aiagent/bin/python",
            "args": [
                "/Users/taoxingjian/Desktop/Knowledge/Large_Language_Model/MCP/MCPServer_test.py"
            ]
        }
    }
}
```

#### 交互测试

![[与Cline进行交互测试.png|500]]
与Cline进行交互测试

#### 导出交互记录
![[Cline导出交互记录.png|500]]
Cline导出交互记录


## **User:**

<task>
请您用weather_calculator查询计算北京的温度+10是多少
</task>
<environment_details>
### VSCode Visible Files
../Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json

### VSCode Open Tabs
../Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json

### Current Time
2025/5/19 下午10:50:01 (Asia/Shanghai, UTC+8:00)

### Current Working Directory (/Users/taoxingjian/Desktop) Files
(Desktop files not shown automatically. Use list_files to explore if needed.)

### Context Window Usage
0 / 64K tokens used (0%)

### Current Mode
ACT MODE
</environment_details>

---

## **Assistant:**

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

## **User:**

[use_mcp_tool for 'weather_calculator'] Result:
{
  "weather": "Sunny",
  "description": "晴朗",
  "temperature": 26
}
<environment_details>
### VSCode Visible Files
../Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json

### VSCode Open Tabs
../Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json

### Current Time
2025/5/19 下午10:50:20 (Asia/Shanghai, UTC+8:00)

### Context Window Usage
18,586 / 64K tokens used (29%)

### Current Mode
ACT MODE
</environment_details>

---

## **Assistant:**

<thinking>
1. 已成功获取北京当前温度为26度
2. 现在需要使用calculate_sum工具计算26 + 10
3. 所有必要参数都已明确（a=26, b=10）
</thinking>

<use_mcp_tool>
<server_name>weather_calculator</server_name>
<tool_name>calculate_sum</tool_name>
<arguments>
{
  "a": 26,
  "b": 10
}
</arguments>
</use_mcp_tool>

---

## **User:**

[TASK RESUMPTION] This task was interrupted 2 minutes ago. It may or may not be complete, so please reassess the task context. Be aware that the project state may have changed since then. The current working directory is now '/Users/taoxingjian/Desktop/Knowledge/Large_Language_Model'. If the task has not been completed, retry the last step before interruption and proceed with completing the task.

Note: If you previously attempted a tool use that the user did not provide a result for, you should assume the tool use was not successful and assess whether you should retry. If the last tool was a browser_action, the browser has been closed and you must launch a new browser if needed.
<environment_details>
### VSCode Visible Files
MCP/MCPServer的最简实现.ipynb

### VSCode Open Tabs
MCP/MCPServer的最简实现.ipynb
MCP/image.png
MCP/mcp.json

### Current Time
2025/5/19 下午10:53:02 (Asia/Shanghai, UTC+8:00)

### Current Working Directory (/Users/taoxingjian/Desktop/Knowledge/Large_Language_Model) Files
.DS_Store
Agent.ipynb
Agent.md
CompleteCode.py
Function calling VS MCP.ipynb
Function calling VS MCP.md
Function_Calling_Function.png
Function_Calling.png
FunctionalCalling.ipynb
FunctionalCalling.md
FunctionCalling_Code.py
index.html
IterativeFunctionCalling.py
MCP_STANDARD_GUIDE.md
mcp.json
MCPClient_new.py
MCPServer_new.py
Outline.md
Prompt.md
React.md
MCP/
MCP/FunctionalCalling.ipynb
MCP/FunctionCalling_Code.py
MCP/image.png
MCP/MCP_Client_stdio.py
MCP/MCP_README.md
MCP/mcp_standard.json
MCP/mcp.json
MCP/MCP实现详解.md
MCP/MCP通信方式总结.md
MCP/MCPServer_test.py
MCP/MCPServer的最简实现.ipynb
MCP/setup.py
MCP/mcp_server_time/
MCP/mcp_server_time/__init__.py
MCP/mcp_server_time/__main__.py
MCP/mcp_server_time/server.py
MCP/mcp_weather_calculator/
MCP/mcp_weather_calculator/__init__.py
MCP/mcp_weather_calculator/__main__.py
MCP/mcp_weather_calculator/server.py
MCP/time/
MCP/time/.DS_Store
MCP/time/.python-version
MCP/time/Dockerfile
MCP/time/pyproject.toml
MCP/time/README.md
MCP/time/uv.lock
MCP/time/src/
MCP/time/src/.DS_Store
MCP/time/src/mcp_server_time/
MCP/time/src/mcp_server_time/__init__.py
MCP/time/src/mcp_server_time/__main__.py
MCP/time/src/mcp_server_time/server.py
MCP/time/test/
MCP/time/test/time_server_test.py

### Context Window Usage
18,870 / 64K tokens used (29%)

### Current Mode
ACT MODE
</environment_details>

---

## **Assistant:**

<thinking>
1. 任务中断前已完成获取北京温度(26度)的步骤
2. 中断前正在执行计算26+10的操作
3. 需要重新执行calculate_sum工具计算26+10
4. 所有必要参数仍然有效(a=26, b=10)
5. 当前工作目录变化不影响此计算任务
</thinking>

<use_mcp_tool>
<server_name>weather_calculator</server_name>
<tool_name>calculate_sum</tool_name>
<arguments>
{
  "a": 26,
  "b": 10
}
</arguments>
</use_mcp_tool>

---

## **User:**

[use_mcp_tool for 'weather_calculator'] Result:
{
  "result": 36.0,
  "input_a": 26.0,
  "input_b": 10.0,
  "operation": "addition"
}
<environment_details>
### VSCode Visible Files
MCP/MCPServer的最简实现.ipynb

### VSCode Open Tabs
MCP/MCPServer的最简实现.ipynb
MCP/image.png
MCP/mcp.json

### Current Time
2025/5/19 下午10:53:22 (Asia/Shanghai, UTC+8:00)

### Context Window Usage
19,844 / 64K tokens used (31%)

### Current Mode
ACT MODE
</environment_details>

---

## **Assistant:**

<attempt_completion>
<result>
北京当前天气晴朗，温度为26度。26度加10等于36度。
</result>
</attempt_completion>
