__all__ = ['UserData', 'UserSchema']

from dataclasses import dataclass, field
from typing import Optional

import marshmallow_dataclass


@dataclass
class UserData:
    id: int = field()
    username: str = field()
    email: Optional[str] = field()
    is_admin: Optional[str] = field()


UserSchema = marshmallow_dataclass.class_schema(UserData)
