
from os import path
from typing import Final, Dict, Any, Callable, Optional
from fastapi import APIRouter, Request, Depends
import httpx
import numpy as np
import json
from core.scripts.transform import (
    fast_json_process,
    parallel_data_transform,
    convert_dict_to_array,
    convert_array_to_dict
)

method_creation = {
    "GET": lambda client, url, _headers, _params, _data: client.get(url, params=_params, headers=_headers),
    "POST": lambda client, url, _headers, _params, _data: client.post(url, params=_params, headers=_headers, json=_data),
    "PUT": lambda client, url, _headers, _params, _data: client.put(url, params=_params, headers=_headers, json=_data),
    "DELETE": lambda client, url, _headers, _params, _data: client.delete(url, params=_params, headers=_headers)
}


class RouteFactory:
    def __init__(self, proxy) -> None:
        self.proxy = proxy
        self.router: Final[APIRouter] = APIRouter()

    def create_router(self, proxy_def, _callback = None) -> None:
        handler = self._create_handler(proxy_def.method, proxy_def, _callback, proxy_def.params)

        # Add tags and name if provided
        route_kwargs = {
            "path": self.proxy.endpoint + proxy_def.prefix,
            "endpoint": handler,
            "methods": [proxy_def.method],
        }

        # Add optional params if provided
        if hasattr(proxy_def, '_name') and proxy_def._name:
            route_kwargs["name"] = proxy_def._name

        if hasattr(proxy_def, '_tags') and proxy_def._tags:
            route_kwargs["tags"] = proxy_def._tags

        self.router.add_api_route(**route_kwargs)

    
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

    def _create_handler(self, method: str, proxy_def_route, _callback = None, params=Depends()):
        try:
            async def handler(request: Request,params=params):
                url = str(self.proxy.target_url + proxy_def_route.url_prefix).format(**params)
                print(url)
                async with httpx.AsyncClient(
                    headers={"User-Agent": "Sisyphus-Middleware"},
                    timeout=getattr(proxy_def_route, "_timeout", 30)
                ) as client:
                    headers = None
                    if self.proxy.header:
                        headers = {k: v for k, v in request.headers.items()
                                if k.lower() not in self.proxy.header}

                    request_body = None
                    if method in {"POST", "PUT"}:
                        try:
                            request_body = await request.json()
                        except:
                            request_body = await request.body()
                            if request_body:
                                request_body = self._process_request_data(request_body)

                    params = dict(request.query_params)

                    if hasattr(proxy_def_route, "_data") and proxy_def_route._data:
                        if request_body and isinstance(request_body, dict):
                            request_body.update(proxy_def_route._data)
                        else:
                            request_body = proxy_def_route._data

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

                        response_headers = {}
                        if proxy_response.headers.get("content-type"):
                            response_headers["content-type"] = proxy_response.headers["content-type"]

                        return processed_content,
                            

                    except httpx.RequestError as e:
                        error_response = {
                            "error": f"Error proxying request: {str(e)}",
                            "status": "failed"
                        }
                        return json.dumps(error_response).encode("utf-8"),
            return handler
        except Exception as e:
            print(e)
