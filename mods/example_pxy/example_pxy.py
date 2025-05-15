from core.shared.proxy_definition import ProxyDefinition, ProxyRouteDefinition
from core.factory.register_route import RegisterRoute
from core.factory.route_factory import RouteFactory

class ExampleMod():
    def __init__(self):
        self.name = "ExampleMod"
        self.description = "An Example Proxy Mod"
        self.register_mod = RegisterRoute(ProxyDefinition(endpoint="/proxy/test", target_url="https://jsonplaceholder.typicode.com"), self.name, self.description)

        print("Registering " + self.name)

        self.route()

    def get_factory(self) -> RouteFactory:
        return self.register_mod.Factory

    def route(self):
        self.register_mod.Factory.create_router(
            ProxyRouteDefinition(route="/item", url_route="/todos", method="GET"))
        self.register_mod.Factory.create_router_param(
            ProxyRouteDefinition(route="/item/{id}", url_route="/todos/{id}", params={"id":"5"}, method="GET"))
        self.register_mod.Factory.create_router(
            ProxyRouteDefinition(route="/post", url_route="/posts", method="POST", data={"title":"test", "body":"test", "userId":1} )
        )
        self.register_mod.Factory.create_router(
            ProxyRouteDefinition(route="/custom/post", url_route="/posts", method="POST")
        )
        self.register_mod.Factory.create_router_param(
            ProxyRouteDefinition(route="/patch/{id}", url_route="/patch/{id}", params={"id":5}, method="PATCH")
        )

