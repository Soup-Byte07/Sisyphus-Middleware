from fastapi import FastAPI
from core.factory.route_factory import RouteFactory
from core.shared.proxy_definition import ProxyDefinition, ProxyPrefixDefinition
from pydantic import HttpUrl, BaseModel
import uvicorn
app = FastAPI()

@app.get("/exit")
async def exit():
    import os
    import signal
    os.kill(os.getpid(), signal.SIGINT)

@app.get("/")
async def root():
    return {"message": "Hello World"}


def nothin_lol(data):
    return { "data": "tricked nerd!", "oldData": data }

# Set up the routes
proxy_def = ProxyDefinition(
    endpoint="/proxy/test",
    target_url="http://192.168.1.157:8000/",
)


factory = RouteFactory(proxy_def)

factory.create_router(ProxyPrefixDefinition(prefix="/item", method="GET"), nothin_lol)
factory.create_router(ProxyPrefixDefinition(prefix="/bar", method="GET"), nothin_lol)


# This is how the routes are registered
app.include_router(factory.router)



from core.factory.mod_loader import ModLoader

mod_loader = ModLoader()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
