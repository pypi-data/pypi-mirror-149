# 使用例

## Kintoneアプリの定義
```python
from pyntone.models.base import KintoneBaseModel
from pyntone.models.field import SingleLineText

class User(KintoneBaseModel):
    name: SingleLineText = SingleLineText.config('名前', default_value='')
    user_id: SingleLineText = SingleLineText.config('ユーザーID', default_value='')
    uid: SingleLineText = SingleLineText.config('uid', default_value='')
```

## クライアントの作成
```python
from pyntone.models.auth import ApiTokenAuth
from pyntone.kintone_rest_api_client import KintoneRestAPIClient


auth = ApiTokenAuth(api_token=kintone_api_key)
client = KintoneRestAPIClient(User, kintone_domain, kintone_app_id, auth)
```

## レコード一件取得
```python
res = client.record.get_record(id=1)
print(res.record.name)
```

## レコード一括取得
```python
res = client.record.get_records(fields=[])
for i in res.records:
    print(i.name)
```

## レコード登録
```python
record = {
    'name': 'name1',
    'uid': 'aaaaa',
    'user_id': 'hello'
}
res = client.record.add_record(record=record)
print(res)
```

## レコード一括登録
```python
add_records = [
    {'name': 'name1', 'uid': 'aaaaa', 'user_id': 'hello'},
    {'name': 'name2', 'uid': 'bbbbb', 'user_id': 'world'},
]
res = client.record.add_records(add_records)
print(res)
```

## レコード更新
```python
record = {
    'name': '名前１',
}
res = client.record.update_record(12, record)
print(res)
```

## レコード一括更新
```python
from pyntone.models.record import UpdateRecord

update_records = [
    UpdateRecord(key=12, record={'name': '123', 'user_id': 'hellohello'}),
    UpdateRecord(key=11, record={'uid': '456', 'user_id': 'worldworld'}),
]
res = client.record.update_records(update_records)
print(res)
```

## レコード削除
```python
from pyntone.models.record import DeleteRecord

res = client.record.delete_records([12, DeleteRecord(id=27, revision=2)])
print(res)
```