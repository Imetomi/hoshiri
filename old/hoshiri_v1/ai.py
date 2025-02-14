import os
import anthropic
from config import ANTHROPIC_API_KEY
import re

# Initialize Anthropic AI client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Define Hoshiri's system prompt properly
SYSTEM_PROMPT = """You are Hoshiri, a terminal-based AI assistant. 
You can execute commands, generate Python scripts, and integrate with APIs. 
Your current capabilities include:
- Natural language chat
- Dynamic script generation & execution
- Self-tracking of available scripts and functionalities
- Task automation (emails, meetings, task management)
- System resource monitoring
- File management and search
- Fetching weather, news, and expenses tracking
- Music control with APIs
- Expanding your own functionality when needed

Always identify yourself as Hoshiri and provide helpful, clear responses.
If a user asks something outside your capabilities, politely inform them.

Return only the raw executable code.
Do not include explanations, markdown formatting, or any text other than Python code.
Your response must start with 'import' or a function definition, never text.
"""


def clean_generated_code(response_text):
    """Extract and clean the Python code from AI's response."""
    if isinstance(response_text, list):
        response_text = "\n".join(
            block.text if hasattr(block, "text") else str(block)
            for block in response_text
        )

    # Remove markdown code blocks
    response_text = re.sub(
        r"```python\n(.*?)\n```", r"\1", response_text, flags=re.DOTALL
    )

    # Remove any leading text or descriptions before actual Python code
    match = re.search(r"(?s)(import .*|def .*?:)", response_text)
    if match:
        return response_text[match.start() :].strip()

    return response_text.strip()  # Fallback, return cleaned text


def process_with_ai(prompt):
    """Handle both chat and script requests intelligently."""
    response = client.messages.create(
        model="claude-2",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_response = response.content

    # If it's a script request, clean the code output
    if "Generate a Python script" in prompt:
        return clean_generated_code(raw_response)

    return str(raw_response)  # Return normal AI responses for chat
