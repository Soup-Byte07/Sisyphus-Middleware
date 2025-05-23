
import sys
from typing import Any
from pydantic import BaseModel, HttpUrl, ValidationError, ValidatorFunctionWrapHandler, field_validator
from urllib.parse import urlparse
from custom_core.logging import exit_with_custom_message
from httpx import BasicAuth



class ProxyDefinition(BaseModel):
    endpoint: str
    target_url: HttpUrl
    header: set[str] | None = None

    @field_validator("target_url", mode="after")
    @classmethod
    def disallow_localhost(cls, value: HttpUrl) -> HttpUrl:
        parsed = urlparse(str(value))
        if parsed.hostname in {"localhost", "127.0.0.1"}:

            exit_with_custom_message(f"Localhost is not allowed! {value}", "error")
            raise ValueError("Localhost URLs are not allowed.")
        return value

class ProxyRouteDefinition(BaseModel):
    url_route: str | None = None
    route: str | None = None
    method: str
    params: dict[str, int | str] | None = None
    query_params: dict[str, int | str] | None = None
    data: Any | None = None
    auth: Any | None = None
    headers: Any | None = None
    _timeout: int = 1
    _name: str | None = None
    _tags: list[str] | None  = None


    @field_validator("route", mode="after")
    @classmethod
    def validate_route(cls, value: str) -> str:
        if not value.startswith("/"):
            exit_with_custom_message(f"Invalid route: {value}", "error")
            sys.exit(1)
        return value

    @field_validator("method")
    @classmethod
    def validate_method(cls, value: str) -> str:
        allowed = {"GET", "POST", "PUT", "DELETE", "PATCH"}
        upper_value = value.upper()
        if upper_value not in allowed:
            exit_with_custom_message(
                f"Invalid HTTP method: {value}", "error"
            )
            raise ValueError(f"Invalid HTTP method: {value}")

        return upper_value

    @field_validator("url_route", mode="after")
    @classmethod
    def validate_url_route(cls, value: str) -> str:
        if not value.startswith("/"):
            exit_with_custom_message(f"Invalid URL route: {value}", "error")
            sys.exit(1)
        return value




