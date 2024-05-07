# Importing built-in modules.
import os
from dotenv import load_dotenv
import aiohttp
import urllib.parse
from typing import Dict
import random
#Importing httpx module.
import httpx

# Loading variables from .env into the environment
load_dotenv()

# Loading configs.
api_key = os.getenv("TENOR_API_KEY")

# Gives Random TENOR GIF From Google via input.
async def tenor_random_gif(search_term: str | int, limit: int = 8) -> str:
    """
    Fetches a random GIF URL related to the provided search term from the Tenor API.

    Args:
    - search_term (str | int): The term or phrase to search for GIFs.
    - limit (int): The maximum number of GIFs to retrieve (default is 8).

    Returns:
    - str: A URL of a random GIF based on the search term. If no GIFs are found or an error occurs,
           it returns a default happy anime GIF URL.
    """
    async with httpx.AsyncClient() as client:
        url = f"https://g.tenor.com/v1/search?q={search_term}&key={api_key}&limit={limit}"
        try:
            response = await client.get(url)
            if response.status_code == 200:
                search_results = response.json()
                random_entry = random.choice(search_results.get("results", []))
                gif = random_entry.get("media", [])[0].get("gif", {}).get("url")
                return gif
        except httpx.HTTPError:
            return "https://media.tenor.com/9AkT4oAEyXUAAAAC/anime-happy-anime-excited.gif"

async def detect_anime(url: str) -> Dict[str, str]:
    """
    Detects the anime using anime scene.

    Args:
        url (str): The URL of the photo/video clip.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing details of the anime if successful, else None.
    """

    api_url = f'https://api.trace.moe/search?anilistInfo&url={urllib.parse.quote_plus(url)}'

    async with aiohttp.ClientSession() as session:
        response = await session.get(api_url)
        if response.status != 200:
            return None

        data = await response.json()
        result = data['result'][0]

        seconds = int(result['from'])
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time = f'{hours:d}:{minutes:02d}:{seconds:02d}'

        anime_info = result['anilist']['title']
        
        anime_details = {
            'time': time,
            'native_title': anime_info['native'],
            'romaji_title': anime_info['romaji'],
            'english_title': anime_info['english'],
            'episode': result['episode'],
            'image_url': result['image'],
            'similarity': f'{result["similarity"] * 100:.2f}%',
        }

        video_response = await session.get(result['video'])
        if video_response.status == 200:
            anime_details['video_content'] = await video_response.read()
        return anime_details

if __name__ == "__main__":
    pass