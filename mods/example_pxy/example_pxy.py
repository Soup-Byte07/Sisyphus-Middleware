from core.scripts.out_callbacks import funny_haha_example
from core.scripts.in_callbacks import input_example

from core.shared.proxy_definition import ProxyDefinition, ProxyRouteDefinition
from core.factory.register_mod import register_mod, RegisterMod
from core.factory.route_factory import RouteFactory
from core.shared.load_toml_config import LoadedTomlConfigs
from mods.example_pxy.libs.auth.example_pxy_handle_authentication import ExamplePxyHandleAuthentication
from mods.example_pxy.callbacks.out.parse_data import str_to_json


from core.sisyphus import Sisyphus

class ExampleMod():
    def __init__(self, sisyphus: Sisyphus):

        self.id: str = "example_pxy"
        self.name: str = "Example Pxy"
        self.description: str = "An Example Proxy Mod"
        self.sisyphus: Sisyphus = sisyphus

        self.register_mod: RegisterMod = register_mod(
            self.id,
            {
                "ProxyDefinition": ProxyDefinition(endpoint="/proxy/test", target_url="https://jsonplaceholder.typicode.com"),
                "mod_name": self.name,
                "mod_id": self.id,
                "mod_description": self.description
            }
        )

        # Load toml config
        self.config = LoadedTomlConfigs(self.id).load_config("mods/example_pxy/example_pxy.toml")

        # Load authentication
        self.authentication_basic: ExamplePxyHandleAuthentication = ExamplePxyHandleAuthentication()
        # Load routes
        self.register_routes()


        self.sisyphus.register(self.get_factory().router)

    def get_factory(self) -> RouteFactory:
        return self.register_mod.Factory

    def register_routes(self):
        self.register_mod.Factory.create_router(
            ProxyRouteDefinition(route="/item", url_route="/todos", method="GET"))
        self.register_mod.Factory.create_router_param(
            ProxyRouteDefinition(route="/item/{id}", url_route="/todos/{id}", params={"id":"5"}, method="GET"))
        self.register_mod.Factory.create_router(
            ProxyRouteDefinition(route="/post", url_route="/posts", method="POST", data={"title":"test", "body":"test", "userId":1}),
            _out_callback=funny_haha_example,
            _in_callback=input_example
        )
        self.register_mod.Factory.create_router(
            ProxyRouteDefinition(route="/custom/post", url_route="/posts", method="POST")
        )
        self.register_mod.Factory.create_router_param(
            ProxyRouteDefinition(route="/patch/{id}", url_route="/patch/{id}", params={"id":5}, method="PATCH")
        )
#       To use authentication on a route that requires it. Simply just add the auth parameter to what ever route you want
#       Disclaimer: This will only just apply the Auth to the request. It will not check if the auth is valid or not
#        self.register_mod.Factory.create_router(
#            ProxyRouteDefinition(route="/custom/post", url_route="/posts",
#                 method="POST",
#                 auth=self.authentication_basic.register().create_auth_header())
#        )


