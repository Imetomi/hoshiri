# hoshiri/anthropic_client.py

import os
from anthropic import Anthropic


class AnthropicClient:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", "YOUR_API_KEY"))

    def interpret_command(self, user_input: str) -> dict:
        # Use the "chat.completions.create" method (Messages API)
        response = self.client.chat.completions.create(
            model="claude-3.5-sonnet-20240620",  # Must be a model your account can use
            messages=[
                {"role": "system", "content": "You are Hoshiri, a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
            max_tokens_to_sample=200,
            temperature=1.0,
        )

        # The returned text is in response.completion
        text = response.completion.strip()

        return {"type": "chat", "response_text": text or "No response from Anthropic."}
