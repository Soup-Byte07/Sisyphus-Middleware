from core.shared.proxy_definition import ProxyDefinition
from core.factory.route_factory import RouteFactory

class RegisterRoute:

    def __init__(self, ProxyDefinition: ProxyDefinition, mod_name:str, mod_description:str):
        self.Factory = RouteFactory(ProxyDefinition)
        self.name = mod_name
        self.mod_description = mod_description
