from pydantic import BaseModel, SecretStr
from fastapi import Request, Response
from httpx import BasicAuth
from base64 import b64encode

from core.logging.logging import register_mod_lib

class AuthenticationHandler(BaseModel):
    username: str
    password: SecretStr
    
    def authenticate(self, request: Request) -> Response:
        raise NotImplementedError("Subclasses should implement this method.")


class RegisterLibAuthenticationHandler():
    auth_handler: AuthenticationHandler
    def __init__(self, username: str, password: str, mod_name: str = "", register_name: str = ""):
        self.mod_name = mod_name
        self.auth_handler = AuthenticationHandler(username=username, password=SecretStr(password))
        register_mod_lib(mod_name, register_name)



class BasicAuthenticationHandler(RegisterLibAuthenticationHandler):
    register_name: str = "BasicAuthenticationHandler"
    def create_auth_header(self) -> BasicAuth:
        return BasicAuth(self.auth_handler.username, self.auth_handler.password.get_secret_value())
    def create_raw_header(self):
        tokenized = b64encode(f"{self.auth_handler.username}:{self.auth_handler.password.get_secret_value()}".encode('utf-8')).decode("ascii")
        return f'Basic {tokenized}'
    def create_b64_header(self) -> str:
        return b64encode(f"{self.auth_handler.username}:{self.auth_handler.password.get_secret_value()}".encode('utf-8')).decode("ascii")

class BearerAuthenticationHandler(RegisterLibAuthenticationHandler):
    register_name: str = "BearerAuthenticationHandler"
    def create_auth_header(self, token: str) -> str:
        return token


