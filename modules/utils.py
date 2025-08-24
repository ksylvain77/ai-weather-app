"""
Weather app - Utilities Module
Utility functions

This module contains utility functions for Weather app.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

def get_timestamp() -> str:
    """
    Get current timestamp in ISO format
    
    Returns:
        str: Current timestamp
    """
    return datetime.now().isoformat()

def format_response(data: Any, status: str = "success") -> Dict[str, Any]:
    """
    Format a standard API response
    
    Args:
        data: Response data
        status: Response status (default: "success")
        
    Returns:
        Dict: Formatted response
    """
    return {
        "status": status,
        "timestamp": get_timestamp(),
        "data": data
    }

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """
    Load configuration from file
    
    Args:
        config_path: Path to config file
        
    Returns:
        Dict: Configuration data
    """
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load config from {config_path}: {e}")
    
    # Return default config
    return {
        "service_name": "weather_app",
        "port": 5000,
        "debug": False
    }

def save_log(message: str, level: str = "INFO") -> None:
    """
    Save log message
    
    Args:
        message: Log message
        level: Log level (INFO, WARNING, ERROR)
    """
    timestamp = get_timestamp()
    log_entry = f"[{timestamp}] {level}: {message}"
    print(log_entry)
    
    # Optionally save to file
    try:
        with open("app.log", "a") as f:
            f.write(log_entry + "\n")
    except Exception:
        pass  # Silent fail for logging

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe filesystem operations
    
    Args:
        filename: Original filename
        
    Returns:
        str: Sanitized filename
    """
    import re
    # Remove or replace unsafe characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return sanitized.strip()
