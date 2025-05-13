from core.shared.base import BaseProxyMod
from core.shared.proxy_definition import ProxyDefinition, ProxyPrefixDefinition
from core.factory.register_route import RegisterRoute
from core.factory.route_factory import RouteFactory
from core.sisyphus import Sisyphus
from typing import List, Dict, Any, Optional, Callable
from .json_placeholder import enhance_todo_item, filter_posts, enrich_comments, process_bytes_response
from datetime import datetime

class ExampleMod():
    def __init__(self):
        self.name = "ExampleMod"
        self.description = "An Example Proxy Mod"
        self.register_mod = RegisterRoute(ProxyDefinition(endpoint="/proxy/test", target_url="https://jsonplaceholder.typicode.com/"), self.name, self.description)

        print("Registering " + self.name)

        self.route()

    def get_factory(self) -> RouteFactory:
        return self.register_mod.Factory

    def route(self):
        self.register_mod.Factory.create_router(
            ProxyPrefixDefinition(prefix="/item", url_prefix="todos", method="GET"))
        self.register_mod.Factory.create_router_param(
            ProxyPrefixDefinition(prefix="/item/{id}", url_prefix="todos/{id}", params={"id":"5"}, method="GET"))
        self.register_mod.Factory.create_router(
            ProxyPrefixDefinition(prefix="/post", url_prefix="posts", method="POST", params=None, data={"title":"test", "body":"test", "userId":1} )
        )
        self.register_mod.Factory.create_router(
            ProxyPrefixDefinition(prefix="/custom/post", url_prefix="posts", method="POST", params=None )
        )

