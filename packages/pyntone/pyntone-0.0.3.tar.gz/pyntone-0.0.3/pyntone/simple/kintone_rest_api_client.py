from typing import Generic, Type, Union

from pyntone.simple.client.record_client import RecordClient
from pyntone.simple.client.app_client import AppClient
from pyntone.simple.http.http_client import HttpClent
from pyntone.simple.kintone_request_config_builder import KintoneRequestConfigBuilder
from pyntone.models.auth import DiscriminatedAuth


class KintoneRestAPIClient:
    def __init__(self, domain: str, auth: DiscriminatedAuth, guest_space_id: Union[None, int, str] = None):
        url = f'https://{domain}.cybozu.com'
        
        config_builder = KintoneRequestConfigBuilder(auth=auth, base_url=url)
        http_client = HttpClent(config_builder=config_builder)
        
        self.app = AppClient(http_client=http_client, guest_space_id=guest_space_id)
        self.record = RecordClient(http_client=http_client, guest_space_id=guest_space_id)
