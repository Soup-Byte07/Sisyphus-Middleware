import importlib.util
from pathlib import Path
from core.shared.base import BaseProxyMod
from fastapi import FastAPI, APIRouter


class ModLoader:
    def __init__(self,  mod_path: Path, mod_name: str, fast_api: FastAPI):
        self.mod_path = mod_path
        self.mod_name = mod_name
        self.fast_api = fast_api
        
    def register(self, mod: APIRouter):
        self.fast_api.include_router(mod)


