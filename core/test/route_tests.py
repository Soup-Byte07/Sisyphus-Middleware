import pytest
from unittest.mock import Mock, AsyncMock
from fastapi import Request
from core.factory.route_factory import RouteFactory
from core.shared.proxy_definition import ProxyDefinition, ProxyRouteDefinition

def test_input_callback_functionality():
    """Test that input callbacks can modify request data before it hits the request"""
    
    # Test callback that modifies input
    def test_callback(input_data):
        if isinstance(input_data, dict):
            input_data["modified"] = True
            input_data["original_title"] = input_data.get("title", "")
            input_data["title"] = "Modified Title"
        return input_data
    
    # Create mock proxy definition
    proxy_def = ProxyDefinition(
        endpoint="/api",
        target_url="https://httpbin.org"
    )
    
    # Create route factory
    factory = RouteFactory(proxy_def)
    
    # Test that the callback modifies data
    test_data = {"title": "Original Title", "content": "Some content"}
    modified_data = test_callback(test_data)
    
    assert modified_data["modified"] == True
    assert modified_data["title"] == "Modified Title"
    assert modified_data["original_title"] == "Original Title"
    assert modified_data["content"] == "Some content"
    
    print("✓ Input callback modification test passed")

if __name__ == "__main__":
    test_input_callback_functionality()