# MCP_Server与MCP_Client的交互
参考教程：https://www.bilibili.com/video/BV1Y854zmEg9?spm_id_from=333.788.recommend_more_video.-1&vd_source=ba16f478e6d7f23888c37746ea6756de 

## 引言

上述教程通过中介程序调用MCP_Server，可以获取交互记录。
![[交互记录日志.png|500]]
交互记录日志
为了简单起见，我们不采用自己跑一遍教程的方式，而是直接记录教程信息，解读交互过程。

## 解读交互日志

### 1. 客户端初始化请求（客户端 → 服务器）

第一步是客户端发送初始化请求，建立与服务器的连接。


```python
# 客户端初始化请求
{
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {
            "name": "Cline",
            "version": "3.12.3"
        }
    },
    "jsonrpc": "2.0",
    "id": 0
}
```

**解析：**
- `method: "initialize"` - 表示这是一个初始化请求
- `protocolVersion: "2024-11-05"` - 客户端使用的MCP协议版本
- `capabilities: {}` - 客户端的能力（此处为空，表示使用默认能力）
- `clientInfo` - 客户端信息，包含名称（Cline）和版本（3.12.3）
- `jsonrpc: "2.0"` - 使用的JSON-RPC协议版本
- `id: 0` - 请求ID，用于匹配响应

### 2. 服务器初始化响应（服务器 → 客户端）


```python
# 服务器初始化响应
{
    "jsonrpc": "2.0",
    "id": 0,
    "result": {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "experimental": {},
            "prompts": {
                "listChanged": false
            },
            "resources": {
                "subscribe": false,
                "listChanged": false
            },
            "tools": {
                "listChanged": false
            }
        },
        "serverInfo": {
            "name": "weather",
            "version": "1.6.0"
        }
    }
}
```

**解析：**
- `id: 0` - 与请求ID匹配，表明这是对初始化请求的响应
- `result` - 包含服务器的响应结果
  - `protocolVersion: "2024-11-05"` - 服务器支持的协议版本
  - `capabilities` - 服务器支持的各种能力：
    - `experimental` - 实验性功能（空）
    - `prompts.listChanged: false` - 提示列表是否支持实时变更
    - `resources.subscribe: false` - 是否支持资源订阅
    - `resources.listChanged: false` - 资源列表是否支持实时变更  
    - `tools.listChanged: false` - 工具列表是否支持实时变更
  - `serverInfo` - 服务器信息
    - `name: "weather"` - 服务器名称，表示这是一个天气服务
    - `version: "1.6.0"` - 服务器版本

### 3. 客户端发送初始化完成通知（客户端 → 服务器）

客户端通知服务器初始化已完成。


```python
# 客户端发送初始化完成通知
{
    "method": "notifications/initialized",
    "jsonrpc": "2.0"
}
```

**解析：**
- `method: "notifications/initialized"` - 表示这是一个通知服务器初始化已完成的消息
- 注意这个请求没有`id`字段，表明这是一个通知（notification），不需要服务器响应

### 4. 客户端请求工具列表（客户端 → 服务器）

客户端请求获取服务器提供的工具列表。


```python
# 客户端请求工具列表
{
    "method": "tools/list",
    "jsonrpc": "2.0",
    "id": 1
}
```

**解析：**
- `method: "tools/list"` - 请求获取服务器支持的工具列表
- `id: 1` - 请求ID，用于匹配响应

### 5. 服务器返回工具列表（服务器 → 客户端）


```python
# 服务器返回工具列表
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "tools": [
            {
                "name": "get_alerts",
                "description": "Get weather alerts for a US state.

Args:
    state: Two-letter US state code (e.g. CA, NY)
",
                "inputSchema": {
                    "properties": {
                        "state": {
                            "title": "State",
                            "type": "string"
                        }
                    },
                    "required": ["state"],
                    "title": "get_alertsArguments",
                    "type": "object"
                }
            },
            {
                "name": "get_forecast",
                "description": "Get weather forecast for a location.

Args:
    latitude: Latitude of the location
    longitude: Longitude of the location
",
                "inputSchema": {
                    "properties": {
                        "latitude": {
                            "title": "Latitude",
                            "type": "number"
                        },
                        "longitude": {
                            "title": "Longitude",
                            "type": "number"
                        }
                    },
                    "required": ["latitude", "longitude"],
                    "title": "get_forecastArguments",
                    "type": "object"
                }
            }
        ]
    }
}
```

