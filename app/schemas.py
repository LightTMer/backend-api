from typing import List
from pydantic import BaseModel, field_validator


class UserSchema(BaseModel):
    user_id: int
    name: str
    sex: str
    home_town: str
    friends: list[int] = []

    @field_validator("sex", mode="before")
    @classmethod
    def validate_sex(cls, v) -> str:
        if not v:
            return ""

        if not isinstance(v, int):
            raise ValueError("sex should be int")

        if v == 1:
            return "Female"
        elif v == 2:
            return "Male"
        else:
            raise ValueError("sex could be only 1 or 2")


class GroupSchema(BaseModel):
    group_id: int
    name: str
    members: list[int] = []


class DetailedGroupSchema(GroupSchema):
    subscribers: List[UserSchema]


class DetailedUserSchema(UserSchema):
    follows: List[UserSchema]
    subscribes: List[GroupSchema]


class CreateUserSchema(UserSchema):
    follows: list[int]
    subscribes: list[int]


class CreateGroupSchema(GroupSchema):
    subscribers: list[int]
