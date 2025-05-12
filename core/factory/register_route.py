from core.shared.proxy_definition import ProxyDefinition
from core.factory.route_factory import RouteFactory

class RegisterRoute:

    def __init__(self, ProxyDefinition: ProxyDefinition, mode_name:str):
        self.Factory = RouteFactory(ProxyDefinition)
