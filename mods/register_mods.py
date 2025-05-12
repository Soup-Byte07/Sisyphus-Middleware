from fastapi import FastAPI
from core.factory.mod_loader import ModLoader

def register_all_mods(app: FastAPI, mods_dir: str = "mods") -> dict:
    
    


    mod_loader = ModLoader(app, mods_dir)
    return mod_loader.load_and_register_all()
