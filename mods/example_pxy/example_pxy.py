from core.shared.base import BaseProxyMod
from core.shared.proxy_definition import ProxyDefinition
from fastapi import Request, Response
import httpx

class ExampleMod(BaseProxyMod):
    def get_routes(self):


        async def handler(request: Request, id: int):
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"https://jsonplaceholder.typicode.com/todos/{id}")
                return Response(content=resp.content, media_type="application/json")

        return [
            RouteDefinition(path="/todo/item/{id}", method="GET", handler=handler)
        ]
