from model_init import initialize
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import asyncio
llm = initialize()

# =========================================================================================================
# prompt = ChatPromptTemplate.from_template("写一副关于{topic}的对联")
# parser = StrOutputParser()
# chain = prompt | llm | parser

# # sync
# chunks = []
# for chunk in chain.stream({"topic": "铜合金"}):  # type(chunk): AIMessageChunk
#     chunks.append(chunks)
#     print(chunk, end="|", flush=True)
# =========================================================================================================

# =========================================================================================================
# # async
# async def async_stream():
#     chunks = []
#     async for chunk in chain.astream({"topic": "铜合金"}):
#         chunks.append(chunk)
#         print(chunk, end="|", flush=True)
# asyncio.run(async_stream())
# =========================================================================================================

# =========================================================================================================
# # 流式json
# prompt = ChatPromptTemplate.from_template("写一副关于{topic}的对联，结果展示成一个json，json的key分别是上联下联和横批，key不要是中文。")
# parser = JsonOutputParser()
# chain = prompt | llm | parser

# async def async_json_stream():
#     async for chunk in chain.astream({"topic": "铜合金"}):
#         print(chunk, flush=True)
# asyncio.run(async_json_stream())
# =========================================================================================================


# =========================================================================================================
# # 流式解析
# template = "写三副关于{topic}的对联，结果展示成一个json，json的key分别是上联下联和横批，横批的key是transversals，value是对应的列表，key不要是中文。"
# prompt = ChatPromptTemplate.from_template(template)
# parser = JsonOutputParser()

# async def _extract_transversal_streaming(input_stream):
#     """A function that operates on input streams."""

#     async for input in input_stream:
#         if not isinstance(input, dict):
#             continue

#         if "transversals" not in input:
#             continue

#         transversals = input["transversals"]

#         if not isinstance(transversals, list):
#             continue
#         yield transversals
            
# chain = prompt | llm | parser | _extract_transversal_streaming

# async def async_extract_stream():
#     async for chunk in chain.astream({"topic": "铜合金"}):
#         print(chunk, flush=True)
# asyncio.run(async_extract_stream())
# =========================================================================================================

# event
# =========================================================================================================
# async def get_events():
#     async for event in llm.astream_events("写一副对联"):
#         print(f"========={event['event']}==========")
#         print(event)
#         print()
# asyncio.run(get_events())
# =========================================================================================================

# =========================================================================================================
prompt = ChatPromptTemplate.from_template("写一副关于{topic}的对联，结果展示成一个json，json的key分别是上联下联和横批，key不要是中文。")
parser = JsonOutputParser()
chain = prompt | llm | parser

# =============================
# async def async_json_stream_event():
#     async for event in chain.astream_events({"topic": "铜合金"}):
#         print(f"========={event['event']}==========")
#         print(event)
#         print()
# asyncio.run(async_json_stream_event())
# =============================

# =============================
async def parse_chain_event():
    num_events = 0
    async for event in chain.astream_events({"topic": "铜合金"}):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            print(
                f"Chat model chunk: {repr(event['data']['chunk'].content)}",
                flush=True,
            )
        if kind == "on_parser_stream":
            print(f"Parser chunk: {event['data']['chunk']}", flush=True)
        num_events += 1
        if num_events > 30:
            # Truncate the output
            print("...")
            break
asyncio.run(parse_chain_event())
# =========================================================================================================