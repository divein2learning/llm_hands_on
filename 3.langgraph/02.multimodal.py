from langchain_core.messages import HumanMessage
from model_init import initialize_4v

llm = initialize_4v()


image_url = "https://python.langchain.com/assets/images/tool_calling_concept-552a73031228ff9144c7d59f26dedbbf.png"
message = HumanMessage(
    content=[
        {"type": "text", "text": "描述一下这张图"},
        {"type": "image_url", "image_url": {"url": image_url}},
    ],
)
response = llm.invoke([message])
print(response.content)
