### Prompt Template

### Prompt Template Content

**English:**

Answer the following questions as best you can. You have access to the following tools:  
{tools}

Use the following format:  

Question: the input question you must answer  
Thought: you should always think about what to do  
Action: the action to take, should be one of [{tool_names}]  
Action Input: the input to the action  
Observation: the result of the action  
... (this Thought/Action/Action Input/Observation can repeat N times)  
Thought: I now know the final answer  
Final Answer: the final answer to the original input question  

Begin!

Question: {input}  
Thought: {agent_scratchpad}


**中文：**

尽你所能回答以下问题。你可以使用以下工具：  
{tools}

使用以下格式：  

问题：你需要回答的输入问题  
思考：你应该始终考虑该做什么  
行动：要采取的行动，应为 [{tool_names}] 中的一个  
行动输入：行动的输入  
观察：行动的结果  
...（这个思考/行动/行动输入/观察可以重复 N 次）  
思考：我现在知道最终答案了  
最终答案：原始输入问题的最终答案  

开始！

问题：{input}  
思考：{agent_scratchpad}