**解析：**
- `id: 1` - 与请求ID匹配，表明这是对工具列表请求的响应
- `result.tools` - 包含服务器提供的两个工具：
  
  1. **get_alerts工具**
     - `name: "get_alerts"` - 工具名称
     - `description` - 工具描述：获取美国州的天气警报
     - `inputSchema` - 输入参数结构：
       - 需要一个`state`参数，类型为字符串，表示美国州的两字母代码（如CA, NY）
  
  2. **get_forecast工具**
     - `name: "get_forecast"` - 工具名称
     - `description` - 工具描述：获取特定位置的天气预报
     - `inputSchema` - 输入参数结构：
       - 需要`latitude`（纬度）和`longitude`（经度）两个数值参数，表示地理位置

**注意：**
1. description来自于代码编写时的特殊注释：docstring

![[docstring.png|500]]
docstring

2. inputSchema遵守的是一个叫JSON Schema的规范

JSON Schema是本身也是一段JSON，用于描述另一段JSON的结构：
![[JSON_Schema.png|500]]
JSON Schema


比如上图中的JSON Schema，要求JSON中必须有两个参数（`latitude`和`longitude`），然后两个参数的属性都是number。


3. InputSchema是根据注册为mcp tools的参数定义实现的：
![[InputSchema.png|500]]
InputSchema

### 6. 客户端请求资源列表（客户端 → 服务器）

客户端请求获取服务器提供的资源列表。


```python
# 客户端请求资源列表
{
    "method": "resources/list",
    "jsonrpc": "2.0",
    "id": 2
}
```

**解析：**
- `method: "resources/list"` - 请求获取服务器支持的资源列表
- `id: 2` - 请求ID，用于匹配响应

### 7. 服务器返回资源列表


```python
# 服务器返回资源列表
{
    "jsonrpc": "2.0",
    "id": 2,
    "result": {
        "resources": []
    }
}
```

**解析：**
- `id: 2` - 与请求ID匹配，表明这是对资源列表请求的响应
- `result.resources: []` - 空数组，表示服务器没有提供任何资源

### 8. 资源模板列表请求

客户端请求获取服务器提供的资源模板列表。


```python
# 客户端请求资源模板列表
{
    "method": "resources/templates/list",
    "jsonrpc": "2.0",
    "id": 3
}
```

**解析：**
- `method: "resources/templates/list"` - 请求获取服务器支持的资源模板列表
- `id: 3` - 请求ID，用于匹配响应

### 9. 服务器返回资源模板列表


```python
# 服务器返回资源模板列表
{
    "jsonrpc": "2.0",
    "id": 3,
    "result": {
        "resourceTemplates": []
    }
}
```

**解析：**
- `id: 3` - 与请求ID匹配，表明这是对资源模板列表请求的响应
- `result.resourceTemplates: []` - 空数组，表示服务器没有提供任何资源模板

### 10. 客户端发送调用工具请求（客户端 → 服务器）

客户端请求调用服务器提供的`get_forecast`工具来获取天气预报。


```python
# 客户端请求调用get_forecast工具
{
    "method": "tools/call",
    "params": {
        "name": "get_forecast",
        "arguments": {
            "latitude": 40.7128,
            "longitude": -74.006
        }
    },
    "jsonrpc": "2.0",
    "id": 4
}
```

**解析：**
- `method: "tools/call"` - 表示这是一个调用工具的请求
- `params` - 调用参数：
  - `name: "get_forecast"` - 要调用的工具名称
  - `arguments` - 传递给工具的参数：
    - `latitude: 40.7128` - 纬度值（40.7128是纽约市的纬度）
    - `longitude: -74.006` - 经度值（-74.006是纽约市的经度）
- `id: 4` - 请求ID，用于匹配响应

### 11. 服务器返回工具调用结果（服务器 → 客户端）


