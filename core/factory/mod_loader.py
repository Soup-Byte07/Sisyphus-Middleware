import importlib.util
import sys
import os
import json
from typing import Dict, List, Any, Optional, Set
from pathlib import Path
from core.shared.base import BaseProxyMod
from fastapi import FastAPI, APIRouter

class ModLoader:
    """
    Handles the dynamic loading and registration of proxy modules.
    """
    
    def __init__(self, fast_api: FastAPI, mods_dir: str = "mods"):
        """
        Initialize the ModLoader.
        
        Args:
            fast_api: The FastAPI application instance
            mods_dir: Directory where mods are located (relative to project root)
        """
        self.fast_api = fast_api
        self.mods_dir = mods_dir
        self.loaded_mods: Dict[str, BaseProxyMod] = {}
        
    def discover_mods(self) -> List[Dict[str, Any]]:
        """
        Discover all available mods in the mods directory.
        
        Returns:
            List of mod information dictionaries with paths and metadata
        """
        mods = []
        # Skip the __pycache__ and any files starting with _ or .
        for entry in os.scandir(self.mods_dir):
            if entry.is_dir() and not entry.name.startswith(('_', '.')):
                mod_info = {
                    'name': entry.name,
                    'path': entry.path,
                    'config': None
                }
                
                # Look for config file (TOML or JSON)
                config_path = os.path.join(entry.path, f"{entry.name}.toml")
                json_config_path = os.path.join(entry.path, f"{entry.name}.json")
                
                if os.path.exists(config_path):
                    try:
                        # Try to read TOML config
                        with open(config_path, "r", encoding="utf-8") as f:
                            # Import tomllib only when needed (Python 3.11+)
                            try:
                                import tomllib
                                mod_info['config'] = tomllib.loads(f.read())
                            except ImportError:
                                # Fallback for older Python versions
                                print(f"Warning: tomllib not available, skipping TOML config for {entry.name}")
                    except Exception as e:
                        print(f"Error loading TOML config for mod {entry.name}: {str(e)}")
                        
                elif os.path.exists(json_config_path):
                    try:
                        # Try to read JSON config
                        with open(json_config_path, "r", encoding="utf-8") as f:
                            mod_info['config'] = json.load(f)
                    except Exception as e:
                        print(f"Error loading JSON config for mod {entry.name}: {str(e)}")
                
                mods.append(mod_info)
        return mods
    
    def load_mod(self, mod_info: Dict[str, Any]) -> Optional[BaseProxyMod]:
        """
        Load a single mod by its information.
        
        Args:
            mod_info: Dictionary containing mod information
            
        Returns:
            Instantiated mod or None if loading failed
        """
        mod_name = mod_info['name']
        mod_path = mod_info['path']
        
        try:
            main_module_path = os.path.join(mod_path, f"{mod_name}.py")
            if not os.path.exists(main_module_path):
                print(f"Main module file not found for mod {mod_name}")
                return None
            print(main_module_path)
            spec = importlib.util.spec_from_file_location(mod_name, main_module_path)
            if spec is None or spec.loader is None:
                print(f"Failed to create spec for mod {mod_name}")
                return None
            print(spec)
            #module = importlib.util.module_from_spec(spec)
            module = importlib.import_module(main_module_path)
            #sys.modules[mod_name] = module

            spec.loader.exec_module(module)

            print(module, "here")
            # Find the mod class (subclass of BaseProxyMod)
            mod_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                print(attr_name)
                if isinstance(attr, type) and issubclass(attr, BaseProxyMod) and attr is not BaseProxyMod:
                    mod_class = attr
                    break
                    
            if mod_class is None:
                print(f"No BaseProxyMod implementation found in {mod_name}")
                return None
                
            # Instantiate the mod class with config if available
            config = mod_info.get('config')
            if config:
                return mod_class(config)
            else:
                return mod_class()
                
        except Exception as e:
            print(f"Error loading mod {mod_name}: {str(e)}")
            return None
    
    def register_mod(self, mod: BaseProxyMod) -> None:
        """
        Register a mod's routes with the FastAPI application.
        
        Args:
            mod: The mod instance to register
        """
        router = mod.register_routes()
        self.fast_api.include_router(router)
            
    def load_and_register_all(self) -> Dict[str, BaseProxyMod]:
        """
        Discover, load and register all available mods.
        
        Returns:
            Dictionary of loaded mods by name
        """
        discovered_mods = self.discover_mods()
        loaded_mods = {}
        
        for mod_info in discovered_mods:
            mod_instance = self.load_mod(mod_info)
            if mod_instance:
                mod_name = mod_info['name']
                loaded_mods[mod_name] = mod_instance
                self.register_mod(mod_instance)
                print(f"Successfully loaded and registered mod: {mod_name}")
                
        self.loaded_mods = loaded_mods
        return loaded_mods
