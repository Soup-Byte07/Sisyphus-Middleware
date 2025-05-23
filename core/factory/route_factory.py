from pydantic import BaseModel
from core.authentication.authentication import AuthenticationHandler
from core.logging.logging import check_post_require, log_route_creation
from typing import Final, Any, Tuple

from fastapi import APIRouter, Request, Depends, Response as FastAPIResponse
from httpx import AsyncClient, Response, Client, RequestError
from core.types.types import AuthenticationTypes

import json
import inspect
import mimetypes
from fastapi.responses import StreamingResponse



from core.scripts.transform import (
    fast_json_process,
    parallel_data_transform,
    convert_dict_to_array,
    convert_array_to_dict
)
from core.shared.proxy_definition import ProxyDefinition, ProxyRouteDefinition

method_creation  = {
    "GET": lambda client, url, _headers, _params, _data, _auth: 
        client.get(url, params=_params, headers=_headers, auth=_auth, follow_redirects=True),
    "POST": lambda client, url, _headers, _params, _data, _auth:
        client.post(url, params=_params, headers=_headers, json=_data, auth=_auth, follow_redirects=True),
    "PUT": lambda client, url, _headers, _params, _data, _auth:
        client.put(url, params=_params, headers=_headers, json=_data, auth=_auth, follow_redirects=True),
    "PATCH": lambda client, url, _headers, _params, _data, _auth:
        client.patch(url, params=_params, headers=_headers, json=_data, auth=_auth,  follow_redirects=True),
    "DELETE": lambda client, url, _headers, _params, _data, _auth:
        client.delete(url, params=_params, headers=_headers, auth=_auth, follow_redirects=True)
}


