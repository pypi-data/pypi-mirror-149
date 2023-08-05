from typing import Any, Union

from pyntone.models.field import UpdateKey
from pydantic import BaseModel


class UpdateRecord(BaseModel):
    key: Union[int, str, UpdateKey]
    revision: Union[int, str, None] = None
    record: dict[str, Any]
    
    def data(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            'record': { key: { 'value': val } for key, val in self.record.items() },
        }
        if self.revision is not None:
            data['revision'] = self.revision

        if type(self.key) is UpdateKey:
            data['updateKey'] = self.key.dict()
        else:
            data['id'] = self.key
        return data

class DeleteRecord(BaseModel):
    id: Union[int, str]
    revision: Union[int, str]