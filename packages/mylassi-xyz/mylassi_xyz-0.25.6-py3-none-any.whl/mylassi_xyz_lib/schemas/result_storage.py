__all__ = [
    'ResultStorageInfoData', 'ResultStorageInfoSchema',
    'ResultStorageData', 'ResultStorageSchema',
    'ResultStorageListData', 'ResultStorageListSchema',
]

from dataclasses import dataclass, field
from typing import List

import marshmallow_dataclass


@dataclass
class ResultStorageInfoData:
    id: str = field()


@dataclass
class ResultStorageData:
    id: str = field()
    data: dict = field()


@dataclass
class ResultStorageListData:
    length: int = field()
    page: int = field()
    pages: int = field()
    items: List[ResultStorageInfoData] = field(default_factory=list)


ResultStorageInfoSchema = marshmallow_dataclass.class_schema(ResultStorageInfoData)()
ResultStorageSchema = marshmallow_dataclass.class_schema(ResultStorageData)()
ResultStorageListSchema = marshmallow_dataclass.class_schema(ResultStorageListData)()
