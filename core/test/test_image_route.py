import sys
import os
import asyncio
import httpx
import json
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from fastapi.responses import Response, JSONResponse

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.factory.route_factory import RouteFactory
from core.shared.proxy_definition import ProxyDefinition, ProxyRouteDefinition

# Mock server to simulate Drupal API
app = FastAPI()
test_client = TestClient(app)

@app.get("/node/person/{id}/field_profile_photo")
async def mock_profile_photo(id: str):
    """Mock endpoint that returns a JSON response with image URL"""
    # This simulates the Drupal JSON response with a URL to an image
    return JSONResponse({
        "url": f"https://example.com/images/{id}.jpg",
        "alt": "Profile photo",
        "width": 800,
        "height": 600
    })

async def test_image_route():
    # Create a test proxy definition
    test_id = "480179e8-3d98-4239-8cb1-52966c9530d3"
    
    # Setup a test server
    proxy_def = ProxyDefinition(
        endpoint="/api",
        target_url="http://localhost:8000",  # This will point to our mock server
        header=None
    )
    
    route_def = ProxyRouteDefinition(
        url_route="/node/person/{id}/field_profile_photo",
        route="/test_image/{id}",
        method="GET",
        params=["id"]
    )
    
    # Create the route factory
    factory = RouteFactory(proxy_def)
    factory.create_router_param(route_def)
    
    # Create a test app with our route
    test_app = FastAPI()
    test_app.include_router(factory.router)
    
    # Create a test client to make requests
    client = TestClient(test_app)
    
    # Test the route with the provided ID
    print(f"Testing route /api/test_image/{test_id}")
    response = client.get(f"/api/test_image/{test_id}")
    
    print(f"Response status code: {response.status_code}")
    
    # Check if it's a binary response or JSON
    content_type = response.headers.get("content-type", "")
    print(f"Response content type: {content_type}")
    
    if "image" in content_type:
        print("Received image response successfully")
    else:
        # If not an image, print the response content for debugging
        try:
            print(f"Response JSON: {response.json()}")
        except:
            print(f"Response text: {response.text[:200]}...")

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_image_route())