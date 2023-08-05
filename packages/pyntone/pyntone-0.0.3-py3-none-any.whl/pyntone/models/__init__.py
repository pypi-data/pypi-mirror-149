from typing import Union
from pydantic import BaseModel

class App(BaseModel):
    app: Union[int, str]
    revision: Union[int, str]