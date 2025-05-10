from fastapi import FastAPI, Depends
from functools import lru_cache

from typing_extensions import Annotated

# Set env file
import sisyphus_env

@lru_cache
def get_settings():
    return sisyphus_env.SisyphusSettings()

app = FastAPI(title="Sisyphus Middleware API", version="0.1.0");


# Load paths
from routers import frontend
app.include_router(frontend.router)


@app.get("/")
def read_root(settings: Annotated[sisyphus_env.SisyphusSettings, Depends(get_settings)]):
    print(settings)
    return { "MiddlewareName": settings.app_name, "Version": settings.version }

def main():
    print("Hello from sisyphus-middleware!")


if __name__ == "__main__":
    main()
