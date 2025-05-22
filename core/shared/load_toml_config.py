from core.logging.logging import register_mod_lib
from core.scripts.loader import load_toml_config


class LoadedTomlConfigs:
    def __init__(self, mod_name):
        register_mod_lib(mod_name, "LoadedTomlConfigs")
        self.configs = {}

    def load_config(self, config_path: str):
        if config_path not in self.configs:
            self.configs[config_path] = load_toml_config(config_path)
        return self.configs[config_path]

    def load_local_config(self, config_path: str):
        if config_path not in self.configs:
            self.configs[config_path] = load_toml_config(config_path)
        return self.configs[config_path]

