from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from model_init import initialize

llm = initialize()

system_message = SystemMessage("你是一个大模型砖家")
user_message = HumanMessage("能给我讲一个大模型相关的笑话吗")
# print(system_message)
# print(user_message)

template = ChatPromptTemplate(messages=[system_message, user_message])
# print(template)
for chunk in llm.stream(template.format()):
    print(chunk.content, flush=True, end="")
