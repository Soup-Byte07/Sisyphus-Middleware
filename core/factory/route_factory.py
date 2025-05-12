
from os import path
from typing import Final, Dict, Any
from fastapi import APIRouter, Request, Response
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
    "POST": lambda client, url, _headers, _params, _data: client.post(url, params=_params, headers=_headers, data=_data),
    "PUT": lambda client, url, _headers, _params, _data: client.put(url, params=_params, headers=_headers, data=_data),
    "DELETE": lambda client, url, _headers, _params, _data: client.delete(url, params=_params, headers=_headers)
}


class RouteFactory:
    def __init__(self, proxy) -> None:
        self.proxy = proxy
        self.router: Final[APIRouter] = APIRouter()
    
    def create_router(self, proxy_def, _callback = None) -> None:
        handler = self._create_handler(proxy_def.method, proxy_def, _callback)
        print(self.proxy.endpoint + proxy_def.prefix)
        self.router.add_api_route(
            path=self.proxy.endpoint + proxy_def.prefix,
            endpoint=handler,
            methods=[proxy_def.method],
        )
    
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
        """Process request data with Numba optimization."""
        try:
            # Parse JSON if the content is JSON
            if request_data and isinstance(request_data, bytes):
                try:
                    data_dict = json.loads(request_data.decode('utf-8'))
                    if isinstance(data_dict, dict):
                        # Convert dictionary to array for Numba processing
                        data_array = convert_dict_to_array(data_dict)
                        if len(data_array) > 0:
                            # Apply optimized processing - use parallel transform for request data
                            processed_array = parallel_data_transform(data_array)
                            # Convert back to dictionary
                            processed_dict = convert_array_to_dict(data_dict, processed_array)
                            # Return JSON bytes
                            return json.dumps(processed_dict).encode('utf-8')
                except (json.JSONDecodeError, UnicodeDecodeError):
                    pass  # Not JSON or can't decode, return original
            return request_data
        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return request_data

    def _create_handler(self, method: str, proxy_def_route,  _callback = None):
        async def handler(request: Request,  **path_params):
            url = ""
            print(self.proxy.target_url, proxy_def_route.url_prefix)
            url = str(self.proxy.target_url + proxy_def_route.url_prefix).format(**path_params)
            async with httpx.AsyncClient(headers={"User-Agent": "test-client"}) as client:
                headers = None
                if(self.proxy.header):
                    headers = {k: v for k, v in request.headers.items() if k.lower() not in self.proxy.header}
                
                params = request.query_params
                request_body = await request.body() if method in {"POST", "PUT"} else None

                if request_body and method in {"POST", "PUT"}:
                    processed_request_body = self._process_request_data(request_body)
                else:
                    processed_request_body = request_body
                params = dict(request.query_params)
                params.update(path_params)

                proxy_response = await method_creation[method](
                    client,
                    url,
                    headers,
                    params,
                    processed_request_body
                )

                processed_content = self._process_response_data(proxy_response.content)
                if(_callback):
                    processed_content = _callback(processed_content)
                print(processed_content)
                return processed_content
        return handler
