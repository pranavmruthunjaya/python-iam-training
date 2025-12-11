import os
import yaml
from dotenv import load_dotenv

load_dotenv()

def load_yaml_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
    
def get_env_var(name: str, default=None, required: bool=False)->str:
    value = os.getenv(name, default)
    if required and value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value