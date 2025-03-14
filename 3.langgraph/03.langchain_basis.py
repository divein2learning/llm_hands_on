# 1. 加载网页内容
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
data = loader.load()

# 2. 文本分割
# 使用递归字符分割器将文档分割成较小的块，每块500字符，无重叠
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)
# print(type(all_splits)) # class<'list'>
print(len(all_splits))

# 3. 初始化嵌入模型
# 使用modelscope下载BGE中文嵌入模型
from modelscope import snapshot_download
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
model_dir = snapshot_download("BAAI/bge-base-zh-v1.5")
bge_embeddings = HuggingFaceBgeEmbeddings(model_name=model_dir, show_progress=True)
# print(embeddings)

# 4. 创建向量存储
# 使用FAISS向量数据库存储文档嵌入
from langchain_community.vectorstores import FAISS
vectorstore = FAISS.from_documents(documents=all_splits, embedding=bge_embeddings)
print(vectorstore)

# 5. 获取RAG提示模板
from langchain import hub
from langchain.prompts import PromptTemplate
# 自定义多轮对话的提示模板
template = """使用以下上下文来回答用户的问题。如果你不知道答案，就说你不知道，请不要编造答案。

上下文: {context}

聊天历史:
{chat_history}

用户问题: {question}

请用中文回答。
"""
prompt = PromptTemplate(
    input_variables=["context", "chat_history", "question"],
    template=template
)

# 6. 初始化LLM模型
# 使用智谱AI的GLM-4-flash模型
from langchain_community.chat_models import ChatZhipuAI
from dotenv import load_dotenv
load_dotenv()
llm = ChatZhipuAI(model="glm-4-flash")

# 7. 构建多轮对话的检索问答链
from langchain.chains import ConversationalRetrievalChain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    combine_docs_chain_kwargs={"prompt": prompt}
)

# 8. 执行多轮对话
chat_history = []
while True:
    question = input("\n请输入您的问题(输入'quit'退出): ")
    if question.lower() == 'quit':
        break
        
    result = qa_chain({"question": question, "chat_history": chat_history})
    print("\nAI回答:", result['answer'])
    
    # 将当前对话加入历史记录
    chat_history.append((question, result['answer']))
