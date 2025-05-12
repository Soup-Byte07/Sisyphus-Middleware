from typing import Any, Callable
from pydantic import BaseModel, HttpUrl
class ProxyDefinition(BaseModel):
    endpoint: str
    target_url: str
    header: set[str] | None = None

class ProxyPrefixDefinition(BaseModel):
    url_prefix: str | None = None
    prefix: str | None = None
    method: str
    has_params: bool = False
    _data: dict[str, Any] | None = None
    _timeout: int = 1
    _name: str | None = None
    _tags: list[str] | None  = None

