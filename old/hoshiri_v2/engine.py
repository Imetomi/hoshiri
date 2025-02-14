# hoshiri/engine.py
import os
import importlib
from hoshiri.registry import Registry
from hoshiri.anthropic_client import AnthropicClient


class HoshiriEngine:
    def __init__(self):
        self.registry = Registry()
        self.ai_client = AnthropicClient()

    # hoshiri/engine.py

    def handle_command(self, command: str) -> str:
        interpretation = self.ai_client.interpret_command(command)

        if interpretation.get("type") == "chat":
            return interpretation.get("response_text", "No AI response.")

        # If you want script-generation logic for other tasks, put it here.
        return "No module found."

    def generate_script(self, interpretation: dict) -> dict:
        """
        Dynamically generates a module file in hoshiri/modules/
        based on AI instructions and stores metadata in the registry.
        """
        module_name = interpretation.get("module_name", "dynamic_module")
        script_content = """def run_command(command):
            # Demo: This is a dynamically generated script
            return "Executing: " + command
        """

        filename = f"{module_name}.py"
        file_path = os.path.join("hoshiri", "modules", filename)

        with open(file_path, "w") as f:
            f.write(script_content)

        module_info = {
            "name": module_name,
            "description": "Dynamically generated module",
            "file_path": file_path,
        }
        self.registry.add_module(module_info)
        return module_info

    def execute_module(self, module_info: dict, command: str) -> str:
        """
        Imports the module and calls its 'run_command' function.
        """
        try:
            module_path = module_info["file_path"].replace("/", ".").replace(".py", "")
            mod = importlib.import_module(module_path)
            result = mod.run_command(command)
            return result
        except Exception as e:
            return f"Error executing module: {str(e)}"
