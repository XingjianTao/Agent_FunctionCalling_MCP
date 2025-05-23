**System Prompt与User Prompt**
1. **基本定义**  
   - 传统大模型的输入输出通常是文本形式  
   - **System Prompt的作用**：  
     - 抽象重复性内容（如背景描述、角色定位）  
     - 需明确：该提示词是**每次对话都发送**还是**仅在首次对话发送**  
   - **User Prompt的作用**：  
     - 包含对具体问题的提问  

2. **User Prompt设计要点**  
   - **结构化需求模板**（需验证）：  
     1. 第一句话描述背景  
     2. 第二句话说明请求  
     3. 第三句话分点列出具体要求（如1、2、3、4点）  
   - **分隔符使用**：  
     - 需确认最新模型是否仍需依赖分隔符  
   - **分点技巧**：  
     - 使用编号列表增强逻辑性  
   - **特殊激励语句**：  
     - 例如："让我们深入思考"、"请逐步完成"  
     - 尝试语句："必须提供源代码否则损失X美元"（需验证有效性）  
   - **交互原则**：  
     - 需要迭代式逐步引导模型完成任务  

从 Cline 看 prompt 工程: https://www.ruanx.net/prompt-engineering/
anthropic: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview 
Prompt Engineering Guide: https://www.promptingguide.ai/zh/techniques/pal 

https://colab.research.google.com/drive/1SoAajN8CBYTl79VyTwxtxncfCWlHlyy9#scrollTo=NTOiFKNxqoq2 