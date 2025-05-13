from pydantic import Callable, ClassName, Couroutine, Any, BaseModel, Response, Awaitable
from core.logging.logging import check_post_require, log_route_creation
from typing import Final
from fastapi import APIRouter, Request, Depends
import httpx
import json
import inspect



from core.scripts.transform import (
    fast_json_process,
    parallel_data_transform,
    convert_dict_to_array,
    convert_array_to_dict
)
from core.shared.proxy_definition import ProxyRouteDefinition

method_creation = {
    "GET": lambda client, url, _headers, _params, _data: client.get(url, params=_params, headers=_headers),
    "POST": lambda client, url, _headers, _params, _data: client.post(url, params=_params, headers=_headers, json=_data),
    "PUT": lambda client, url, _headers, _params, _data: client.put(url, params=_params, headers=_headers, json=_data),
    "PATCH": lambda client, url, _headers, _params, _data: client.patch(url, params=_params, headers=_headers, json=_data),
    "DELETE": lambda client, url, _headers, _params, _data: client.delete(url, params=_params, headers=_headers)
}


class RouteFactory:
    def __init__(self, proxy) -> None:
        self.proxy = proxy
        self.router: Final[APIRouter] = APIRouter()
    
    def create_router_param(self, proxy_route_def: ProxyRouteDefinition, _callback = None) -> None:
        handler = self._create_handler_path_param(proxy_route_def.method, proxy_route_def, _callback)
        route_path = self.proxy.endpoint + proxy_route_def.route
        route_kwargs = {
                "path": route_path,
                "endpoint": handler,
                "methods": [proxy_route_def.method],
            }
        if proxy_route_def.params:
            get_params = self.get_param_dict(proxy_route_def.params)
            async def wrapper(request: Request, path_params =get_params):
                return await handler(request, **path_params)
            route_kwargs["endpoint"] = wrapper
        
        if hasattr(proxy_route_def, '_name') and proxy_route_def._name:
            route_kwargs["name"] = proxy_route_def._name

        if hasattr(proxy_route_def, '_tags') and proxy_route_def._tags:
            route_kwargs["tags"] = proxy_route_def._tags

        self.router.add_api_route(**route_kwargs)

        log_route_creation(route_path, proxy_route_def.method, message="with parameters")

        
    def create_router(self, proxy_route_def: ProxyRouteDefinition, _callback = None) -> None:
        handler = self._create_handler(proxy_route_def.method, proxy_route_def, _callback)
        route_path = self.proxy.endpoint + proxy_route_def.route
        route_kwargs = {
            "path": route_path,
            "endpoint": handler,
            "methods": [proxy_route_def.method],
        }
        if hasattr(proxy_route_def, '_name') and proxy_route_def._name:
            route_kwargs["name"] = proxy_route_def._name

        if hasattr(proxy_route_def, '_tags') and proxy_route_def._tags:
            route_kwargs["tags"] = proxy_route_def._tags

        self.router.add_api_route(**route_kwargs)
        log_route_creation(route_path, proxy_route_def.method)



    def get_param_dict(self, param_names: list[str]):
        def dependency_func(**kwargs):
            return kwargs
        dependency_func.__signature__ = inspect.Signature([

            inspect.Parameter(name, inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=str)
            for name in param_names
        ])
        return Depends(dependency_func)


    
    def _process_response_data(self, response_data):
        """Process response data with Numba optimization."""
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

    def _create_handler_path_param(self, method: str, proxy_route_def: ProxyRouteDefinition, _callback: BaseModel | None = None):
        async def handler(request: Request, **path_params: dict[str, str]):
            url = str(str(self.proxy.target_url) + proxy_route_def.url_route).format(**path_params)
            return await self.httpx_request_handle(
                url, request, method, proxy_route_def, _callback
            )
        return handler

    def _create_handler(self, method: str, proxy_route_def: ProxyRouteDefinition, _callback = None):
        async def handler(request: Request):
            url = str(str(self.proxy.target_url) + proxy_route_def.url_route)

            return await self.httpx_request_handle(
                url, request, method, proxy_route_def, _callback
            )
        return handler

    async def httpx_request_handle(self, url, request, method, proxy_def_route, _callback=None):
        async with httpx.AsyncClient(
            headers={"User-Agent": "Sisyphus-Middleware"},
            timeout=getattr(proxy_def_route, "_timeout", 30)
        ) as client:
            headers = None
            if self.proxy.header:
                headers = {k: v for k, v in request.headers.items()
                        if k.lower() not in self.proxy.header}


            # Assign the data value to the request body
            request_body = None
            params = dict(request.query_params)
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

            check_post_require(method, request_body) # Check if POST request has data
            try:
                proxy_response = await method_creation[method](
                    client,
                    url,
                    headers,
                    params,
                    request_body
                )

                processed_content = self._process_response_data(proxy_response.content)
                if _callback:
                    processed_content = _callback(processed_content)
                return processed_content,
            except httpx.RequestError as e:
                error_response = {
                    "error": f"Error proxying request: {str(e)}",
                    "status": "failed"
                }
                return json.dumps(error_response).encode("utf-8"),
