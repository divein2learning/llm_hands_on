from modelscope import snapshot_download
from FlagEmbedding import FlagModel


def get_embeddings(embedding_model, chunks):
    embeddings = embedding_model.encode(chunks)
    return embeddings

# queries = ['query_1', 'query_2']
# passages = ["样例文档-1", "样例文档-2"]
# q_embeddings = model.encode_queries(queries)
# p_embeddings = model.encode(passages)
# scores = q_embeddings @ p_embeddings.T

if __name__ == "__main__":
    embedding_model_path = snapshot_download('BAAI/bge-base-zh-v1.5')
    chunks= [
    "Michael Jackson was a legendary pop icon known for his record-breaking music and dance innovations.",
    "Fei-Fei Li is a professor in Stanford University, revolutionized computer vision with the ImageNet project.",
    "Brad Pitt is a versatile actor and producer known for his roles in films like 'Fight Club' and 'Once Upon a Time in Hollywood.'",
    "Geoffrey Hinton, as a foundational figure in AI, received Turing Award for his contribution in deep learning.",
    "Eminem is a renowned rapper and one of the best-selling music artists of all time.",
    "Taylor Swift is a Grammy-winning singer-songwriter known for her narrative-driven music.",
    "Sam Altman leads OpenAI as its CEO, with astonishing works of GPT series and pursuing safe and beneficial AI.",
    "Morgan Freeman is an acclaimed actor famous for his distinctive voice and diverse roles.",
    "Andrew Ng spread AI knowledge globally via public courses on Coursera and Stanford University.",
    "Robert Downey Jr. is an iconic actor best known for playing Iron Man in the Marvel Cinematic Universe.",
    ]
    model = FlagModel(embedding_model_path, 
                  query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                  use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation
    embeddings = get_embeddings(model, chunks)
    print(type(embeddings))
