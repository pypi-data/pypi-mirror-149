__all__ = [
    'ProviderOptionData', 'ProviderOptionSchema',
    'ProviderData', 'ProviderSchema', 'ProviderListData', 'ProviderListSchema',
    'ProviderCredentialData', 'ProviderCredentialSchema',
    'DocumentOptionData', 'DocumentOptionSchema',
    'DocumentData', 'DocumentSchema'
]

import datetime
from dataclasses import dataclass, field
from typing import Optional, List

import marshmallow_dataclass

from .users import UserData


@dataclass
class ProviderOptionData:
    name: str = field()
    type: str = field()
    credentials: str = field()


@dataclass
class ProviderData:
    id: str = field()
    name: str = field()
    type: str = field()


@dataclass
class ProviderListData:
    length: int = field()
    page: int = field()
    pages: int = field()
    items: List[ProviderData] = field(default_factory=list)


@dataclass
class ProviderCredentialData:
    id: str = field()
    name: str = field()
    type: str = field()
    salt: str = field()
    credentials: str = field()


@dataclass
class DocumentOptionData:
    name: str = field()
    provider: str = field()
    path: str = field()

    on_created: Optional[datetime.datetime] = field()
    on_updated: Optional[datetime.datetime] = field()
    owner_id: Optional[int] = field()


@dataclass
class DocumentData:
    id: str = field()
    name: str = field()

    owner: Optional[UserData] = field()


ProviderOptionSchema = marshmallow_dataclass.class_schema(ProviderOptionData)()
ProviderSchema = marshmallow_dataclass.class_schema(ProviderData)()
ProviderListSchema = marshmallow_dataclass.class_schema(ProviderListData)()
ProviderCredentialSchema = marshmallow_dataclass.class_schema(ProviderCredentialData)()

DocumentOptionSchema = marshmallow_dataclass.class_schema(DocumentOptionData)()
DocumentSchema = marshmallow_dataclass.class_schema(DocumentData)()
