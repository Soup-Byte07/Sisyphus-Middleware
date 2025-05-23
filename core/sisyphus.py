import uvicorn

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter
from core.scripts.loader import load_toml_config
from core.logging.logging import invalid_port
from core.authentication.certificate import SSLCertificateManager


class Sisyphus:
    def __init__(self):
        self.app: FastAPI = FastAPI()
        self.ssl_config = None
        self.cors_config = None
        self.config = load_toml_config("sisyphus.toml")
        self.port: int = invalid_port(int(self.config["port"]))
        


        if self.config["cors"]["use_cors"] == True:
            self.cors_config = self.config["cors"]
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=self.cors_config["allow_origin"],
                allow_credentials=self.cors_config["allow_credentials"],
                allow_methods=self.cors_config["allow_methods"],
                allow_headers=self.cors_config["allow_headers"],
            )

        
        if self.config["load_cert"]["load"] == True:
            self.ssl_config = SSLCertificateManager(self.config["load_cert"])
    
    def run(self):
        if self.config["load_cert"]["load"] == True:
            uvicorn.run(self.app, host="0.0.0.0", port=self.port, ssl_keyfile=self.ssl_config.keyfile, ssl_certfile=self.ssl_config.certfile)
        else:
            uvicorn.run(self.app, host="0.0.0.0", port=self.port) 

    def register(self, route: APIRouter):
        print(route)
        self.app.include_router(route)
