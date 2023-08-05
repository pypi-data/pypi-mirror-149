from datetime import date, datetime, time, timedelta, timezone
from enum import Enum
from typing import Any, Optional, Union

from pydantic import BaseModel, validator

JST = timezone(timedelta(hours=9))

# Enum
class UnitPosition(Enum):
    BEFORE = 'BEFORE'
    AFTER = 'AFTER'

class Format(Enum):
    NUMBER = 'NUMBER'
    NUMBER_DIGIT = 'NUMBER_DIGIT'
    DATETIME = 'DATETIME'
    DATE = 'DATE'
    TIME = 'TIME'
    HOUR_MINUTE = 'HOUR_MINUTE'
    DAY_HOUR_MINUTE = 'DAY_HOUR_MINUTE'

class Align(Enum):
    HORIZONTAL = 'HORIZONTAL'
    VERTICAL = 'VERTICAL'

class EntityType(Enum):
    USER = 'USER'
    GROUP = 'GROUP'
    ORGANIZATION = 'ORGANIZATION'

class LookUpFieldType(Enum):
    SINGLE_LINE_TEXT = 'SINGLE_LINE_TEXT'
    NUMBER = 'NUMBER'
    LINK = 'LINK'


class FieldConfig:
    def __init__(self, model:type, property) -> None:
        self.model = model
        self.property = property

class BaseField(BaseModel):
    type: str
    
    @staticmethod
    def config() -> Any:
        raise NotImplementedError()

class BaseDatetimeField(BaseField):
    value: datetime
    
    @validator('value')
    def __convert_tz(cls, dt: datetime):
        return dt.astimezone(tz=JST)

class RecordNumber(BaseField):
    value: str
    
    @staticmethod
    def config(label: str, code: Optional[str] = None) -> Any:
        return FieldConfig(RecordNumber, {
            'label': label,
            'code': code
        })

class Id(BaseField):
    value: int
    
    @staticmethod
    def config(label: str, code: Optional[str] = None) -> Any:
        return FieldConfig(Id, {
            'label': label,
            'code': code
        })

class Revision(BaseField):
    value: int

    @staticmethod
    def config(label: str, code: Optional[str] = None) -> Any:
        return FieldConfig(Revision, {
            'label': label,
            'code': code
        })

class User(BaseModel):
    code: str
    name: str

class Creator(BaseField):
    value: User
    
    @staticmethod
    def config(label: str, code: Optional[str] = None) -> Any:
        return FieldConfig(Creator, {
            'label': label,
            'code': code
        })

class CreatedTime(BaseDatetimeField):
    @staticmethod
    def config(label: str, code: Optional[str] = None) -> Any:
        return FieldConfig(CreatedTime, {
            'label': label,
            'code': code
        })

class Modifier(BaseField):
    value: User
    
    @staticmethod
    def config(label: str, code: Optional[str] = None) -> Any:
        return FieldConfig(Modifier, {
            'label': label,
            'code': code
        })

class UpdatedTime(BaseDatetimeField):
    @staticmethod
    def config(label: str, code: Optional[str] = None) -> Any:
        return FieldConfig(UpdatedTime, {
            'label': label,
            'code': code
        })

class SingleLineText(BaseField):
    type: str
    value: str
    
    @staticmethod
    def config(label: str, code: Optional[str] = None, no_label:bool=False, required:bool=False,
            min_length:Union[str,int]='', max_length:Union[str,int]='', 
            expression:str='', hide_expression:bool=False, unique:bool=False, default_value:Union[str,int]='') -> Any:
        return FieldConfig(SingleLineText, {
            'type': 'SINGLE_LINE_TEXT',
            'label': label,
            'code': code,
            'noLabel': no_label,
            'required': required,
            'minLength': min_length,
            'maxLength': max_length,
            'expression': expression,
            'hideExpression': hide_expression,
            'unique': unique,
            'defaultValue': default_value
        })

class Number(BaseField):
    value: int

    @staticmethod
    def config(label: str, code: Optional[str] = None, no_label:bool=False, required:bool=False,
            min_length:Union[str,int]='', max_length:Union[str,int]='', 
            digit:bool=False, unique:bool=False, default_value:Union[str,int]='',
            display_scale:Union[str,int]='', unit:str='', unit_position:UnitPosition=UnitPosition.BEFORE) -> Any:
        return FieldConfig(Number, {
            "type": "NUMBER",
            'code': code,
            "label": label,
            "noLabel": no_label,
            "required": required,
            "minValue": min_length,
            "maxValue": max_length,
            "digit": digit,
            "unique": unique,
            "defaultValue": default_value,
            "displayScale": display_scale,
            "unit": unit,
            "unitPosition": unit_position.value
        })

