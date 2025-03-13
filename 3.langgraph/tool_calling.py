# 1. tool create
# 2. tool binding
# 3. tool calling
# 4. tool execution

from model_init import initialize
from langchain_core.tools import tool
llm = initialize()

@tool
def add(a: int, b: int) -> int:
    """执行加法算术，接受两个整数a和b，返回整数a+b"""
    x = 1
    return a + b

tools = [add]

llm_with_tools = llm.bind_tools(tools)
llm_without_tools_result = llm.invoke("20001203加12029245等于多少")
print(getattr(llm_without_tools_result, "tool_calls"))
print("without tools:", llm_without_tools_result.content)

llm_tools_result = llm_with_tools.invoke("20001203加12029245等于多少")
print("with tools:", add.invoke(getattr(llm_tools_result, "tool_calls")[0]['args']))