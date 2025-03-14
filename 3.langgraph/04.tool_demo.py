from dotenv import load_dotenv
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()


@tool
def search(query: str):
    """call to serf the web"""
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


ddg_search = DuckDuckGoSearchRun()
# result = ddg_search.invoke("你好，今天宁波的天气如何？")
# print(result)

tools = [ddg_search]
# model = ChatOllama(model="qwen2.5")
model = ChatZhipuAI(model="glm-4-flash", temperature=0.7)

agent = create_react_agent(model, tools, debug=True)

# query = "what's the weather in San Francisco?"
query = "介绍一下manus和openmanus的区别，搜索后整理给我"
final_state = agent.invoke({"messages": [{"role": "user", "content": query}]})

print(final_state["messages"][-1].content)