class Calc(BaseField):
    value: int

    @staticmethod
    def config(label: str,  expression:str, code: Optional[str] = None, no_label:bool=False,
            required:bool=False, format:Format=Format.NUMBER, hide_expression:bool=False,
            display_scale:Union[str,int]='', unit:str='', unit_position:UnitPosition=UnitPosition.BEFORE) -> Any:
        return FieldConfig(Calc, {
            "type": "CALC",
            "label": label,
            'code': code,
            "noLabel": no_label,
            "required": required,
            "expression": expression,
            "format": format.value,
            "displayScale": display_scale,
            "hideExpression": hide_expression,
            "unit": unit,
            "unitPosition": unit_position
        })

class MultiLineText(BaseField):
    value: str

    @staticmethod
    def config(label: str, code: Optional[str] = None, no_label:bool=False, required:bool=False, default_value:Union[str,int]='') -> Any:
        return FieldConfig(MultiLineText, {
            'type': 'MULTI_LINE_TEXT',
            'label': label,
            'code': code,
            'noLabel': no_label,
            'required': required,
            'defaultValue': default_value
        })

class RichText(BaseField):
    value: str

    @staticmethod
    def config(label: str, code: Optional[str] = None, no_label:bool=False, required:bool=False, default_value:Union[str,int]='') -> Any:
        return FieldConfig(RichText, {
            'type': 'RICH_TEXT',
            'label': label,
            'code': code,
            'noLabel': no_label,
            'required': required,
            'defaultValue': default_value
        })

class Option(BaseModel):
    label: str
    index: int

class CheckBox(BaseField):
    value: list[str]
    
    @staticmethod
    def config(label: str, options: list[Option], code: Optional[str] = None, no_label:bool=False, required:bool=False, default_value:list[Union[str,int]]=[], align: Align=Align.HORIZONTAL) -> Any:
        return FieldConfig(CheckBox, {
            "type": "CHECK_BOX",
            "code": code,
            "label": label,
            "noLabel": no_label,
            "required": required,
            "options": options,
            "defaultValue": default_value,
            "align": align.value
        })

class RadioButton(BaseField):
    value: str
    
    @staticmethod
    def config(label: str, options: list[Option], code: Optional[str] = None, no_label:bool=False, required:bool=False, default_value:Union[str,int]='', align: Align=Align.HORIZONTAL) -> Any:
        return FieldConfig(RadioButton, {
            "type": "RADIO_BUTTON",
            "code": code,
            "label": label,
            "noLabel": no_label,
            "required": required,
            "options": options,
            "defaultValue": default_value,
            "align": align
        })

class DropDown(BaseField):
    value: str
    
    @staticmethod
    def config(label: str, options: list[Option], code: Optional[str] = None, no_label:bool=False, required:bool=False, default_value:list[Union[str,int]]=[]) -> Any:
        return FieldConfig(DropDown, {
            "type": "DROP_DOWN",
            "code": code,
            "label": label,
            "noLabel": no_label,
            "required": required,
            "options": options,
            "defaultValue": default_value
        })

class MultiSelect(BaseField):
    value: list[str]
    
    @staticmethod
    def config(label: str, options: list[Option], code: Optional[str] = None, no_label:bool=False, required:bool=False, default_value:list[Union[str,int]]=[]) -> Any:
        return FieldConfig(MultiSelect, {
            "type": "MULTI_SELECT",
            "code": code,
            "label": label,
            "noLabel": no_label,
            "required": required,
            "options": options,
            "defaultValue": default_value
        })

class FileContent(BaseModel):
    content_type: str
    file_key: str
    name: str
    size: int

class File(BaseField):
    value: list[FileContent]

class Link(BaseField):
    value: str

class Date(BaseField):
    value: date
    
    @staticmethod
    def config(label: str, code: Optional[str] = None, no_label:bool=False, required:bool=False, unique:bool=False, default_value:Union[str,int]='', default_now_value: bool=False) -> Any:
        return FieldConfig(Date, {
            "type": "DATE",
            "code": code,
            "label": label,
            "noLabel": no_label,
            "required": required,
            "unique": unique,
            "defaultValue": default_value,
            "defaultNowValue": default_now_value
        })

