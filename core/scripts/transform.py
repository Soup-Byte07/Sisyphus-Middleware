"""
Performance-optimized transformation functions using Numba.
These functions can be used throughout the codebase for data processing tasks.
"""

import numpy as np
from numba import jit, njit, prange

@njit
def fast_json_process(data):
    """
    Process JSON-like data with Numba optimization.
    This is a simple example that could be expanded based on specific needs.
    
    Args:
        data: Numpy array representation of data to process
        
    Returns:
        Processed data
    """
    result = np.zeros_like(data)
    for i in range(len(data)):
        result[i] = data[i] * 2  # Example operation
    return result

@jit(parallel=True)
def parallel_data_transform(data, transform_factor=1.0):
    """
    Apply a transformation to data using parallel processing.
    
    Args:
        data: Numpy array to transform
        transform_factor: Factor to apply in transformation
        
    Returns:
        Transformed data
    """
    result = np.zeros_like(data)
    n = len(data)
    
    for i in prange(n):
        # Example of a more complex transformation that benefits from parallelization
        result[i] = np.sin(data[i] * transform_factor) + np.sqrt(np.abs(data[i]))
    
    return result

@njit
def fast_header_process(headers_array):
    """
    Process HTTP headers with Numba optimization.
    
    Args:
        headers_array: Numpy array representation of headers
        
    Returns:
        Processed headers array
    """
    # Example processing - in real use, you'd adapt this to your specific needs
    result = np.zeros_like(headers_array)
    for i in range(len(headers_array)):
        if headers_array[i] > 0:  # Example condition
            result[i] = headers_array[i] + 10
        else:
            result[i] = headers_array[i]
    return result

def convert_dict_to_array(data_dict):
    """
    Convert dictionary data to numpy arrays for Numba processing.
    Numba works best with numpy arrays and primitive types.
    
    Args:
        data_dict: Dictionary data to convert
        
    Returns:
        Numpy array representation
    """
    # This is a helper function - implementation depends on your data structure
    # Example implementation:
    if not data_dict:
        return np.array([])
    
    try:
        values = [float(v) for v in data_dict.values() if isinstance(v, (int, float))]
        return np.array(values, dtype=np.float64)
    except (ValueError, TypeError):
        return np.array([])

def convert_array_to_dict(original_dict, processed_array):
    """
    Convert processed numpy array back to dictionary.
    
    Args:
        original_dict: Original dictionary to use as template
        processed_array: Numpy array with processed values
        
    Returns:
        Dictionary with processed values
    """
    # This is a helper function - implementation depends on your data structure
    # Example implementation:
    if not original_dict or len(processed_array) == 0:
        return original_dict.copy()
    
    result = original_dict.copy()
    numeric_keys = [k for k, v in original_dict.items() if isinstance(v, (int, float))]
    
    for i, key in enumerate(numeric_keys):
        if i < len(processed_array):
            result[key] = processed_array[i]
            
    return result
