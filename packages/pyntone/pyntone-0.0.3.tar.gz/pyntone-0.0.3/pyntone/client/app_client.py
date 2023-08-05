from typing import Any, Generic, Optional, Union

from pyntone.http.http_client import HttpClent
from pyntone.kintone_request_config_builder import KintoneRequestParams
from pyntone.models import App
from pyntone.models.response import RecordModelT
from pyntone.url import build_path

class AppClient(Generic[RecordModelT]):
    def __init__(self, model: type[RecordModelT], http_client: HttpClent, default_app_id: Union[int, str, None], guest_space_id: Union[int, str, None] = None):
        self.model = model
        self.http_client = http_client
        self.default_app_id = default_app_id
        self.guest_space_id = guest_space_id
    
    def add_field_from_model(self, app_id: Union[int, str, None]=None):
        path = self._build_path_with_guest_space_id('app/form/fields', True)
        params = KintoneRequestParams(
            data = {
                'app': self._get_app_id(app_id),
                'properties': self.model.json()
            }
        )
        res = self.http_client.post(path, params)
        return res
    
    def deploy_app(self, apps: Optional[list[App]]=None, revert: bool=False):
        data: dict[str, Any] = { 'revert': revert }
        if apps is not None and len(apps) > 0:
            data['apps'] = [ app.dict() for app in apps ]
        else:
            data['apps'] = [ App(app=self._get_app_id(self.default_app_id), revision=-1).dict() ]

        params = KintoneRequestParams(data=data)
        path = self._build_path_with_guest_space_id('app/deploy', True)
        return self.http_client.post(path, params)
    
    def _get_app_id(self, app_id: Union[int, str, None]) -> Union[int, str]:
        if app_id is None:
            if self.default_app_id is None:
                raise ValueError('App ID is None')
            else:
                return self.default_app_id
        else:
            return app_id
    
    def _build_path_with_guest_space_id(self, endpoint_name: str, preview: bool) -> str:
        return build_path(endpoint=endpoint_name, guest_space_id=self.guest_space_id, preview=preview)