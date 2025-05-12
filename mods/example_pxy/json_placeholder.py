"""
Utility functions for interacting with the JSON Placeholder API.

This module provides helper functions that can be used by the
Example Proxy Module to process and transform data.
"""

import json
from typing import Dict, List, Any, Union, Optional
from datetime import datetime

def enhance_todo_item(todo_data: Dict[str, Any], module_name: str) -> Dict[str, Any]:
    """
    Enhance a todo item with additional metadata.

    Args:
        todo_data: The original todo data from JSONPlaceholder
        module_name: The name of the module processing the data

    Returns:
        Enhanced todo data with additional fields
    """
    todo_data["from_proxy"] = True
    todo_data["module"] = module_name
    todo_data["enhanced"] = True
    todo_data["processed_at"] = datetime.now().isoformat()

    # Add a completion percentage based on todo status
    if todo_data.get("completed", False):
        todo_data["progress"] = 100
    else:
        todo_data["progress"] = 0

    return todo_data

def filter_posts(posts_data: List[Dict[str, Any]],
                max_id: int = 10,
                module_name: str = "UnknownModule") -> List[Dict[str, Any]]:
    """
    Filter and enhance a list of posts.

    Args:
        posts_data: List of posts from JSONPlaceholder
        max_id: Only include posts with ID less than this value
        module_name: Name of the module processing the data

    Returns:
        Filtered and enhanced list of posts
    """
    filtered_posts = [post for post in posts_data if post.get("id", 0) < max_id]

    for post in filtered_posts:
        post["processed_by"] = module_name
        post["timestamp"] = datetime.now().isoformat()
        # Calculate a word count for the body
        if "body" in post and isinstance(post["body"], str):
            post["word_count"] = len(post["body"].split())

    return filtered_posts

def enrich_comments(comments_data: List[Dict[str, Any]], module_name: str) -> List[Dict[str, Any]]:
    """
    Enrich a list of comments with additional metadata.

    Args:
        comments_data: List of comments from JSONPlaceholder
        module_name: Name of the module processing the data

    Returns:
        Enriched list of comments with additional fields
    """
    for comment in comments_data:
        comment["processed_by"] = module_name
        comment["timestamp"] = datetime.now().isoformat()

        # Add sentiment analysis placeholder (in a real app, use NLP)
        if "body" in comment and isinstance(comment["body"], str):
            text = comment["body"].lower()
            if any(word in text for word in ["great", "good", "excellent", "like", "love"]):
                comment["sentiment"] = "positive"
            elif any(word in text for word in ["bad", "terrible", "hate", "dislike"]):
                comment["sentiment"] = "negative"
            else:
                comment["sentiment"] = "neutral"

            # Add character count
            comment["char_count"] = len(comment["body"])

    return comments_data

def process_bytes_response(data: bytes, processor_func: callable) -> bytes:
    """
    Helper function to process a bytes response using a processor function.
    
    Args:
        data: Raw bytes data from the API response
        processor_func: Function to process the parsed JSON data
        
    Returns:
        Processed data as bytes
    """
    if not isinstance(data, bytes):
        return data
        
    try:
        json_data = json.loads(data.decode('utf-8'))
        processed_data = processor_func(json_data)
        return json.dumps(processed_data).encode('utf-8')
    except Exception as e:
        print(f"Error processing response: {str(e)}")
        return data