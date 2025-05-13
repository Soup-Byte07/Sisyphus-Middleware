
import sys
from typing import Any
from pydantic import BaseModel, HttpUrl, ValidationError, ValidatorFunctionWrapHandler, field_validator
from urllib.parse import urlparse
from custom_core.logging import exit_with_custom_message



class ProxyDefinition(BaseModel):
    endpoint: str
    target_url: HttpUrl
    header: set[str] | None = None

    @field_validator("endpoint", mode="after")
    @classmethod
    def validate_endpoint(cls, value):
        if not value.startswith("/"):
            exit_with_custom_message(f"Invalid prefix: {value}", "error")
            raise ValueError("Endpoint must start with '/'")
        return value
    
    @field_validator("target_url", mode="after")
    @classmethod
    def disallow_localhost(cls, value: str) -> str:
        parsed = urlparse(str(value))
        if parsed.hostname in {"localhost", "127.0.0.1"}:

            exit_with_custom_message(f"Localhost is not allowed! {value}", "error")
            raise ValueError("Localhost URLs are not allowed.")
        return value

class ProxyPrefixDefinition(BaseModel):
    url_prefix: str | None = None
    prefix: str | None = None
    method: str
    params: Any | None = None
    data: Any = None
    _timeout: int = 1
    _name: str | None = None
    _tags: list[str] | None  = None


    @field_validator("prefix", mode="after")
    def validate_endpoint(cls, value) -> str:
        if not value.startswith("/"):
            exit_with_custom_message(f"Invalid prefix: {value}", "error")
            sys.exit(1)
        return value
    @field_validator("method")
    def validate_method(cls, value):
        allowed = {"GET", "POST", "PUT", "DELETE", "PATCH"}
        upper_value = value.upper()
        if upper_value not in allowed:
            exit_with_custom_message(
                f"Invalid HTTP method: {value}", "error"
            )
            raise ValueError(f"Invalid HTTP method: {value}")

        return upper_value


