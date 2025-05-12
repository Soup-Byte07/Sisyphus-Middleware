from fastapi import APIRouter, FastAPI

from core.factory.route_factory import RouteFactory
from core.shared.proxy_definition import ProxyDefinition, ProxyPrefixDefinition
from pydantic import HttpUrl, BaseModel
import uvicorn
from mods.register_mods import register_all_mods


#app.include_router(factory.router)
class Sisyphus:
    def __init__(self, port: int):

        self.app = FastAPI()
        self.port = port
    
    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)

    def register(self, route: APIRouter):
        print(route)
        self.app.include_router(route)
