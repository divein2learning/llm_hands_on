from convert_pdf import get_chunks
from embedding_test import get_embeddings
from FlagEmbedding import FlagModel
from modelscope import snapshot_download
from qwen_model_test import get_model_and_tokenizer

SYSTEM_PROMPT = "你是一个文档问答助手，请保证回答的准确性和真实性。"

RAG_PROMPT = (
    "上下文信息如下。\n"
    "---------------------\n"
    "{context}\n"
    "---------------------\n"
    "请根据上下文信息而不是先验知识来回答用户的查询。"
    "你的回答要尽可能严谨。\n"
    "如果没有找到相关的内容，请明确指出。\n\n"
    "用户请求如下：\n"
    "{query}\n"
)


def find_top_k_chunks(embedding_model, query, chunks, k=5):
    # get embeddings
    content_embeddings = get_embeddings(embedding_model, chunks)
    query_embedding = get_embeddings(embedding_model, [query])
    # Calculete similarity
    scores = query_embedding @ content_embeddings.T  # scores.shape = (1, len(chunks))
    sorted_indices = sorted(
        range(len(scores[0])), key=lambda i: scores[0][i], reverse=True
    )
    return [chunks[i] for i in sorted_indices[:k]]


def search_context(
    query, chunks, embedding_model, k=5, verbose=False, reverse_chunk_indices=False
):
    top_k_chunks = find_top_k_chunks(embedding_model, query, chunks, k=5)
    if reverse_chunk_indices:
        top_k_chunks = top_k_chunks[::-1]
    if verbose:
        print("===========top5 chunks============")
        print(top_k_chunks)
    context_str = " ".join(top_k_chunks)
    return context_str


def generate(messages, verbose=False):
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    if verbose:
        print("===========model input text============")
        print(text)

    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(**model_inputs, max_new_tokens=512)
    generated_ids = [
        output_ids[len(input_ids) :]
        for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print("===========model response============")
    print(response)

    return response


if __name__ == "__main__":
    embedding_model_path = snapshot_download("BAAI/bge-base-zh-v1.5")

    embedding_model = FlagModel(
        embedding_model_path,
        query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
        use_fp16=True,
    )  # Setting use_fp16 to True speeds up computation with a slight performance degradation

    pdf_path = "E:\仿真软件驱动开发文档.pdf".replace("\\", "/")
    query = "仿真驱动的配置文件是什么？里面有什么配置项？"
    # query = "驱动的参数解析要解析成什么样子，接口长什么样？"

    chunks = get_chunks(pdf_path, chunk_size=200)

    verbose = False
    # RAG prompt
    context_str = search_context(query, chunks, embedding_model, k=5, verbose=verbose)
    prompt = RAG_PROMPT.format(context=context_str, query=query)
    print("===========RAG prompt============")
    print(prompt)

    model_name = "Qwen/Qwen2.5-0.5B-Instruct"
    model_path = snapshot_download(model_name)
    model, tokenizer = get_model_and_tokenizer(model_path)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    while True:
        messages.append({"role": "user", "content": prompt})
        response = generate(messages, verbose=verbose)
        messages.append({"role": "assistent", "content": response})

        query = input("请输入：")
        if query == "/exit":
            break
        context_str = search_context(
            query, chunks, embedding_model, k=5, verbose=verbose
        )
        prompt = RAG_PROMPT.format(context=context_str, query=query)
