import discord
from discord_ui.embeds.greetings_embed import greetings_status_embed
import asyncio
from discord_ui.embeds.functional_embeds import AnimeEmbed
from functions.anime_functions import *

class ButtonLabels:
    STATUS = "Status"
    WELCOME = "Welcome Embed"
    EXIT = "Exit Embed"
    DM = "DM Embed"
    ANIME_DESCRIPTION = "Anime Description"
    ANIME_INFO = "Anime Info"

class ButtonColors:
    RED = discord.ButtonStyle.red
    GREEN = discord.ButtonStyle.green
    GRAY = discord.ButtonStyle.gray

class ButtonsView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        self.interaction: discord.Interaction = interaction
        super().__init__()

    async def send_buttons(self) -> None:
        await self.interaction.edit_original_response(content="", view=self)

class GreetingsButtonsView(ButtonsView):
    def __init__(self, interaction: discord.Interaction, get_embed: callable) -> None:
        self.interaction: discord.Interaction = interaction
        super().__init__(self.interaction)
        self.get_embed: callable = get_embed

    @discord.ui.button(label=ButtonLabels.STATUS, style=ButtonColors.RED)
    async def status_button(self, interaction: discord.Interaction, *args) -> None:
        await interaction.response.defer()
        status_embed: discord.Embed = await greetings_status_embed(interaction=self.interaction)
        await self.interaction.edit_original_response(embed=status_embed, view=self)

    @discord.ui.button(label=ButtonLabels.WELCOME, style=ButtonColors.GREEN)
    async def welcome_button(self, interaction: discord.Interaction, *args) -> None:
        await interaction.response.defer()
        welcome_embed: discord.Embed = await self.get_embed(interaction=self.interaction, data_type="welcome_greetings_embed")
        await self.interaction.edit_original_response(embed=welcome_embed, view=self)

    @discord.ui.button(label=ButtonLabels.EXIT, style=ButtonColors.RED)
    async def exit_button(self, interaction: discord.Interaction, *args) -> None:
        await interaction.response.defer()
        exit_embed: discord.Embed = await self.get_embed(interaction=self.interaction, data_type="exit_greetings_embed")
        await self.interaction.edit_original_response(embed=exit_embed, view=self)

    @discord.ui.button(label=ButtonLabels.DM, style=ButtonColors.GRAY)
    async def dm_button(self, interaction: discord.Interaction, *args) -> None:
        await interaction.response.defer()
        dm_embed: discord.Embed = await self.get_embed(interaction=self.interaction, data_type="dm_greetings_embed")
        await self.interaction.edit_original_response(embed=dm_embed, view=self)

class AnimeInfoButtonsView(ButtonsView):
    def __init__(self, interaction: discord.Interaction, get_embed: AnimeEmbed.search_anime_embed, anime_info: Anime) -> None:
        self.interaction: discord.Interaction = interaction
        super().__init__(self.interaction)

        self.anime_info_embed: discord.Embed = get_embed(anime_info)
        self.anime_description: str = anime_info.description 

    @discord.ui.button(label=ButtonLabels.ANIME_INFO, style=ButtonColors.GREEN)
    async def anime_info(self, interaction: discord.Interaction, *args) -> None:
        await interaction.response.defer()
        await self.interaction.edit_original_response(embed=self.anime_info_embed, view=self)

    @discord.ui.button(label=ButtonLabels.ANIME_DESCRIPTION, style=ButtonColors.GRAY)
    async def description(self, interaction: discord.Interaction, *args) -> None:
        await interaction.response.defer()
        await self.interaction.edit_original_response(content=f"📖**Description**📖\n`{self.anime_description}`", embed=None, view=self)

if __name__ == "__main__":
    pass