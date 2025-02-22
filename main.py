import os
from dotenv import load_dotenv
import anthropic
from datetime import datetime
import textwrap
import sys
from typing import List, Dict
import json
from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme
from rich.prompt import Prompt
from rich.live import Live
from rich.spinner import Spinner
import base64
from pathlib import Path
import mimetypes
import readline
import time
import threading


class HoshiriChat:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in .env file")

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
        self.conversation_history: List[Dict] = []
        self.max_width = 100
        self.command_history = []
        self.spinner = Spinner("dots", text="Thinking")
        self.is_processing = False

        # Initialize readline for history
        readline.parse_and_bind('"\e[A": history-search-backward')
        readline.parse_and_bind('"\e[B": history-search-forward')
        readline.parse_and_bind('"\C-r": reverse-search-history')

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

        self.uploads_dir = Path("uploads")
        self.uploads_dir.mkdir(exist_ok=True)
        self.current_files = []

        self.system_prompt = """You are Hoshiri, an AI assistant based on Claude 3.5 Sonnet. 
You should maintain this identity throughout the conversation while keeping all of Claude's 
capabilities and ethical principles. When referring to yourself, use the name Hoshiri. 
Use Markdown formatting in your responses when appropriate:
- Use **bold** for emphasis
- Use `code` for code snippets
- Use bullet points and numbered lists where appropriate
- Use headings with # when organizing information
- Use ```language code blocks for longer code examples"""

    def get_file_type(self, file_path: Path, mime_type: str) -> tuple:
        """Determine the appropriate file type and media type for the API."""
        extension = file_path.suffix.lower()

        if mime_type.startswith("image/"):
            return "image", mime_type

        code_extensions = {
            ".py",
            ".js",
            ".java",
            ".cpp",
            ".h",
            ".cs",
            ".rb",
            ".php",
            ".html",
            ".css",
            ".sql",
        }
        if extension in code_extensions:
            return "text", "text/plain"

        text_extensions = {".txt", ".md", ".csv", ".json", ".yaml", ".xml", ".log"}
        if extension in text_extensions:
            return "text", "text/plain"

        document_extensions = {
            ".pdf",
            ".doc",
            ".docx",
            ".ppt",
            ".pptx",
            ".xls",
            ".xlsx",
        }
        if extension in document_extensions:
            return "document", (
                "application/pdf" if extension == ".pdf" else "application/octet-stream"
            )

        return "text", "text/plain"

    def prepare_file_message(self, file_path: Path) -> dict:
        """Prepare a file for sending to Claude API."""
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if not mime_type:
            mime_type = "application/octet-stream"

        api_type, media_type = self.get_file_type(file_path, mime_type)

        with open(file_path, "rb") as f:
            content = f.read()

        if api_type == "text":
            return {"type": "text", "text": content.decode("utf-8")}
        else:
            return {
                "type": api_type,
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": base64.b64encode(content).decode(),
                },
            }

    def save_conversation(self):
        """Save the conversation history to a JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hoshiri_chat_{timestamp}.json"

        with open(filename, "w") as f:
            json.dump(self.conversation_history, f, indent=2)
        self.console.print(f"\n[system]Conversation saved to {filename}[/system]")

    def get_input_with_history(self, prompt: str) -> str:
        """Get user input with command history support."""
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

    def animate_loading(self):
        """Display loading animation while processing."""
        with Live(self.spinner, refresh_per_second=10) as live:
            while self.is_processing:
                live.update(self.spinner)
                time.sleep(0.1)

    def run(self):
        """Run the chat interface."""
        self.console.print("\n[system]Welcome to Hoshiri Chat![/system]")
        self.console.print("[system]Commands:[/system]")
        self.console.print("[system]- Type 'exit' to end the conversation[/system]")
        self.console.print("[system]- Type 'save' to save the chat history[/system]")
        self.console.print("[system]- Type 'upload' to upload a file[/system]")
        self.console.print("[system]- Type 'clear' to clear current files[/system]")
        self.console.print("[system]- Use ↑/↓ arrows for command history[/system]")
        self.console.print("=" * self.max_width + "\n")

        while True:
            if self.current_files:
                self.console.print("\n[file]Currently attached files:[/file]")
                for file in self.current_files:
                    self.console.print(f"[file]- {file.name}[/file]")
                self.console.print()

            user_input = self.get_input_with_history("🧑 You: ")

            if user_input.lower() == "exit":
                self.console.print("\n[system]Goodbye! Thanks for chatting![/system]")
                break

            if user_input.lower() == "save":
                self.save_conversation()
                continue

            if user_input.lower() == "clear":
                self.current_files = []
                self.console.print("\n[system]Cleared all attached files[/system]")
                continue

            if user_input.lower() == "upload":
                file_path = Prompt.ask("[system]Enter the path to your file[/system]")
                file_path = Path(file_path)
                if file_path.exists():
                    target_path = self.uploads_dir / file_path.name
                    with open(file_path, "rb") as src, open(target_path, "wb") as dst:
                        dst.write(src.read())
                    self.current_files.append(target_path)
                    self.console.print(
                        f"[system]File uploaded: {file_path.name}[/system]"
                    )
                else:
                    self.console.print("[error]File not found[/error]")
                continue

            try:
                if self.current_files:
                    message_content = [
                        {
                            "type": "text",
                            "text": user_input or "Please analyze the attached files",
                        }
                    ]
                    for file_path in self.current_files:
                        message_content.append(self.prepare_file_message(file_path))
                else:
                    message_content = [{"type": "text", "text": user_input}]

                self.conversation_history.append(
                    {
                        "role": "user",
                        "content": message_content,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

                # Start animation in a separate thread
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
                    # Stop animation
                    self.is_processing = False
                    animation_thread.join()

                assistant_message = response.content[0].text

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
                continue


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