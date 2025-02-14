# hoshiri/registry.py
import os
import json

class Registry:
    def __init__(self, registry_path="data/registry.json"):
        self.registry_path = registry_path
        self.modules = []
        self._load_registry()

    def _load_registry(self):
        if os.path.exists(self.registry_path):
            with open(self.registry_path, "r") as f:
                data = json.load(f)
                self.modules = data.get("modules", [])
        else:
            self._save_registry()

    def _save_registry(self):
        data = {
            "modules": self.modules
        }
        with open(self.registry_path, "w") as f:
            json.dump(data, f, indent=2)

    def find_compatible_module(self, interpretation: dict):
        """
        Simplified approach to module matching.
        Always returns None in this demo, forcing script generation.
        """
        return None

    def add_module(self, module_info: dict):
        self.modules.append(module_info)
        self._save_registry()
