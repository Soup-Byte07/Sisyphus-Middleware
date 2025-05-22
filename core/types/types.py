from ssl import VerifyMode, CERT_REQUIRED, SSLContext

from pydantic import BaseModel, Field
from typing import Final, Any, Callable, Awaitable
from httpx import AsyncClient, Response, BasicAuth
from core.authentication.authentication import AuthenticationHandler


class RouteSettingTypes(BaseModel):
    RouteKwargs: dict[str, Any] = Field()

AuthenticationTypes: BasicAuth | None = None

class SSLConfigType(BaseModel):
    certfile: str = Field()
    keyfile: str = Field()
    check_hostname: bool = True
    load_default_certs: bool = False
    password: str | None = None

class SisyphusConfigType(BaseModel):
    server: str = Field()
    port: int = Field()
    load_cert: SSLConfigType | None = None
    route_settings: RouteSettingTypes | None = None
