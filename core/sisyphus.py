from fastapi import APIRouter, FastAPI
import uvicorn


#app.include_router(factory.router)
class Sisyphus:
    def __init__(self, port: int):

        self.app: FastAPI = FastAPI()
        self.port: int = port
    
    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)

    def register(self, route: APIRouter):
        print(route)
        self.app.include_router(route)
