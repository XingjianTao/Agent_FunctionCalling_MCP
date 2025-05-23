下面先用几句话说明 **Pydantic + Function Calling** 的思路，然后给出一份把你脚本改写为“**零手写 JSON-Schema**”的完整示例代码。你可以直接运行对比体验。**下面的代码我们没有测试过**

---

## 为什么用 Pydantic？

| 传统手写 tools 列表            | Pydantic 自动生成                                  |
| ------------------------ | ---------------------------------------------- |
| ✅ 完全可控，但字段多时极易漏写 / 拼错    | ✅ 直接用 Python 类型标注，`BaseModel` 一键产出 JSON-Schema |
| ❌ 需要自己保持函数签名 ↔ Schema 一致 | ✅ `model_json_schema()` 保证两边同步                 |
| ❌ 缺少输入校验                 | ✅ Pydantic 自带强类型校验与默认值处理                       |

> OpenAI Agents SDK、Instructor、openai-function-call 等库都在内部调用 **Pydantic→JSON-Schema** 流程；你也可以自己 `model_json_schema()` 或 `function_schema()` 来做同样的事。([OpenAI][1], [OpenAI][2])

---

## 用「decorator + Pydantic」改写你的示例

下面演示 **两种常见做法**——任选其一即可：

### 方案 A：使用第三方装饰器 `openai_function_call.openai_function`

```python
# pip install openai-function-call pydantic openai

import json
import os
import openai
from openai_function_call import openai_function        # ⭐ 装饰器

openai.api_key = os.getenv("OPENAI_API_KEY")            # 或 DeepSeek 的 key
openai.base_url = "https://api.deepseek.com/v1"

# --------------------------------------------------
# 1. 直接在函数上加装饰器，Schema 自动挂到 .openai_schema
# --------------------------------------------------
@openai_function
def get_weather(city: str) -> dict:
    """获取城市天气（示例固定返回 26 °C 晴）"""
    return {"weather": "Sunny", "temperature": 26}

@openai_function
def calculate_sum(a: float, b: float) -> dict:
    """计算两个数字之和"""
    return {"result": a + b}

# 把 schema 列到 tools；全程无需手写 JSON
tools = [get_weather.openai_schema, calculate_sum.openai_schema]

# --------------------------------------------------
# 2. 与你原来脚本几乎一致的对话循环
# --------------------------------------------------
def ask_beijing_plus_10():
    messages = [{"role": "user", "content": "北京的温度加 10 是多少度？"}]

    # ① 第一次：模型要先拿北京温度
    resp1 = openai.ChatCompletion.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    call1 = resp1.choices[0].message.tool_calls[0]
    result1 = get_weather(**json.loads(call1.function.arguments))

    messages += [
        {"role": "assistant", "tool_calls": resp1.choices[0].message.tool_calls},
        {"role": "tool", "tool_call_id": call1.id, "name": call1.function.name,
         "content": json.dumps(result1)},
    ]

    # ② 第二次：模型要求做加法
    resp2 = openai.ChatCompletion.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    call2 = resp2.choices[0].message.tool_calls[0]
    result2 = calculate_sum(**json.loads(call2.function.arguments))

    messages += [
        {"role": "assistant", "tool_calls": resp2.choices[0].message.tool_calls},
        {"role": "tool", "tool_call_id": call2.id, "name": call2.function.name,
         "content": json.dumps(result2)},
    ]

    # ③ 最终回答
    final = openai.ChatCompletion.create(
        model="deepseek-chat",
        messages=messages,
    )
    print(final.choices[0].message.content)

if __name__ == "__main__":
    ask_beijing_plus_10()
```

**关键点**

| 行号    | 说明                                                                       |
| ----- | ------------------------------------------------------------------------ |
| 6     | `@openai_function` 自动：① 生成 JSON-Schema → 挂到 `.openai_schema`；② 校验入参 / 出参 |
| 25    | `tools` 直接用 `.openai_schema`，避免手写                                        |
| 32-61 | 其余逻辑和你原来的流程一致                                                            |

> 上面装饰器示例来自 GitHub `openai_function_call` 项目文档。([GitHub][3])

---

### 方案 B：原生 Pydantic ➜ 手动生成 Schema（无三方依赖）

如果你不想引入装饰器，只需几行：

```python
from pydantic import BaseModel, Field
import inspect, json, openai, os

class WeatherArgs(BaseModel):
    city: str = Field(..., description="City name")

def get_weather(city: str):
    return {"weather": "Sunny", "temperature": 26}

# 把 Pydantic 模型转成 JSON-Schema，再塞进 tools
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": get_weather.__doc__ or "Get city weather",
        "parameters": WeatherArgs.model_json_schema()   # ⭐ 一行搞定
    }
}]
```

然后其余代码仍用你原来那套“多轮工具调用”逻辑即可。

---

## 结论

* **Pydantic** 让“函数签名 ↔ JSON-Schema”保持一致、不易出错。
* 选用 **装饰器库（Instructor / openai-function-call / Agents SDK）** 可以做到**零手写 Schema**。
* 即便不依赖第三方，也能用 `BaseModel.model_json_schema()` 一行生成，依旧比纯手写省心。

把你的脚本替换成上面的任一方案即可感受到差异。如果想深入了解 Pydantic + Function Calling 在不同框架里的实现细节，随时告诉我！

[1]: https://openai.github.io/openai-agents-python/ref/function_schema/ "Function schema - OpenAI Agents SDK"
[2]: https://openai.github.io/openai-agents-python/tools/?utm_source=chatgpt.com "Tools - OpenAI Agents SDK"
[3]: https://github.com/jphme/openai_function_call "GitHub - jphme/openai_function_call: Helper functions to create openai function calls w/ pydantic"
