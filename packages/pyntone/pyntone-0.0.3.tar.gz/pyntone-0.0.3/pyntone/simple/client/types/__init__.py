from dataclasses import dataclass
from typing import Generic, Optional, TypeVar, Union, Any

from pyntone.models.base import KintoneBaseModel
from pydantic import BaseModel

class KintoneBaseResponse:
    def __init__(self, **kargs) -> None:
        print(self.__annotations__)
        pass

class Field:
    def __init__(self, data: dict[str, Any]) -> None:
        self.__data = data
    
    def __getattr__(self, __name: str) -> Any:
        return self.__data[__name]
    
    def __repr__(self) -> str:
        return 'Field({})'.format(', '.join([ f'{key}={val}' for key, val in self.__data.items() ]))

class Record:
    def __init__(self, data: dict[str, Any]) -> None:
        self.__data = { key: Field(val) for key, val in data.items() }
    
    def __getattr__(self, __name: str) -> Field:
        return self.__data[__name]
    
    def __repr__(self) -> str:
        return 'Record({})'.format(', '.join([ f'{key}={val}' for key, val in self.__data.items() ]))

@dataclass
class ResponseRecord:
    record: Record

@dataclass
class ResponseRecords:
    records: list[Record]
    total_count: Optional[int] = None

class UpdateRecordResponse(BaseModel):
    revision: int

class AddRecordResponse(BaseModel):
    id: Union[int, str]
    revision: int

class AddRecordsResponse(BaseModel):
    ids: list[Union[int, str]]
    revisions: list[int]

class UpdateRecordsResponseRevision(BaseModel):
    id: Union[int, str]
    revision: int

class UpdateRecordsResponse(BaseModel):
    records: list[UpdateRecordsResponseRevision]

class DeleteRecordsResponse(BaseModel):
    value: dict
