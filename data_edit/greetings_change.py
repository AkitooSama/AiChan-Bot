#Importing discord module.
import discord
#Importing local dataclass.
from data_classes.greetings import DatabaseInterface, WelcomeGreetingItems, ExitGreetingItems, DmGreetingItems
from database_helpers import save_to_db
#Importing from local (database py-mongo)
from setup import db

async def welcome_greetings_change(interaction: discord.Interaction):
    #init_db.
    collection = db[f'guild-{interaction.guild.id}']
    #setting data.
    welcome_greeting = WelcomeGreetingItems(
        main_title="🌸 Welcome to the Server! 🌸",
        description="We're absolutely thrilled to have you here! Get ready to immerse yourself in our wonderful community and make some amazing memories together. 🎉🎀✨",
        rgb_color=(255, 192, 203),
        field="🌟 Let's Start the Fun!",
        field_description="Dive into our channels and begin chatting. We can't wait to get to know you! 🎈🌸",
        footer_field="🌈 Have a fantastic time here! 🍭",
        image_url="random",
        footer_url="random"
    )
    #adding data
    DatabaseInterface.save_greeting_to_db(collection=collection, greeting=welcome_greeting, greeting_type="welcome_greetings_embed")
    
async def exit_greetings_change(interaction: discord.Interaction):
    #init_db
    collection = db[f'guild-{interaction.guild.id}']
    #setting data
    exit_greeting = ExitGreetingItems(
        main_title="🌟 Goodbye! See You Soon! 🌟",
        description="It's sad to see you leave, but remember that our doors are always open for your return. Thank you for being a part of our lovely community! 🌸✨",
        rgb_color=(94, 184, 214),
        field="💖 Until We Meet Again!",
        field_description="Remember, you're always welcome here. Take care and see you soon! 🎈🌟",
        footer_field="🌈 We'll miss you! Stay safe! 🍀",
        image_url="random",
        footer_url="random"
    )
    #adding data
    DatabaseInterface.save_greeting_to_db(collection=collection, greeting=exit_greeting, greeting_type="exit_greetings_embed")
    
async def dm_greetings_change(interaction: discord.Interaction):
    #init_db
    collection = db[f'guild-{interaction.guild.id}']
    #setting data
    dm_greeting = DmGreetingItems(
        main_title=f"🌸 Welcome to the {interaction.guild.name}! 🌸",
        description="We're absolutely thrilled to have you here! Get ready to immerse yourself in our wonderful community and make some amazing memories together. 🎉🎀✨",
        rgb_color=(255, 249, 168),
        field="🌟 Let's Start the Fun!",
        field_description="C'mon now come back to server to enjoy furthermore 💖",
        footer_field="🌈 Have a fantastic time here! 🍭",
        image_url="random",
        footer_url="random"
    )
    #adding data
    DatabaseInterface.save_greeting_to_db(collection=collection, greeting=dm_greeting, greeting_type="dm_greetings_embed")
    
async def embed_change(guild_id: int, data: dict, data_type: str):
    await save_to_db(guild_id=guild_id, data=data, data_type=data_type)
    
if __name__ == "__main__":
    pass