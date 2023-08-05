import base64
import json
from enum import Enum
from typing import Any
from urllib.parse import urljoin

from pydantic import BaseModel

from pyntone.models.auth import ApiTokenAuth, DiscriminatedAuth, PasswordAuth


class HttpMethod(Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'

class KintoneRequestParams(BaseModel):
    url_params: dict[str, Any] = {}
    data: dict[str, Any] = {}

class KintoneRequestConfigBuilder():
    def __init__(self, auth: DiscriminatedAuth, base_url: str) -> None:
        self.auth = auth
        self.base_url = base_url
    
    def build(self, method: HttpMethod, path: str, params: KintoneRequestParams) -> dict:
        config = {
            'method': method.value,
            'url': urljoin(self.base_url, path),
            'headers': self._build_headers(method, self.auth),
        }
        if method == HttpMethod.GET:
            url_params = {}
            for key, val in params.url_params.items():
                if type(val) is list:
                    for index, v in enumerate(val):
                        url_params[f'{key}[{index}]'] = v
                else:
                    url_params[key] = val
            config['params'] = url_params

        elif method == HttpMethod.POST:
            payload = dict(**params.data)
            config['data'] = json.dumps(payload)
        
        elif method == HttpMethod.PUT:
            payload = dict(**params.data)
            config['data'] = json.dumps(payload)

        elif method == HttpMethod.DELETE:
            payload = dict(**params.data)
            config['data'] = json.dumps(payload)
        else:
            raise RuntimeError()
        
        return config

    def _convert_data(self, data: dict) -> dict:
        return { key: { 'value': val } for key, val in data.items() }
    
    def _build_headers(self, method: HttpMethod, auth: DiscriminatedAuth) -> dict[str, str]:
        if type(auth) is ApiTokenAuth:
            api_token = auth.api_token
            if type(api_token) is not str:
                api_token = ','.join(api_token)

            headers = {
                'X-Cybozu-API-Token': api_token
            }
            if method != HttpMethod.GET:
                headers['Content-Type'] = 'application/json'

            return headers
        elif type(auth) is PasswordAuth:
            password = auth.password
            user_name = auth.user_name
            b64_pass = base64.b64encode(f'{user_name}:{password}'.encode()).decode()
            headers = {
                'X-Cybozu-Authorization':b64_pass,
                'Authorization':f'Basic {b64_pass}',
            }
            if method != HttpMethod.GET:
                headers['Content-Type'] = 'application/json'

            return headers
        else:
            raise NotImplementedError('未実装')
