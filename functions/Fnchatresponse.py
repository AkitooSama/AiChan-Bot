import os
from typing import List, Dict, Literal
from dotenv import load_dotenv
import asyncio
from functions.random_media import tenor_random_gif
from openai import AsyncOpenAI

# Loading variables from .env into the environment
load_dotenv()

# Loading configs.
api_key: str = os.getenv("OPENAI_API_KEY")

class AiResponses:
    def __init__(self, api_key: str = api_key) -> None:
        self.api_key: str = api_key
        self.role: str = "system"
        self.ai: str = ""
        self.conversation: list = []
    
    def _get_conversation(self, input: str) -> List[Dict[str,str]]:
        content = input.encode(encoding="ASCII", errors="ignore").decode()
        self.conversation.append({"role": "user", "content": content})
        return self.conversation
    
    def set_ai(self, string: str, type: Literal["file", "prompt"]) -> None:
        if type == "file":
            with open(string, "r", encoding="utf-8") as file:
                self.ai = file.read()
        elif type == "prompt":
            self.ai = string

        self.conversation.append({"role": "system", "content": self.ai})

    async def get_response(self, input: str) -> str:
        conversation: List[Dict[str,str]] = self._get_conversation(input=input)

        async with AsyncOpenAI(api_key=self.api_key) as client:
            stream = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation,
                stream=True,
            )
            accumulated_chunks: str = ""
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    accumulated_chunks += chunk.choices[0].delta.content

            content = accumulated_chunks.encode(encoding="ASCII", errors="ignore").decode()
            self.conversation.append({"role": "system", "content": content})

            return accumulated_chunks

class AiGIF(AiResponses):
    def __init__(self, api_key: str = api_key) -> None:
        super().__init__(api_key)

    async def get_gif(self, search_term: str) -> str:
        search_term = await self.get_response(input=f"{search_term} anime")
        print(search_term)
        gif_link: str = await tenor_random_gif(search_term=search_term)
        return gif_link
    
class TenorAI(AiGIF):
    def __init__(self, api_key: str = api_key) -> None:
        super().__init__(api_key)
        prompt: str = "You are a search term generator for the Tenor Python GIF API, Your job is to analyze the given scenario and generate specific and relevant search terms for GIFs related to the scenario, You should provide short, descriptive phrases that capture the essence of the scenario to retrieve suitable GIFs from the API, You will return one simple and short single phrase for Tenor API Search Terms, if the input is not long and simple one word then you will just return whatever input you got."
        self.set_ai(string=prompt, type="prompt")

class AiChan(AiGIF):
    def __init__(self, api_key: str = api_key) -> None:
        super().__init__(api_key)
        path = r"D:\DISCORD BOT BUILDS\Discord Bot version-2\ai_templates\ai_chat.txt"
        self.set_ai(string=path, type="file")

async def test_func():
    ai_chan = AiChan()
    while True:
        user_message = input("Type: ")
        print(await ai_chan.get_response(input=user_message))

if __name__ == "__main__":
    asyncio.run(test_func())