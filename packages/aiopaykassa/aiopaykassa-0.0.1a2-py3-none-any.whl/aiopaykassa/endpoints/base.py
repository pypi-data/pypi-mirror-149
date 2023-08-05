import abc
from typing import Generic, TypeVar, Any

from pydantic import BaseModel, Field, validator
from pydantic.generics import GenericModel

from aiopaykassa.utils import json

PayKassaType = TypeVar('PayKassaType', bound=Any)


class Request(BaseModel):
    data: dict


class Response(GenericModel, Generic[PayKassaType]):
    error: bool
    information: str | None = Field(None, alias="Information")
    message: str | None = None
    data: PayKassaType | None = None

    @validator("data", pre=True)
    def process_empty(cls, v: dict) -> dict | None:
        if not v:
            return None
        else:
            return v


class PayKassaEndpoint(abc.ABC, BaseModel):
    @property
    @abc.abstractmethod
    def __returning__(self) -> type:
        raise NotImplementedError

    @abc.abstractmethod
    def build_request(self, credentials: dict[str, str | int] = None, test_mode: bool = False) -> Request:
        raise NotImplementedError

    @abc.abstractmethod
    def url(self) -> str:
        raise NotImplementedError

    def build_response(self, data: dict[str, Any]) -> Response[PayKassaType]:
        return Response[self.__returning__](**data)

    class Config:
        json_loads = json.loads
        json_dumps = json.dumps
        use_enum_values = True

    def api_dict(self) -> dict:
        d = self.dict()
        for name, value in d.items():
            field = self.__fields__[name]
            mutate = field.field_info.extra.get("api_mutation")
            if mutate:
                d[name] = mutate(value)
        return d
