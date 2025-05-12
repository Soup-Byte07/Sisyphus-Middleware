# Sisyphus-Middleware

A modular proxy server library built with FastAPI, featuring high-performance data processing with Numba optimization.

## Features

- Modular architecture for creating proxy servers
- Route factory for dynamic endpoint creation
- High-performance data processing with Numba JIT compilation
- JSON request/response optimization

## Installation

```bash
# Install with pip
pip install -e .
```

## Usage

```python
from fastapi import FastAPI
from core.factory.route_factory import RouteFactory
from core.shared.proxy_definition import ProxyDefinition, ProxyPrefixDefinition

app = FastAPI()

# Define your proxy endpoint
proxy_def = ProxyDefinition(
    endpoint="/proxy/test",
    target_url="https://jsonplaceholder.typicode.com/todos/1"
)

# Create a factory with your proxy definition
factory = RouteFactory(proxy_def)

# Create a router with prefix and method
factory.create_router(ProxyPrefixDefinition(prefix="/item", method="GET"))

# Include the router in your FastAPI app
app.include_router(factory.router)
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