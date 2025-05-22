from core.logging.logging import custom_message
from pathlib import Path
import os
import toml

def load_toml_config(config_path: str):
    try:
        custom_message(f"Loading config file: {config_path}", "info")
        with open(config_path, "r") as f:
            config = toml.load(f)
        custom_message("Config file loaded successfully.", "info")
        return config
    except FileNotFoundError:
        custom_message(f"Config file not found: {config_path}", "error")
        raise
    except toml.TomlDecodeError:
        custom_message(f"Error decoding TOML file: {config_path}", "error")
        raise

def load_local_toml_config(config_path: str):

    if not os.path.isabs(config_path):
        project_root = Path(__file__).resolve().parent.parent
        config_path = os.path.join(project_root, config_path)

    config_path = os.path.abspath(config_path)
    custom_message(f"Config path resolved to: {config_path}", "info")
    load_toml_config(config_path)

