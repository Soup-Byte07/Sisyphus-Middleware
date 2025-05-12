"""
Tests for Numba-optimized transformation functions.
"""

import pytest
import numpy as np
import json
from core.scripts.transform import (
    fast_json_process,
    parallel_data_transform,
    convert_dict_to_array,
    convert_array_to_dict
)

def test_fast_json_process():
    """Test that fast_json_process correctly processes a numpy array."""
    # Create a sample numpy array
    test_data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    # Process the data
    result = fast_json_process(test_data)
    
    # Expected result is each value doubled (as per our implementation)
    expected = np.array([2.0, 4.0, 6.0, 8.0, 10.0])
    
    # Check results are as expected
    assert np.array_equal(result, expected)

def test_parallel_data_transform():
    """Test that parallel_data_transform correctly transforms data."""
    # Create a sample numpy array
    test_data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    # Process the data with a specific transform factor
    result = parallel_data_transform(test_data, transform_factor=1.0)
    
    # The exact result depends on the transformation in the function,
    # but we can check that we get a result of the right shape and type
    assert isinstance(result, np.ndarray)
    assert result.shape == test_data.shape
    assert not np.array_equal(result, test_data)  # Should be transformed

def test_convert_dict_to_array():
    """Test that convert_dict_to_array correctly converts a dictionary to an array."""
    # Create a sample dictionary
    test_dict = {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": "not_a_number",
    }
    
    # Convert to array
    result = convert_dict_to_array(test_dict)
    
    # Expected result should include only numeric values
    expected = np.array([1.0, 2.0, 3.0])
    
    # Check results
    assert np.array_equal(result, expected)

def test_convert_array_to_dict():
    """Test that convert_array_to_dict correctly converts an array back to dictionary."""
    # Original dictionary
    original_dict = {
        "a": 1,
        "b": 2, 
        "c": 3,
        "d": "string_value"
    }
    
    # Processed array (doubled values)
    processed_array = np.array([2.0, 4.0, 6.0])
    
    # Convert back to dictionary
    result = convert_array_to_dict(original_dict, processed_array)
    
    # Check that numeric values were updated but non-numeric remained the same
    assert result["a"] == 2.0
    assert result["b"] == 4.0
    assert result["c"] == 6.0
    assert result["d"] == "string_value"

def test_end_to_end_json_processing():
    """Test the entire JSON processing pipeline."""
    # Original JSON data
    original_data = {
        "id": 1,
        "value": 42,
        "score": 9.5,
        "name": "test",
        "active": True
    }
    
    # Convert to JSON bytes
    json_bytes = json.dumps(original_data).encode('utf-8')
    
    # Simulate the pipeline:
    # 1. Convert JSON to dict
    data_dict = json.loads(json_bytes.decode('utf-8'))
    
    # 2. Convert dict to array
    data_array = convert_dict_to_array(data_dict)
    
    # 3. Process with fast_json_process
    processed_array = fast_json_process(data_array)
    
    # 4. Convert back to dict
    processed_dict = convert_array_to_dict(data_dict, processed_array)
    
    # 5. Convert back to JSON
    processed_json = json.dumps(processed_dict).encode('utf-8')
    
    # Check results
    result_dict = json.loads(processed_json.decode('utf-8'))
    
    # Numeric values should be doubled
    assert result_dict["id"] == 2
    assert result_dict["value"] == 84
    assert result_dict["score"] == 19.0
    
    # Non-numeric values should remain unchanged
    assert result_dict["name"] == "test"
    assert result_dict["active"] is True

if __name__ == "__main__":
    # Run the tests
    pytest.main(["-xvs", __file__])