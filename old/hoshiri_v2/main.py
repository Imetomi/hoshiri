# main.py
from dotenv import dotenv_values
import asyncio
from anthropic import Anthropic


class Assistant:
    def __init__(self):
        config = dotenv_values(".env")
        api_key = config.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in .env file")
        self.client = Anthropic(api_key=api_key)

    async def generate_code(self, user_input: str) -> str:
        response = self.client.messages.create(
            model="claude-3-sonnet",  # Fixed model name
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Generate Python code that can handle this request: {user_input}",
                }
            ],
        )
        return response.content

    async def execute_code(self, code: str):
        try:
            # Execute in the current environment
            exec(code)
            # Access the result variable if it exists
            return locals().get("result", None)
        except Exception as e:
            return await self.handle_error(code, e)

    async def handle_error(self, failed_code: str, error: Exception) -> str:
        response = self.client.messages.create(
            model="claude-3-sonnet",  # Fixed model name
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"This code failed with error: {str(error)}\n\nCode:\n{failed_code}\n\nPlease fix it.",
                }
            ],
        )
        return await self.execute_code(response.content)

    async def process_request(self, user_input: str):
        code = await self.generate_code(user_input)
        result = await self.execute_code(code)
        return result


async def main():
    try:
        assistant = Assistant()
        while True:
            user_input = input("> ")
            if user_input.lower() in ["exit", "quit"]:
                break

            result = await assistant.process_request(user_input)
            print(result)
    except ValueError as e:
        print(f"Error: {e}")
        print("Please make sure you have a .env file with ANTHROPIC_API_KEY set")


if __name__ == "__main__":
    asyncio.run(main())
