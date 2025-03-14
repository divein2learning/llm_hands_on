# 记录langchain学习所用的code
个人学习所用，代码多来自官网示例，会持续更新（LangChain和LangGraph的代码都合并在`3.langgraph`里

# TODOs:
- [x] LangChain核心内容
- [ ] 添加LangChain主要数据结构用法(Runnable)
- [ ] 添加LangGraph示例
- [ ] 丰富代码注释
- [ ] OpenManus核心代码剖析
  
# 代码目录
|代码|备注|
|---|---|
|[1.rag](1.rag/rag_pipeline.py)|RAG的简单实现，使用pdfminer解析pdf，按字符split chunk，用Qwen/Qwen2.5-0.5B-Instruct模型，embedding模型是bge-base-zh-v1.5|
|[2.pydantic](2.pydantic/demo.py)|pydantic的BaseModel类的初步了解，主要了解BaseModel的json schema，在后续工具调用和json解析会使用|
|[3.langgraph/model_init.py](3.langgraph/model_init.py)|初始化llm，包括GLM-4-flash和GLM-4V-flash|
|[3.langgraph/01.messages.py](3.langgraph/01.messages.py)|langchain的基本Message类，包括SystemMessage、HumanMessage、AIMessage|
|[3.langgraph/02.multimodal.py](3.langgraph/02.multimodal.py)|多模态模型的调用content形式|
|[3.langgraph/03.langchain_basis.py](3.langgraph/03.langchain_basis.py)|langchain实现简单QA chain的示例|
|[3.langgraph/04.tool_demo.py](3.langgraph/04.tool_demo.py)|内置tool的使用和@tool装饰器|
|[3.langgraph/05.tool_concept.py](3.langgraph/05.tool_concept.py)|tool的基本属性以及调用|
|[3.langgraph/06.tool_calling.py](3.langgraph/06.tool_calling.py)|使用tool和不适用tool的结果对比|
|[3.langgraph/07.structured_outputs.py](3.langgraph/07.structured_outputs.py)|输出结构化，json形式|
|[3.langgraph/08.stream.py](3.langgraph/08.stream.py)|流式输出，同步流式，异步流式，事件流|
|[3.langgraph/09.langgraph_graph.ipynb](3.langgraph/09.langgraph_graph.ipynb)|langgraph的基本对话Graph构建流程，以及如何在graph中加入tool调用|
|[3.langgraph/09.langgraph_graph_run.py](3.langgraph/09.langgraph_graph_run.py)|langgraph的基本对话Graph，带tool调用|
|[3.langgraph/10.memory_langgraph.ipynb](3.langgraph/10.memory_langgraph.ipynb)|带有Memory的Graph，带tool调用|