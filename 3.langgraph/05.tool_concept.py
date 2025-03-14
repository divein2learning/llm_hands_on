from model_init import initialize
from langchain_core.tools import tool
llm = initialize()

@tool
def add(a: int, b: int) -> int:
    """执行加法算术，接受两个整数a和b，返回整数a+b"""
    x = 1
    return a + b


print(add) 
print(add.name) # add
print(add.description) # 执行加法算术，接受两个整数a和b，返回整数a+b
print(add.args) # {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}
result = add.invoke({"a": 2, "b": 3})
print(type(result)) # <class 'int'>
print(result) # 5
# result = add.invoke({"a": 2.2, "b": 3}) # ValidationError
