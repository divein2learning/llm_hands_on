from langchain_community.chat_models import ChatZhipuAI
from dotenv import load_dotenv


def initialize():
    load_dotenv()
    llm = ChatZhipuAI(model="glm-4-flash")
    return llm

def initialize_4v():
    load_dotenv()
    llm = ChatZhipuAI(model="glm-4v-flash")
    return llm