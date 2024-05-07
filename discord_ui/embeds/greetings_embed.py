#Importing modules from discord.
import discord
#Importing local module.
from functions.random_media import tenor_random_gif
from database_helpers import get_specific_value_db
from data_classes import greetings
#Importing database.
from setup import db

type GreetingType[T] = greetings.ChannelGreetings[T]

async def greeting_embed(greeting_type: str, greetings_cls: GreetingType, search_term: str, member: discord.Member) -> discord.Embed:
    collection = db[f'guild-{member.guild.id}']
    #Data
    data = greetings.DatabaseInterface.get_greeting_from_db(collection=collection, greeting_cls=greetings_cls, greeting_type=greeting_type)
    image_url, footer_url = data.image_url, data.footer_url
    if image_url == "random": image_url = await tenor_random_gif(search_term=search_term)
    if footer_url == "random": footer_url = await tenor_random_gif(search_term=f"{search_term} 1:1")
    thumbnail_url = member.avatar.url if not data.thumbnail_url else data.thumbnail_url
    #Embed
    embed = discord.Embed(
        title=data.main_title,
        description=f"{member.mention}, {data.description}",
        color=discord.Color.from_rgb(*data.rgb_color)
    )
    
    embed.set_thumbnail(url=thumbnail_url)
    embed.set_image(url=image_url)

    embed.add_field(name=data.field, value=data.field_description)

    embed.set_footer(
        text=data.footer_field,
        icon_url=footer_url
    )
    
    return embed

async def greetings_status_embed(interaction: discord.Interaction) -> discord.Embed:
    collection = db[f'guild-{interaction.user.guild.id}']

    current_greeting_channel = await get_specific_value_db(member=interaction.user, key="greetings_channel_name")
    dm_greeting_status = await get_specific_value_db(member=interaction.user, key="dm_greetings", default_value="on")
            
    welcome_greeting_data: greetings.DatabaseInterface = greetings.DatabaseInterface.get_greeting_from_db(
        collection=collection, greeting_cls=greetings.WelcomeGreetingItems, greeting_type="welcome_greetings_embed"
        )
    exit_greeting_data: greetings.DatabaseInterface = greetings.DatabaseInterface.get_greeting_from_db(
        collection=collection, greeting_cls=greetings.ExitGreetingItems, greeting_type="exit_greetings_embed"
        )
    dm_greeting_data: greetings.DatabaseInterface = greetings.DatabaseInterface.get_greeting_from_db(
        collection=collection, greeting_cls=greetings.DmGreetingItems, greeting_type="dm_greetings_embed"
        )
    
    welcome_greeting_gif, exit_greeting_gif = welcome_greeting_data.image_url, exit_greeting_data.image_url
    welcome_greeting_title, exit_greeting_title, dm_greeting_title = welcome_greeting_data.main_title, exit_greeting_data.main_title, dm_greeting_data.main_title
    
    embed = discord.Embed(title=f"This Feature is: [ON]", color=discord.Color.random())
    embed.add_field(name=f"➊|Current Greeting Channel", value=f"```{current_greeting_channel}```", inline=False)
    embed.add_field(name="➋|Current Welcome (gif,png,jpg) URL", value=f"```{welcome_greeting_gif}```", inline=False,)
    embed.add_field(name="➌|Current Exit (gif,png,jpg) URL", value=f"```{exit_greeting_gif}```", inline=False)
    embed.add_field(name="➍|Current Welcome Head-Title", value=f"```{welcome_greeting_title}```", inline=False)
    embed.add_field(name="➎|Current Exit Head-Title", value=f"```{exit_greeting_title}```", inline=False)
    embed.add_field(name="➏|DM Greeting Status", value=f"```{dm_greeting_status.upper()}```", inline=False)
    embed.add_field(name="➐|DM Head-Title", value=f"```{dm_greeting_title}```", inline=False)

    return embed

if __name__ == "__main__":
    pass