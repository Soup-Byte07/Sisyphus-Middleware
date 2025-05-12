# Sisyphus-Middleware

A modular proxy server library built with FastAPI, featuring high-performance data processing with Numba optimization and a powerful plugin system.

## Features

- Modular architecture for creating proxy servers
- Plugin system for creating custom proxy modules
- Dynamic module loading and registration
- Route factory for dynamic endpoint creation
- High-performance data processing with Numba JIT compilation
- JSON request/response optimization

## Installation

```bash
# Install with pip
pip install -e .
```

## Core Usage

```python
from fastapi import FastAPI
from core.factory.route_factory import RouteFactory
from core.shared.proxy_definition import ProxyDefinition, ProxyPrefixDefinition

app = FastAPI()

# Define your proxy endpoint
proxy_def = ProxyDefinition(
    endpoint="/proxy/test",
    target_url="https://jsonplaceholder.typicode.com"
)

# Create a factory with your proxy definition
factory = RouteFactory(proxy_def)

# Create a router with prefix and method
factory.create_router(ProxyPrefixDefinition(prefix="/item/{id}", method="GET"))

# Include the router in your FastAPI app
app.include_router(factory.router)
```

## Creating Custom Proxy Modules

Sisyphus Middleware allows you to create custom proxy modules that can be dynamically loaded and registered with the system.

### Module Structure

Create a new directory under the `mods` folder with the following structure:

```
mods/
└── your_proxy_mod/
    ├── __init__.py
    ├── your_proxy_mod.py
    └── your_proxy_mod.json (or your_proxy_mod.toml)
```

### Implementing a Custom Proxy Module

1. Create a class that inherits from `BaseProxyMod` in your main module file:

```python
from core.shared.base import BaseProxyMod
from core.shared.proxy_definition import ProxyDefinition, ProxyPrefixDefinition
from typing import List, Optional, Callable

class YourProxyMod(BaseProxyMod):
    def get_proxy_definition(self) -> ProxyDefinition:
        # You can use self.config to access configuration values
        target_url = self.config.get("target_url", "https://api.example.com")

        return ProxyDefinition(
            endpoint="/your-api",
            target_url=target_url,
            header={"user-agent"}  # Headers to exclude from forwarding
        )

    def get_routes(self) -> List[ProxyPrefixDefinition]:
        return [
            ProxyPrefixDefinition(
                prefix="/resource/{id}",
                url_prefix="/resource/{id}",
                method="GET"
            ),
            ProxyPrefixDefinition(
                prefix="/items",
                url_prefix="/items",
                method="GET"
            )
        ]

    def get_callbacks(self) -> List[Optional[Callable]]:
        def transform_resource(data):
            # Transform the response data here
            return data

        return [
            transform_resource,  # For /resource/{id}
            None                # No transformation for /items
        ]
```

2. Create a config file (JSON or TOML) with the same name as your module directory:

```json
{
    "name": "Your Proxy Module",
    "version": "1.0.0",
    "description": "A custom proxy module",
    "target_url": "https://api.example.com",
    "settings": {
        "cache_enabled": true,
        "timeout": 5000
    }
}
```

### Loading Custom Modules

In your main FastAPI application, import and use the module registration function:

```python
from fastapi import FastAPI
from mods.register_mods import register_all_mods

app = FastAPI()

# Register all available mods
loaded_mods = register_all_mods(app)
print(f"Loaded {len(loaded_mods)} mods: {', '.join(loaded_mods.keys())}")
```

## Numba Optimization

This project uses Numba for high-performance data processing:

- JIT (Just-In-Time) compilation for faster execution
- Automatic parallelization of data transformations
- Optimized JSON request/response processing

### Performance Benefits

- Faster data transformations
- Optimized numerical operations
- Efficient handling of large data payloads

## Development

### Requirements

- Python 3.11+
- FastAPI
- Numba

### Running Tests

```bash
pytest
```

## License

See the LICENSE file for details.