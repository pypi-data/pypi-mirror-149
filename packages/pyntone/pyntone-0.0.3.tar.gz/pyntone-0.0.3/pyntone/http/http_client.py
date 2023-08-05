import json
from typing import Any

import requests
from pyntone.kintone_request_config_builder import (
    HttpMethod, KintoneRequestConfigBuilder, KintoneRequestParams)


class KintoneError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class HttpClent():
    def __init__(self, config_builder: KintoneRequestConfigBuilder) -> None:
        self.config_builder = config_builder
    
    def get(self, path: str, params: KintoneRequestParams) -> dict[str, Any]:
        config = self.config_builder.build(HttpMethod.GET, path, params)
        return self._send_request(config)

    def post(self, path: str, params: KintoneRequestParams) -> dict[str, Any]:
        config = self.config_builder.build(HttpMethod.POST, path, params)
        return self._send_request(config)

    def put(self, path: str, params: KintoneRequestParams) -> dict[str, Any]:
        config = self.config_builder.build(HttpMethod.PUT, path, params)
        return self._send_request(config)
    
    def delete(self, path: str, params: KintoneRequestParams) -> dict[str, Any]:
        config = self.config_builder.build(HttpMethod.DELETE, path, params)
        return self._send_request(config)
    
    def _send_request(self, config: dict[str, Any]) -> dict[str, Any]:
        r = requests.request(**config)
        self._is_success(r)
        return json.loads(r.text)

    def _is_success(self, response: requests.Response) -> None:
        if response.status_code != 200:
            raise KintoneError(response.text)
