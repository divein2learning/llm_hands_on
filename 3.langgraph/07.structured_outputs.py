from model_init import initialize

llm = initialize()

# pydantic类的方式，返回对应的pydantic类
from pydantic import BaseModel, Field
class Joke(BaseModel):
    """给笑话打分，打分相反，好笑的低分，不好笑的高分，分数在1-10，并且给出笑话的笑点"""
    rate: str = Field(description="给笑话打分，1-10")
    punchline: str = Field(description="笑话的笑点")

# # TypedDict的方式，返回dict
# from typing_extensions import Annotated, TypedDict
# class Joke(TypedDict):
#     """给笑话打分，打分相反，好笑的低分，不好笑的高分，分数在1-10，并且给出笑话的笑点"""
#     rate: Annotated[int, ..., "给笑话打分，1-10"]
#     punchline: Annotated[str, ..., "笑话的笑点"]

# # # json schema
# Joke = {
#     "title": "joke",
#     "description": "给笑话打分，打分相反，好笑的低分，不好笑的高分，分数在1-10，并且给出笑话的笑点",
#     "type": "object",
#     "properties": {
#         "rate": {
#             "type": "str",
#             "description": "给笑话打分，1-10",
#         },
#         "punchline": {
#             "type": "str",
#             "description": "笑话的笑点",
#         },
#     },
#     "required": ["rate", "punchline"],
# }

llm_with_structure = llm.with_structured_output(Joke)
structured_output = llm_with_structure.invoke("给我一个笑话，要好笑的")
print(structured_output)
print(type(structured_output))

# llm_with_structure = llm.with_structured_output(Joke)
# for chunk in llm_with_structure.stream("给我一个笑话，要好笑的"):
#     print(chunk)