class RouteFactory:
    def __init__(self, proxy: ProxyDefinition) -> None:
        self.proxy: ProxyDefinition = proxy
        self.router: Final[APIRouter] = APIRouter()
    
    def create_router_param(self, proxy_route_def: ProxyRouteDefinition, _in_callback: Any = None, _out_callback: Any=None) -> None:
        handler = self._create_handler_path_param(proxy_route_def.method, proxy_route_def, _in_callback, _out_callback)
        route_path: str = str(self.proxy.endpoint) + str(proxy_route_def.route)
        route_kwargs = {
            "path": route_path,
            "endpoint": handler,
            "methods": [proxy_route_def.method],
            "name": None,
            "tags": None
        }
        if proxy_route_def.params:
            get_params = self.get_param_dict(proxy_route_def.params)
            async def wrapper(request: Request, path_params: Any  =get_params) -> Any:
                return await handler(request, **path_params)
            route_kwargs["endpoint"] = wrapper
        
        if hasattr(proxy_route_def, '_name') and proxy_route_def._name:
            route_kwargs["name"] = proxy_route_def._name

        if hasattr(proxy_route_def, '_tags') and proxy_route_def._tags:
            route_kwargs["tags"] = proxy_route_def._tags

        self.router.add_api_route(**route_kwargs)

        log_route_creation(route_path, proxy_route_def.method, message="with parameters")

        
    def create_router(self, proxy_route_def: ProxyRouteDefinition, _in_callback: Any =None, _out_callback: Any =None) -> None:
        handler = self._create_handler(proxy_route_def.method, proxy_route_def, _in_callback, _out_callback)
        route_path = str(self.proxy.endpoint) + str(proxy_route_def.route)
        route_kwargs = {
            "path": route_path,
            "endpoint": handler,
            "methods": [proxy_route_def.method],
            "name": None,
            "tags": None
        }
        if hasattr(proxy_route_def, '_name') and proxy_route_def._name:
            route_kwargs["name"] = proxy_route_def._name

        if hasattr(proxy_route_def, '_tags') and proxy_route_def._tags:
            route_kwargs["tags"] = proxy_route_def._tags

        self.router.add_api_route(**route_kwargs)
        log_route_creation(route_path, proxy_route_def.method)



    def get_param_dict(self, param_names: list[str]) -> Any | None:
        def dependency_func(**kwargs):
            return kwargs
        dependency_func.__signature__ = inspect.Signature([

            inspect.Parameter(name, inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=str)
            for name in param_names
        ])
        return Depends(dependency_func)


    
    def _process_response_data(self, response_data) -> bytes:
        try:
            if response_data and isinstance(response_data, bytes):
                try:
                    data_dict = json.loads(response_data.decode('utf-8'))
                    if isinstance(data_dict, dict):
                        data_array = convert_dict_to_array(data_dict)
                        if len(data_array) > 0:
                            processed_array = fast_json_process(data_array)
                            processed_dict = convert_array_to_dict(data_dict, processed_array)
                            return json.dumps(processed_dict).encode('utf-8')
                except (json.JSONDecodeError, UnicodeDecodeError):
                    pass
            return response_data
        except Exception as e:
            print(f"Error processing response: {str(e)}")
            return response_data

    def _process_request_data(self, request_data):
        try:
            if request_data and isinstance(request_data, bytes):
                try:
                    data_dict = json.loads(request_data.decode('utf-8'))
                    if isinstance(data_dict, dict):
                        data_array = convert_dict_to_array(data_dict)
                        if len(data_array) > 0:
                            processed_array = parallel_data_transform(data_array)
                            processed_dict = convert_array_to_dict(data_dict, processed_array)
                            return json.dumps(processed_dict).encode('utf-8')
                except (json.JSONDecodeError, UnicodeDecodeError):
                    pass
            return request_data
        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return request_data

    def _create_handler_path_param(self, method: str, proxy_route_def: ProxyRouteDefinition, _in_callback:BaseModel | None = None, _out_callback:BaseModel | None = None):
        async def handler(request: Request, **path_params: dict[str, str]):
            url = str(str(self.proxy.target_url) + proxy_route_def.url_route).format(**path_params)
            return await self.httpx_request_handle(
                url, request, method, proxy_route_def, _in_callback, _out_callback
            )
        return handler

    def _create_handler(self, method: str, proxy_route_def: ProxyRouteDefinition,  _in_callback:BaseModel | None = None, _out_callback:BaseModel | None = None):
        async def handler(request: Request):
            url = str(str(self.proxy.target_url) + proxy_route_def.url_route)

            return await self.httpx_request_handle(
                url, request, method, proxy_route_def, _in_callback, _out_callback
            )
        return handler

    async def httpx_request_handle(self, url: str, request: Request, method, proxy_def_route: ProxyRouteDefinition, _in_callback=None, _out_callback=None):
        async with AsyncClient(
            http2=True,
            headers={"User-Agent": "Mozilla/5.0 (compatible; ProxyBot/1.0)"},
            timeout=getattr(proxy_def_route, "_timeout", 30)
        ) as client:
            headers = None
            auth = proxy_def_route.auth
            query_params = "" # ?example=1
            params = dict(request.query_params)
            request_body = None

            if self.proxy.header:
                headers = {k: v for k, v in request.headers.items()
                        if k.lower() not in self.proxy.header}

            if hasattr(proxy_def_route, "data") and proxy_def_route.data:
                if request_body and isinstance(request_body, dict):
                    request_body.update(proxy_def_route.data)
                else:
                    request_body = proxy_def_route.data
            else:
                if method in {"POST", "PUT", "PATCH"}:
                    try:
                        request_body = await request.json()
                    except:
                        request_body = await request.body()
                        if request_body:
                            request_body = self._process_request_data(request_body)
            
            if _in_callback:
                request_body = _in_callback(request_body)
            if proxy_def_route.query_params:
                for key, value in proxy_def_route.query_params.items():
                    if key not in params:
                        params[key] = value
                    else:
                        params[key] = str(params[key]) + "," + str(value)

            check_post_require(method, request_body) # Check if POST request has data
            try:
                proxy_response = await method_creation[method](
                    client,
                    url + query_params,
                    headers,
                    params,
                    request_body,
                    auth
                )

                processed_content = self._process_response_data(proxy_response.content)
                if _out_callback:
                    processed_content = _out_callback(processed_content)
                return processed_content,
            except RequestError as e:
                error_response = {
                    "error": f"Error proxying request: {str(e)}",
                    "status": "failed"
                }
                return json.dumps(error_response).encode("utf-8"),
