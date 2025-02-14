from ai import process_with_ai
from script_manager import execute_script, generate_script
from utils import get_available_scripts


def is_command(user_input):
    """Determine if input is a command (task automation) or casual chat."""
    keywords = ["list", "fetch", "get", "show", "open", "run", "create", "execute"]
    return any(word in user_input.lower() for word in keywords)


def process_command(command):
    print("Thinking...")

    if is_command(command):
        available_scripts = get_available_scripts()

        if command in available_scripts:
            execute_script(command)
        else:
            script_code = process_with_ai(f"Generate a Python script for: {command}")
            script_name = generate_script(command, script_code)
            execute_script(script_name)
    else:
        # If it's not a command, process it as normal conversation
        response = process_with_ai(command)
        print(f"Hoshiri: {response}")
