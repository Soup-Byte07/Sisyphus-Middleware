from abc import ABC, abstractmethod
from core.factory.route_factory import RouteFactory

class BaseProxyMod(ABC):



    @abstractmethod
    def get_routes(self) -> list[RouteFactory]:
        pass
