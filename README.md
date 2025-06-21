# Sisyphus-Middleware

A modular proxy server library built with FastAPI, featuring a much more easier and modular way of creating proxies.

## Features

- Modular architecture for creating proxy servers
- Plugin system for creating custom proxy modules
- Dynamic module loading and registration
- Route factory for dynamic endpoint creation
- JSON request/response optimization

## Installation

```bash
# Install with pip

source .venv/source/activate.{terminal_name}
# activate.fish

# install/update packages
uv sync

# run sisyphus
python main.py

```

## Creating Custom Proxy Modules

Sisyphus Middleware allows you to create custom proxy modules that can be dynamically loaded and registered with the system.

### Module Structure

Create a new directory under the `mods` folder with the following structure:

```
mods/
└── funny_mod/
    ├── __init__.py
    ├── funny_mod.py
    └── funny_mod.toml
```

### Implementing a Custom Proxy Module

1. Now in the funny_mod.py. We can create our Mod class:

```python

from core.shared.proxy_definition import ProxyDefinition, ProxyRouteDefinition
from core.factory.register_mod import register_mod, RegisterMod
from core.factory.route_factory import RouteFactory
from core.shared.load_toml_config import LoadedTomlConfigs
from core.sisyphus import Sisyphus

class FunnyMod():
    def __init__(self, sisyphus: Sisyphus):
        # Load toml config
        self.config = LoadedTomlConfigs(self.id).load_config("mods/funny_mod/funny_mod.toml")

        self.id: str = self.config.mod.mod_id
        self.name: str = self.config.mod.mod_name
        self.description: str = self.config.mod.mod_description
        self.sisyphus: Sisyphus = sisyphus

        self.register_mod: RegisterMod = register_mod(
            self.id,
            {
                "ProxyDefinition": ProxyDefinition(endpoint="/proxy/test", target_url="https://jsonplaceholder.typicode.com"),
                "mod_name": self.name,
                "mod_id": self.id,
                "mod_description": self.description
            }
        )

        # Load routes
        self.register_routes()
        self.sisyphus.register(self.get_factory().router)

    def get_factory(self) -> RouteFactory:
        return self.register_mod.Factory

    def register_routes(self):
        self.register_mod.Factory.create_router(
            ProxyRouteDefinition(route="/item", url_route="/todos", method="GET"))


```

2. Create a config file TOML with the same name as your module directory:

```toml


[author]
created_by = "Your-Epic-Name"
contributors = ["Your-Handsome-Github", "Example"]
created_at = "2025-05-15"

[mod]
mod_name = "Funny Mod"
mod_id = "funny_mod"
mod_description = "A very funny Mod"
mod_version = "0.1.0"
readme = "README.md"
requires-python = ">=3.11"
dependencies = []

[mod_settings]
global_timeout = 1000
```
```
```


### Loading Custom Modules

Loading a custom module is easy. In the main.py file. Simply just import the module and run the instance.

```python
from core.sisyphus import Sisyphus
from mods.example_pxy.example_pxy import ExampleMod

s = Sisyphus()

# Define your modules here.
LoadExampleMod = ExampleMod(s)

s.run()

## Development

### Requirements

- Python 3.11+
- FastAPI

## License

See the LICENSE file for details.
