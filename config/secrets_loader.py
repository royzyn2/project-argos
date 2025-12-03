import os
from dotenv import load_dotenv
import logging

# Load .env file
load_dotenv()

def get_secret(key: str, default: str = None) -> str:
    """
    Securely retrieve environment variables.
    
    Args:
        key: The name of the environment variable.
        default: The default value if not found.
        
    Returns:
        The value of the environment variable.
        
    Raises:
        ValueError: If the key is not found and no default is provided.
    """
    value = os.getenv(key, default)
    if value is None:
        error_msg = f"Secret '{key}' not found in environment variables."
        logging.error(error_msg)
        raise ValueError(error_msg)
    return value

