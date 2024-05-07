import os
import asyncio
import subprocess
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Union, List, Dict

# Discord imports
import discord
from discord.ext import commands

# Rich for colored printing
from rich import print as rich_print

# Wavelink for music
import wavelink

# MongoDB for database
from pymongo import MongoClient

# Local imports
import loader
from print_tools import print_side_by_side, print_pink_shades

# Load environment variables
load_dotenv()

# Load config data
type StrListInt = str | List[int] | int
config_data: Dict[str,StrListInt] = loader.load_config("config.json")

# MongoDB setup
db_client: MongoClient = MongoClient(host=os.getenv('MONGO_URL'))
db = db_client['Discord-Guilds']

# Player check to avoid looping checkups for login if not needed.
player: bool = True

previous_extensions: List[str] = []

# Function to print the login prompt
def print_prompt(bot: Union[discord.Client, discord.ext.commands.Bot], node: wavelink.Node) -> None:
    text1: str = """
    +-------------------------------------+
    | WE HAVE LOGGED IN AS Ai~chan ♥#8556 |
    +-------------------------------------+
    """
    text2: str = """
    +-----------------------------------------+
    | MUSIC NODE IS BUILD | NODE IS CONNECTED |
    +-----------------------------------------+
    """

    side_by_side_text: str = print_side_by_side(text1, text2)
    rich_print(side_by_side_text)
    info: str = f"BOT_INFO ===> {bot.user}\nNODE_ID ===> {node.identifier}\nBOT_VERSION ===> {config_data['BOT_VER']}\n"
    rich_print(f"[green]{info}")

# Discord client setup
intents: discord.Intents = discord.Intents.all()
client: Union[commands.Bot, discord.Client] = commands.Bot(
    debug_guilds=config_data["GUILDS"],
    command_prefix=config_data['PREFIX'],
    intents=intents,
)

# Function to start the Lavalink server
def start_lavalink_server() -> None:
    current_directory: str = os.getcwd()
    os.chdir(r"openjdk-21_windows-x64_bin\jdk-21\bin")  # Going to Lavalink Folder
    command: str = 'java -jar lavalink.jar'
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.chdir(current_directory)  # Resetting Directory
    sleep(5)

# Asynchronous function to load/reload extensions (cogs)
async def extensions_loader(reload: bool = False) -> None:
    global previous_extensions
    extensions: List[str] = loader.get_extensions(folder_end_with="Z", file_extension=".py", directory="./cogs")
    if reload:
        print("")
        for previous_extension in previous_extensions:
            await client.unload_extension(f"cogs.{previous_extension}")
    rich_print('[green]◦ cogs-loading ◦')
    for extension in extensions:
        await client.load_extension(f"cogs.{extension}")
        rich_print(f'[red]◦ cogs-{extension} loaded ◦')
    if reload:
        client.tree.copy_global_to(guild=discord.Object(id=os.getenv('TEST_SERVER_ID')))
        await client.tree.sync(guild=discord.Object(id=os.getenv('TEST_SERVER_ID')))
    rich_print('[green]◦ cogs-loaded ◦\n')
    previous_extensions = extensions

# Command to reload extensions
@client.tree.command(name="reload_cogs", description="Slash command for reloading cogs.")
async def reload_cogs(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("https://i.imgur.com/u6uh5UF.gif")
    await extensions_loader(reload=True)
    await interaction.edit_original_response(content="**RELOADED SUCCESSFULLY ✅**")

# Event: When the bot is ready
@client.event
async def on_ready() -> None:
    await client.tree.sync(guild=discord.Object(id=os.getenv('TEST_SERVER_ID')))
    try:
        await on_node()  # Log in to Node
    except Exception as e:
        print(f"oof..\n\n{e}")

# Node setup
async def on_node() -> None:
    if player:
        node: wavelink.Node = wavelink.Node(uri=os.getenv('WAVELINK_URI'), password=os.getenv('WAVELINK_PASS'))
        await wavelink.Pool.connect(client=client, nodes=[node])
        print_prompt(bot=client, node=node)

# Asynchronous function to run the bot
async def async_run_bot(ascii_bot_name: str, player_server: bool = True) -> None:
    global player
    player = player_server
    async with client:
        if player_server:
            start_lavalink_server()
        rich_print(print_pink_shades(text=ascii_bot_name))
        await extensions_loader()
        client.tree.copy_global_to(guild=discord.Object(id=os.getenv('TEST_SERVER_ID')))
        loop: asyncio.AbstractEventLoop = client.loop or asyncio.get_event_loop()
        await loop.run_in_executor(ThreadPoolExecutor(), run_bot)

# Synchronous function to actually run the bot
def run_bot() -> None:
    client.run(os.getenv('TOKEN'))

if __name__ == "__main__":
    pass