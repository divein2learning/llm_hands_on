# 1. tool create
# 2. tool binding
# 3. tool calling
# 4. tool execution
# 可以通过python函数，pydantic Model，TypedDict类或者Langchain的Tool对象传递工具
# 文档字符串和类型提示很重要
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from model_init import initialize

llm = initialize()


@tool
def add(a: int, b: int) -> int:
    """执行加法算术，接受两个整数a和b，返回整数a+b"""
    return a + b


# ========================================================================================
# tools = [add]

# llm_with_tools = llm.bind_tools(tools)
# llm_without_tools_result = llm.invoke("20001203加12029245等于多少")
# print(getattr(llm_without_tools_result, "tool_calls"))
# print("without tools:", llm_without_tools_result.content)

# llm_tools_result = llm_with_tools.invoke("20001203加12029245等于多少")
# print("with tools:", add.invoke(getattr(llm_tools_result, "tool_calls")[0]['args']))
# ========================================================================================

# ========================================================================================
# class add(TypedDict):
#      """执行加法算术，接受两个整数a和b，返回整数a+b"""

#      a: Annotated[int, ..., "第一个参数"]
#      b: Annotated[int, ..., "第二个参数"]

# tools = [add]

# llm_with_tools = llm.bind_tools(tools)
# llm_tools_result = llm_with_tools.invoke("20001203+12029245结果是多少")
# print(getattr(llm_tools_result, "tool_calls"))
# ========================================================================================

# ========================================================================================
tools = [add]
llm_with_tools = llm.bind_tools(tools)
messages = [
    SystemMessage(
        "你是一个会调用工具来解决计算问题的AI，能调用工具的时候请不要自己臆想，请确保答案的准确性。"
    ),
    HumanMessage("20001203加12029245等于多少"),
]
ai_msg = llm_with_tools.invoke(messages)
# print(ai_msg.tool_calls)
messages.append(ai_msg)
print("tool call============>")
print(messages)

for tool_call in ai_msg.tool_calls:
    selected_tool = {"add": add}[tool_call["name"]]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)
print("tool message=========>")
print(messages)
final_llm_response = llm_with_tools.invoke(messages)
print(final_llm_response)
print("with tools:", final_llm_response.content)
# ========================================================================================
