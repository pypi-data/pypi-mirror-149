from abc import ABCMeta
from typing import Any

from pyntone.models.field import (BaseField, CreatedTime, Creator, FieldConfig, Id,
                                  Modifier, RecordNumber, Revision,
                                  UpdatedTime)


class KintoneBaseMeta(ABCMeta):
    def __init__(self, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> None:
        if hasattr(self, '__annotations__'):
            for attr_name in self.__annotations__.keys():
                attr = namespace[attr_name]
                if type(attr) is FieldConfig and attr.property.get('code') is None:
                    attr.property['code'] = attr_name
        super().__init__(name, bases, namespace)

class KintoneBaseModel(metaclass=KintoneBaseMeta):
    _id_: Id = Id.config('$id', code='$id')
    _revision_: Revision = Revision.config('$revision', code='$revision')
    _record_number_: RecordNumber = RecordNumber.config('レコード番号', code='レコード番号')
    _created_time_: CreatedTime = CreatedTime.config('作成日時', code='作成日時')
    _creator_: Creator = Creator.config('作成者', code='作成者')
    _updated_time_: UpdatedTime = UpdatedTime.config('更新日時', code='更新日時')
    _modifier_: Modifier = Modifier.config('更新者', code='更新者')
    
    def __new__(cls, **kargs):
        self = super().__new__(cls)
        for key in dir(cls):
            attr = getattr(cls, key)
            if type(attr) is FieldConfig:
                field_code = attr.property['code']
                value = attr.model(**kargs[field_code]) if field_code in kargs else ...
                self.__setattr__(key, value)
        return self
    
    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        attrs = []
        for name in self.__dir__():
            attr = self.__getattribute__(name)
            if issubclass(type(attr), BaseField):
                attrs.append(f"{name}={attr.__class__.__name__}({attr})")
        return '{}({})'.format(cls_name, ', '.join(attrs))
    
    @classmethod
    def json(cls) -> dict[str, Any]:
        ret = {}
        for anno in cls.__annotations__.keys():
            attr = getattr(cls, anno).property
            ret[attr['code']] = attr
        return ret