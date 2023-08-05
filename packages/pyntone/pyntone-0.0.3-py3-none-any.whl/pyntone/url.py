from typing import Union

def build_path(endpoint: str, guest_space_id: Union[None, int, str] = None, preview: bool = False) -> str:
    guest_path = f'/guest/{guest_space_id}' if guest_space_id is not None else ''
    preview_path = '/preview' if preview else ''
    return f'/k{guest_path}/v1{preview_path}/{endpoint}.json'