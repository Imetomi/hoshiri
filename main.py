import os, sys, json, time, threading, readline, base64, mimetypes
from dotenv import load_dotenv
import anthropic
from datetime import datetime
from typing import List, Dict, Optional
from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme
from rich.prompt import Prompt
from rich.live import Live
from pathlib import Path


class ModuleGenerator:
    def __init__(self, client: anthropic.Anthropic, console: Console):
        self.client = client
        self.console = console
        self.modules_dir = Path("modules")
        self.modules_dir.mkdir(exist_ok=True)

    def generate_module(self, specs: dict) -> Path:
        module_name = specs["module_type"]
        module_path = self.modules_dir / f"{module_name}.py"

        code = self.get_code_from_claude(specs)

        with open(module_path, "w") as f:
            f.write(code)

        return module_path

    def get_code_from_claude(self, specs: dict) -> str:
        prompt = f"""Generate a Python module for: {specs['description']}
Requirements: {specs['requirements']}
Credentials needed: {specs['credentials_needed']}
Generate complete, production-ready code."""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
        )

        return response.content[0].text


class HoshiriChat:
    def __init__(self):
        load_dotenv()
        self.setup_directories()

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in .env file")

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
        self.conversation_history: List[Dict] = []
        self.max_width = 100
        self.command_history = []
        self.is_processing = False

        self.theme = Theme(
            {
                "user": "yellow",
                "assistant": "cyan",
                "error": "red",
                "system": "green",
                "file": "magenta",
            }
        )
        self.console = Console(theme=self.theme, width=self.max_width)

        self.capabilities = self.load_capabilities()
        self.module_generator = ModuleGenerator(self.client, self.console)

        self.uploads_dir = Path("uploads")
        self.uploads_dir.mkdir(exist_ok=True)
        self.current_files = []

        self.system_prompt = self.generate_system_prompt()

    def setup_directories(self):
        for dir_name in ["modules", "configs", "uploads"]:
            Path(dir_name).mkdir(exist_ok=True)

    def load_capabilities(self) -> dict:
        cap_file = Path("configs/capabilities.json")
        if not cap_file.exists():
            capabilities = {"modules": {}}
            self.save_capabilities(capabilities)
            return capabilities
        return json.load(open(cap_file))

    def save_capabilities(self, capabilities: dict):
        with open("configs/capabilities.json", "w") as f:
            json.dump(capabilities, f, indent=2)

    def generate_system_prompt(self) -> str:
        return f"""You are Hoshiri, an AI assistant based on Claude 3.5 Sonnet.
Current capabilities: {json.dumps(self.capabilities, indent=2)}

For each request, analyze if it requires new capabilities:
If yes, respond with JSON:
{{
    "needs_module": true,
    "module_type": "type_name",
    "requirements": ["req1", "req2"],
    "credentials_needed": ["cred1", "cred2"],
    "description": "Module purpose"
}}
If no, respond normally in chat.
Use markdown formatting appropriately."""

    def animate_loading(self):
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        i = 0
        with Live("", refresh_per_second=10) as live:
            while self.is_processing:
                live.update(f"[cyan]{frames[i]} Thinking...[/cyan]")
                i = (i + 1) % len(frames)
                time.sleep(0.1)

    def get_input_with_history(self, prompt: str) -> str:
        try:
            if self.command_history:
                readline.clear_history()
                for cmd in self.command_history:
                    readline.add_history(cmd)
            user_input = input(prompt)
            if user_input.strip():
                self.command_history.append(user_input)
            return user_input
        except (EOFError, KeyboardInterrupt):
            return "exit"

    def process_response(self, response_text: str) -> Optional[dict]:
        try:
            if response_text.startswith("{"):
                specs = json.loads(response_text)
                if specs.get("needs_module"):
                    return specs
        except json.JSONDecodeError:
            pass
        return None

    def handle_new_module(self, specs: dict):
        try:
            module_path = self.module_generator.generate_module(specs)

            self.capabilities["modules"][specs["module_type"]] = {
                "path": str(module_path),
                "requirements": specs["requirements"],
                "credentials": specs["credentials_needed"],
            }
            self.save_capabilities(self.capabilities)

            self.system_prompt = self.generate_system_prompt()

            self.console.print(
                f"\n[system]Created new module: {specs['module_type']}[/system]"
            )

            config = {}
            for cred in specs["credentials_needed"]:
                config[cred] = Prompt.ask(f"Enter {cred}")

            config_path = Path("configs") / f"{specs['module_type']}_config.json"
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)

        except Exception as e:
            self.console.print(f"[error]Failed to create module: {str(e)}[/error]")

    def prepare_file_message(self, file_path: Path) -> dict:
        mime_type = (
            mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        )
        with open(file_path, "rb") as f:
            content = f.read()
            if mime_type.startswith(("text/", "application/")):
                return {"type": "text", "text": content.decode()}
            return {
                "type": "file",
                "source": {
                    "type": "base64",
                    "media_type": mime_type,
                    "data": base64.b64encode(content).decode(),
                },
            }

    def run(self):
        self.console.print("\n[system]Welcome to Hoshiri Chat![/system]")
        self.console.print("[system]Commands: exit, save, upload, clear[/system]")
        self.console.print("[system]Use ↑/↓ arrows for history[/system]")
        self.console.print("=" * self.max_width + "\n")

        while True:
            if self.current_files:
                self.console.print("\n[file]Attached files:[/file]")
                for file in self.current_files:
                    self.console.print(f"[file]- {file.name}[/file]")
                self.console.print()

            user_input = self.get_input_with_history("🧑 You: ")

            if user_input.lower() == "exit":
                self.console.print("\n[system]Goodbye![/system]")
                break

            if user_input.lower() == "save":
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                with open(f"hoshiri_chat_{timestamp}.json", "w") as f:
                    json.dump(self.conversation_history, f, indent=2)
                self.console.print(
                    f"\n[system]Chat saved: hoshiri_chat_{timestamp}.json[/system]"
                )
                continue

            if user_input.lower() == "clear":
                self.current_files = []
                self.console.print("\n[system]Files cleared[/system]")
                continue

            if user_input.lower() == "upload":
                file_path = Path(Prompt.ask("[system]File path[/system]"))
                if file_path.exists():
                    target_path = self.uploads_dir / file_path.name
                    with open(file_path, "rb") as src, open(target_path, "wb") as dst:
                        dst.write(src.read())
                    self.current_files.append(target_path)
                    self.console.print(f"[system]Uploaded: {file_path.name}[/system]")
                else:
                    self.console.print("[error]File not found[/error]")
                continue

            try:
                message_content = [{"type": "text", "text": user_input}]
                if self.current_files:
                    for file_path in self.current_files:
                        message_content.append(self.prepare_file_message(file_path))

                self.conversation_history.append(
                    {
                        "role": "user",
                        "content": message_content,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                self.is_processing = True
                animation_thread = threading.Thread(target=self.animate_loading)
                animation_thread.start()

                try:
                    response = self.client.messages.create(
                        model=self.model,
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in self.conversation_history
                        ],
                        system=self.system_prompt,
                        max_tokens=4096,
                    )
                finally:
                    self.is_processing = False
                    animation_thread.join()

                assistant_message = response.content[0].text

                module_specs = self.process_response(assistant_message)
                if module_specs:
                    self.handle_new_module(module_specs)
                    continue

                self.conversation_history.append(
                    {
                        "role": "assistant",
                        "content": [{"type": "text", "text": assistant_message}],
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                self.console.print()
                self.console.print("[assistant]🤖 Hoshiri:[/assistant]")
                self.console.print(Markdown(assistant_message))
                self.console.print()

            except Exception as e:
                self.is_processing = False
                self.console.print(f"\n[error]❌ Error: {str(e)}[/error]\n")


def main():
    try:
        if not os.path.exists(".env"):
            with open(".env", "w") as f:
                f.write("ANTHROPIC_API_KEY=your-api-key-here")
            print("❌ Created .env file. Please add your API key to it.")
            print("File location: " + os.path.abspath(".env"))
            sys.exit(1)

        chat = HoshiriChat()
        chat.run()

    except ValueError as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please add your API key to the .env file:")
        print("ANTHROPIC_API_KEY=your-api-key-here")
        sys.exit(1)


if __name__ == "__main__":
    main()
