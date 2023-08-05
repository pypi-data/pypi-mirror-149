__all__ = [
    'LoginRequestData', 'LoginRequestSchema',
    'LoginResponseData', 'LoginResponseSchema'
]

from dataclasses import dataclass

import marshmallow_dataclass

from .users import UserData


@dataclass
class LoginRequestData:
    username: str
    password: str


@dataclass
class LoginResponseData:
    user: UserData
    token: str


LoginRequestSchema = marshmallow_dataclass.class_schema(LoginRequestData)()
LoginResponseSchema = marshmallow_dataclass.class_schema(LoginResponseData)()
