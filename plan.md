# 主要功能逻辑
1. 根据设计提取实体和关系的schema，并将其转换为pydantic模型
2. 使用langextract提取出实体和关系
3. 将提取出的实体和关系通过cypher语句写入到neo4j中
4. 针对用户问题再用大模型基于schema生成cypher语句，查询图谱
5. 将查询的图谱再让大模型进行返回

# 主要技术栈
1. pydantic: 用于定义实体和关系的schema
2. langextract: 用于实体和关系的提取
3. neo4j: 用于存储图谱
4. openai: 用于大模型的调用
5. langgraph: 用于对话流程的控制
6. FastAPI: 用于接口的实现

# 包管理工具
uv

# 参考项目
1. [ai-knowledge-graph](https://github.com/robert-mcdermott/ai-knowledge-graph)
- triple extraction
- entity standardization
- relation inference
- visualization
2. [langextract](https://github.com/google/langextract.git)
3. [Docling Graph](https://github.com/langchain/langgraph.git)
4. [graphrag-Chinese-llm](https://github.com/via007/graphrag-Chinese-llm.git)
