from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Callable
from core.factory.route_factory import RouteFactory
from core.shared.proxy_definition import ProxyDefinition, ProxyPrefixDefinition

class BaseProxyMod(ABC):
    """
    Base class for all proxy modules.
    
    Modules should inherit from this class and implement the get_proxy_definition and
    get_routes methods to provide their proxy routes.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the proxy module.
        
        Args:
            config: Optional configuration dict (can be loaded from TOML)
        """
        self.config = config or {}
        self.name = self.__class__.__name__
        self.proxy_def = self.get_proxy_definition()
        self.route_factory = RouteFactory(self.proxy_def)
        
    @abstractmethod
    def get_proxy_definition(self) -> ProxyDefinition:
        """
        Define the proxy configuration for this module.
        
        Returns:
            ProxyDefinition object with endpoint and target_url
        """
        pass
        
    @abstractmethod
    def get_routes(self) -> List[ProxyPrefixDefinition]:
        """
        Define the routes to be exposed by this proxy module.
        
        Returns:
            List of ProxyPrefixDefinition objects with their callbacks
        """
        pass
        
    def register_routes(self):
        """
        Register all routes with the route factory.
        
        Returns:
            The configured router with all routes
        """
        routes = self.get_routes()
        callbacks = self.get_callbacks()
        
        # Map callbacks to routes if both lists have matching length
        if len(callbacks) == len(routes):
            for route, callback in zip(routes, callbacks):
                self.route_factory.create_router(route, callback)
        else:
            # If no callbacks or mismatched lists, register without callbacks
            for route in routes:
                self.route_factory.create_router(route)
                
        return self.route_factory.router
        
    def get_callbacks(self) -> List[Optional[Callable]]:
        """
        Define callbacks for each route.
        Override this method to provide custom transformations.
        
        Returns:
            List of callback functions (or None)
        """
        return [None] * len(self.get_routes())