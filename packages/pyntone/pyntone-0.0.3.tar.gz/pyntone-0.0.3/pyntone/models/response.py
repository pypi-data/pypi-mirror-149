from dataclasses import dataclass
from typing import Generic, Optional, TypeVar, Union

from pyntone.models.base import KintoneBaseModel
from pydantic import BaseModel


def converter(string: str) -> str:
    if string in {'id_', 'revision_'}:
        return '$'+string.replace('_', '')
    elif string in {'created_time_', 'modifier_', 'record_number_', 'creator_', 'updated_time_'}:
        data = {'created_time_': '作成日時', 'modifier_': '更新者', 'record_number_': 'レコード番号', 'creator_': '作成者', 'updated_time_': '更新日時'}
        return data[string]
    else:
        return string

RecordModelT = TypeVar('RecordModelT', bound=KintoneBaseModel)

class KintoneBaseResponse:
    def __init__(self, **kargs) -> None:
        print(self.__annotations__)
        pass

@dataclass
class ResponseRecord(Generic[RecordModelT]):
    record: RecordModelT

@dataclass
class ResponseRecords(Generic[RecordModelT]):
    records: list[RecordModelT]
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
