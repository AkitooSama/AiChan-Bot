#Importing built-in module.
from typing import TypeVar
# Importing discord module.
import discord
#Importing dataclass.
from data_classes import greetings
#Importing local modules.
from discord_ui.embeds.greetings_embed import greeting_embed
from discord_ui.views.status import GreetingsToggleView, GreetingsReminderToggleView, DMGreetingsToggleView
from database_helpers import get_specific_value_db
from data_edit.greetings_change import embed_change
from data_classes.greetings import ChannelGreetings

#Typing-Hinting
GreetingType = TypeVar("GreetingType", bound=ChannelGreetings)

class MemberActions:
    """Contains methods to acknowledge member actions in a Discord server."""

    @staticmethod
    async def member_join(member: discord.Member, channel_name: str) -> None:
        """Sends a greeting to a specified text channel when a member joins the server.

        Parameters
        ----------
        member : discord.Member
            The member who joined the server.
        channel_name : str
            The name of the text channel where the message will be sent.
        """
        channel: discord.TextChannel = discord.utils.get(member.guild.text_channels, name=channel_name)
        if channel:
            embed = await greeting_embed(member=member, greeting_type="welcome_greetings_embed", search_term="cute anime welcome", greetings_cls=greetings.WelcomeGreetingItems)
            await channel.send(content=member.mention, embed=embed)
        else:
            channel = await get_specific_value_db(member=member, key="bot_channel_name")
            await channel.send(content="`Context: Greetings Functionality is ON\nNot working: Server greetings channel is not available\nProblem: so greetings won't work properly\nWhy it happened: maybe you changed that greetings channel name or something\nSolution: please set your greeting channel again.`")
        
    @staticmethod
    async def member_remove(member: discord.Member, channel_name: str) -> None:
        """Sends a greeting to a specified text channel when a member leaves the server.

        Parameters
        ----------
        member : discord.Member
            The member who left the server.
        channel_name : str
            The name of the text channel where the message will be sent.
        """
        channel = discord.utils.get(member.guild.text_channels, name=channel_name)
        if channel:
            embed = await greeting_embed(member=member, greeting_type="exit_greetings_embed", search_term="cute anime bye exit greeting", greetings_cls=greetings.ExitGreetingItems)
            await channel.send(content=member.mention, embed=embed)
        else:
            channel = await get_specific_value_db(member=member, key="bot_channel_name")
            await channel.send(content="`Context: Greetings Functionality is ON\nNot working: Server greetings channel is not available\nProblem: so greetings won't work properly\nWhy it happened: maybe you changed that greetings channel name or something\nSolution: please set your greeting channel again.`")
        
    @staticmethod
    async def dm_greetings(member: discord.Member) -> None:
        """Sends a greeting to joined member private (DM) when a member joins the server.

        Parameters
        ----------
        member : discord.Member
            The member who joined the server.
        """
        embed = await greeting_embed(member=member, greeting_type="dm_greetings_embed", search_term="cute anime personal welcome greeting", greetings_cls=greetings.DmGreetingItems)
        await member.send(content=member.mention, embed=embed)
        

class ToggleActions:
    """Contains methods to handle toggling functionalities in a Discord server."""

    @staticmethod
    async def greetings_toggler(interaction: discord.Interaction) -> None:
        """Initiates toggling for greetings functionality via interaction.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction object initiated by a user.
        """
        view = GreetingsToggleView()
        await interaction.response.send_message(content="✨Toggle from the options below✨", view=view, delete_after=120, ephemeral=True)

    @staticmethod
    async def greetings_reminder_toggler(interaction: discord.Interaction) -> None:
        """Initiates toggling for greetings reminder functionality via interaction.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction object initiated by a user.
        """
        view = GreetingsReminderToggleView()
        await interaction.response.send_message(content="✨Toggle from the options below✨", view=view, delete_after=120, ephemeral=True)

    @staticmethod
    async def dm_greetings_toggler(interaction: discord.Interaction) -> None:
        """Initiates toggling for direct message greetings functionality via interaction.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction object initiated by a user.
        """
        view = DMGreetingsToggleView()
        await interaction.response.send_message(content="✨Toggle from the options below✨", view=view, delete_after=120, ephemeral=True)

class EmbedActions:
    """Contains methods to acknowledge changes in any embed of a Discord server."""
    
    @staticmethod
    async def get_embed(interaction: discord.Interaction, data_type: str):
        embeds = {
            "welcome_greetings_embed": await greeting_embed(member=interaction.user, greeting_type="welcome_greetings_embed", search_term="cute anime personal welcome greeting", greetings_cls=greetings.DmGreetingItems),
            "exit_greetings_embed": await greeting_embed(member=interaction.user, greeting_type="exit_greetings_embed", search_term="cute anime bye exit greeting", greetings_cls=greetings.ExitGreetingItems),
            "dm_greetings_embed": await greeting_embed(member=interaction.user, greeting_type="dm_greetings_embed", search_term="cute anime personal welcome greeting", greetings_cls=greetings.DmGreetingItems)
        }
        embed = embeds.get(data_type)
        return embed
    
    @staticmethod
    async def embed_editor(interaction: discord.Interaction, data: dict, data_type: str) -> None:
        """Creates and sends embedded messages based on user interactions.

        This method facilitates the creation and display of embedded messages triggered by user interactions.
        It takes the provided data and generates specific types of embedded messages, such as welcome greetings,
        exit messages, or direct message greetings, based on the 'data_type' parameter.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction object initiated by a user.

        data : dict
            A dictionary containing data to configure the embedded messages.

        data_type : str
            Specifies the type of embedded message to create embeds.
            Determines the specific message format and content to generate.
        """
        if not data_type == "(None) No Embed Activated.":
            await embed_change(guild_id=interaction.guild.id, data=data, data_type=data_type)
            embed = await EmbedActions.get_embed(interaction=interaction, data_type=data_type)
            await interaction.followup.send(content="✨Review the Embed✨", embed=embed)
            
if __name__ == "__main__":
    pass