class Time(BaseField):
    value: time
    
    @staticmethod
    def config(label: str, code: Optional[str] = None, no_label:bool=False, required:bool=False, default_value:Union[str,int]='', default_now_value: bool=False) -> Any:
        return FieldConfig(Time, {
            "type": "TIME",
            "code": code,
            "label": label,
            "noLabel": no_label,
            "required": required,
            "defaultValue": default_value,
            "defaultNowValue": default_now_value
        })

class Datetime(BaseDatetimeField):
    @staticmethod
    def config(label: str, code: Optional[str] = None, no_label:bool=False, required:bool=False, default_value:Union[str,int]='', default_now_value: bool=False) -> Any:
        return FieldConfig(Datetime, {
            "type": "TIME",
            "code": code,
            "label": label,
            "noLabel": no_label,
            "required": required,
            "defaultValue": default_value,
            "defaultNowValue": default_now_value
        })

class Entity(BaseModel):
    type: EntityType
    code: str

class UserSelect(BaseField):
    value: list[User]
    
    @staticmethod
    def config(label: str, code: Optional[str] = None, no_label:bool=False, required:bool=False, entities:list[Entity]=[], default_value:list[Union[str,int]]=[]) -> Any:
        return FieldConfig(UserSelect, {
            "type": "USER_SELECT",
            "code": code,
            "label": label,
            "noLabel": no_label,
            "required": required,
            "entities": entities,
            "defaultValue": default_value
        })

class Category(BaseField):
    value: list[str]

class Status(BaseField):
    value: str

class StatusAssignee(BaseField):
    value: list[User]

class RelatedApp(BaseModel):
    # TODO
    app: Union[int, str] = ''
    code: str = ''

class FieldMapping(BaseModel):
    field: str
    related_field: str

class LookUp(BaseField):
    @staticmethod
    def config(label: str, type: LookUpFieldType, related_app:RelatedApp, related_key_field: str, field_mappings:list[FieldMapping]=[], lookup_picker_fields: list[str]=[], filter_cond:str='', sort:str='', code: Optional[str] = None, no_label:bool=False, required:bool=False, default_value:list[Union[str,int]]=[]) -> Any:
        return FieldConfig(LookUp, {
            "type": type.value,
            "code": code,
            "label": label,
            "noLabel": no_label,
            "required": required,
            "lookup": {
                "relatedApp": related_app.json(),
                "relatedKeyField": related_key_field,
                "fieldMappings": field_mappings,
                "lookupPickerFields": lookup_picker_fields,
                "filterCond": filter_cond,
                "sort": sort
            }
        })

class SubTable(BaseField):
    # TODO
    pass

class Organization(BaseModel):
    code: str
    name: str

class OrganizationSelect(BaseField):
    value: list[Organization]
    
    @staticmethod
    def config(label: str, code: Optional[str] = None, no_label:bool=False, required:bool=False, entities:list[Entity]=[], default_value:list[Union[str,int]]=[]) -> Any:
        return FieldConfig(OrganizationSelect, {
            "type": "ORGANIZATION_SELECT",
            "code": code,
            "label": label,
            "noLabel": no_label,
            "required": required,
            "entities": entities,
            "defaultValue": default_value
        })

class Group(BaseField):
    code: str
    
    @staticmethod
    def config(label: str, code: Optional[str] = None, no_label:bool=False, open_group:bool=False) -> Any:
        return FieldConfig(OrganizationSelect, {
            "type": "GROUP",
            "code": code,
            "label": label,
            "noLabel": no_label,
            "openGroup": open_group
        })

class KintoneGroup(BaseModel):
    code: str
    name: str

class GroupSelect(BaseField):
    value: list[KintoneGroup]
    
    @staticmethod
    def config(label: str, code: Optional[str] = None, no_label:bool=False, required:bool=False, entities:list[Entity]=[], default_value:list[Union[str,int]]=[]) -> Any:
        return FieldConfig(GroupSelect, {
            "type": "GROUP_SELECT",
            "code": code,
            "label": label,
            "noLabel": no_label,
            "required": required,
            "entities": entities,
            "defaultValue": default_value
        })

####

class UpdateKey(BaseModel):
    field: str
    value: str
