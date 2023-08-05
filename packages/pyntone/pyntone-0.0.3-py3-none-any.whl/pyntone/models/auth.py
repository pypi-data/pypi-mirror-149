from typing import Union

from pydantic import BaseModel


class ApiTokenAuth(BaseModel):
    type = 'apiToken'
    api_token: Union[str, list[str]]

class PasswordAuth(BaseModel):
    type = 'password'
    user_name: str
    password: str

class SessionAuth(BaseModel):
    type = 'session'

class OAuthTokenAuth(BaseModel):
    type = 'oAuthToken'
    oauth_token: str

DiscriminatedAuth = Union[ApiTokenAuth, PasswordAuth, SessionAuth, OAuthTokenAuth]

class BasicAuth(BaseModel):
    user_name: str
    password: str
