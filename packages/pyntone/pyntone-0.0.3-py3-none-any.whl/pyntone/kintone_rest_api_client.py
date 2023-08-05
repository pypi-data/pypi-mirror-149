from typing import Generic, Type, Union

from pyntone.client.record_client import RecordClient
from pyntone.client.app_client import AppClient
from pyntone.http.http_client import HttpClent
from pyntone.kintone_request_config_builder import KintoneRequestConfigBuilder
from pyntone.models.auth import DiscriminatedAuth
from pyntone.models.response import RecordModelT


class KintoneRestAPIClient(Generic[RecordModelT]):
    def __init__(self, model: Type[RecordModelT], domain: str, auth: DiscriminatedAuth, default_app_id: Union[int, str, None] = None, guest_space_id: Union[None, int, str] = None):
        url = f'https://{domain}.cybozu.com'
        
        config_builder = KintoneRequestConfigBuilder(auth=auth, base_url=url)
        http_client = HttpClent(config_builder=config_builder)
        
        self.app = AppClient(model=model, http_client=http_client, default_app_id=default_app_id, guest_space_id=guest_space_id)
        self.record = RecordClient(model=model, http_client=http_client, default_app_id=default_app_id, guest_space_id=guest_space_id)
