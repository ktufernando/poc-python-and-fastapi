from typing import Any, List, Optional

import peewee
from pydantic import BaseModel, EmailStr
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class UserRequestModel(BaseModel):
    username: str
    email: EmailStr
    #email: Optional[str] = None


class UserResponseModel(UserRequestModel):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class UserListResponseModel(BaseModel):
    __root__: List[UserResponseModel]


class OkResponseModel(BaseModel):
    message: str
