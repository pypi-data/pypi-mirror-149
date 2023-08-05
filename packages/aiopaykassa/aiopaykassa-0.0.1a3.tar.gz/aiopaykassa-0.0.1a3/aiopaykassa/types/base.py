from pydantic import BaseModel

from ..utils import json


class PayKassaObject(BaseModel):
    class Config:
        json_loads = json.loads
        json_dumps = json.dumps
        use_enum_values = True
