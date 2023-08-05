from typing import Optional
import os


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment value by key

    Parameters:
        key (str): environment variable name
        default (Optional[str]): default value if environment variable not found

    Returns:
        Optional[str]:Returning environment varibale value or default value
    """

    try:
        value: str = os.getenv(key, default)
        return value if value is not None else default
    except Exception as _:
        return default


def get_env_or_throw(key: str) -> str:
    """Get environment value by key

    Parameters:
        key (str): environment variable name
    Raises:
        RuntimeError: Variable name not found
    Returns:
        str:Returning environment varibale value or default value
    """

    value: str = os.environ[key]

    if value is None:
        raise Exception(f"Environment variable '{key}' not found")

    return value