```python
# 服务器返回天气预报结果
{
    "jsonrpc": "2.0",
    "id": 4,
    "result": 
    {
        "content": 
        [
            {
                "type": "text",
                "text": "
                            Today:
                            Temperature: 64°F
                            Wind: 2 to 18 mph S
                            Forecast: Mostly sunny. High near 64, with temperatures falling to around 62 in the afternoon. South wind 2 to 18 mph, with gusts as high as 30 mph.

                            ---

                            Tonight:
                            Temperature: 57°F
                            Wind: 12 to 17 mph S
                            Forecast: Mostly cloudy. Low around 57, with temperatures rising to around 59 overnight. South wind 12 to 17 mph, with gusts as high as 29 mph.

                            ---

                            Saturday:
                            Temperature: 78°F
                            Wind: 12 to 21 mph SW
                            Forecast: Partly sunny, with a high near 78. Southwest wind 12 to 21 mph, with gusts as high as 32 mph.

                            ---

                            Saturday Night:
                            Temperature: 57°F
                            Wind: 15 to 18 mph W
                            Forecast: A chance of rain showers between 8pm and 2am. Mostly cloudy. Low around 57, with temperatures rising to around 61 overnight. West wind 15 to 18 mph. Chance of precipitation is 30%.

                            ---

                            Sunday:
                            Temperature: 62°F
                            Wind: 14 to 17 mph NW
                            Forecast: Partly sunny, with a high near 62. Northwest wind 14 to 17 mph.
                        "
            }
        ],
        "isError": false
    }
}
```

**解析：**
- `id: 4` - 与请求ID匹配，表明这是对调用get_forecast工具请求的响应
- `result` - 包含工具执行的结果：
  - `content` - 内容数组，包含结果项：
    - `type: "text"` - 内容类型为文本
    - `text` - 包含了详细的天气预报信息，分为多个时段（今天、今晚、周六、周六晚上、周日）
      - 每个时段包含温度、风况和天气预报的详细描述
  - `isError: false` - 表示工具执行成功，没有发生错误

### MCP通信总结

通过分析以上MCP客户端与服务器间的通信日志，我们可以总结出MCP协议的基本工作流程：

1. **初始化阶段**：
   - 客户端发送初始化请求，提供协议版本和客户端信息
   - 服务器响应，提供自身支持的能力和服务器信息
   - 客户端发送初始化完成通知

2. **发现阶段**：
   - 客户端请求服务器提供的工具列表
   - 客户端请求服务器提供的资源列表
   - 客户端请求服务器提供的资源模板列表

3. **调用阶段**：
   - 客户端调用服务器提供的工具（本例中是获取纽约市的天气预报）
   - 服务器执行工具功能并返回结果

MCP协议使用JSON-RPC 2.0作为底层通信协议，每个请求都有一个与之对应的响应（除了通知类型的消息）。这种设计使得客户端与服务器之间的通信简单明了且易于理解。在本例中，服务器提供了两个天气相关的工具，但没有提供任何资源或资源模板。

| 步骤  | 目的             | 方法名                         | 备注                    |
| --- | -------------- | --------------------------- | --------------------- |
| ①-② | 建立会话 / 协商版本、能力 | `initialize`                | JSON-RPC 请求-响应        |
| ③   | 完成初始化通知        | `notifications/initialized` | 无 id，单向通知             |
| ④-⑤ | 获取可用工具清单       | `tools/list`                | 返回每个工具的 `inputSchema` |
| ⑥-⑨ | （可选）探查资源与模板    | `resources/*`               | 此例均为空                 |
| ⑩-⑪ | 真实业务调用         | `tools/call`                | 为指定经纬度取天气预报           |


## 直接与MCP Server交流

1. **初始化阶段**：
我们修改了我们的名字（Cline->txj），客户端返回了我们的服务器名称。

`{"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"txj","version":"0.0.1"}},"jsonrpc":"2.0","id":0}`
`{"method":"notifications/initialized","jsonrpc":"2.0"}`

![[DirectTalkWithMCPServer1.png|500]]
DirectTalkWithMCPServer1

2. **发现阶段**：
`{"method":"resources/list","jsonrpc":"2.0","id":2}`
`{"method":"resources/templates/list","jsonrpc":"2.0","id":3}`
![[DirectTalkWithMCPServer2.png|500]]
DirectTalkWithMCPServer2

3. **调用阶段**：
我们成功调用我们自己编的MCP Server获取了北京的天气。
`{"method":"tools/call","params":{"name":"get_weather","arguments":{"city":"北京"}},"jsonrpc":"2.0","id":4}`

![[DirectTalkWithMCPServer3.png|500]]
DirectTalkWithMCPServer3
