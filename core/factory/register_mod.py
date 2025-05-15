from core.shared.proxy_definition import ProxyDefinition
from core.factory.route_factory import RouteFactory

mod_registry = {}

class RegisterMod:
    def __init__(self, ProxyDefinition: ProxyDefinition, mod_name: str, mod_id:str, mod_description:str):
        self.Factory: RouteFactory = RouteFactory(ProxyDefinition)
        self.name: str = mod_name
        self.id: str = mod_id
        self.description: str = mod_description

def register_mod(id: str, info) -> RegisterMod:
    mod_registry[id] = RegisterMod(
        ProxyDefinition=info["ProxyDefinition"],
        mod_name=info["mod_name"],
        mod_id=info["mod_id"],
        mod_description=info["mod_description"]
    )
    return mod_registry[id]


