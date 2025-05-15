from pydantic import BaseModel, Field
from typing import Final, Any, Callable, Awaitable
from httpx import AsyncClient, Response, BasicAuth
from core.authentication.authentication import AuthenticationHandler




class RouteSettingTypes(BaseModel):
    RouteKwargs: dict[str, Any] = Field()

AuthenticationTypes: BasicAuth | None = None
