from typing import Union
from pprint import pp
from datetime import datetime

from pydantic import BaseModel, PositiveInt

class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: Union[datetime, None] = None
    tastes: dict[str, PositiveInt]

print(User.schema())

external_data = {
    'id': 123,
    'signup_ts': '2019-06-01 12:22',
    'tastes': {
        'wine': 9,
        b'cheese': 7,
        'cabbage': '1',
    }
}

user = User(**external_data)

pp(user.id)

pp(user.model_dump())
pp(User.model_json_schema())
