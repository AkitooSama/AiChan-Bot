import discord
from discord.ext import commands
from typing import Literal, Optional
from decorators.permissions import requires_permission
from custom_classes.responses import FunctionResponses

class Admin(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.app_commands.command(name="clear_messages", description="Slash command for clearing messages from the channel.")
    @discord.app_commands.describe(count="number of messages you want to delete.")
    @discord.app_commands.describe(oldest_first="starts cleaning messages from top.")
    @discord.app_commands.describe(reason="reason for deleting?")
    @requires_permission(permission="administrator")
    async def _clear_messages(self, interaction: discord.Interaction, count: int, oldest_first: Optional[Literal['Yes','No']], reason: Optional[str] = "No Reason") -> None:
        await FunctionResponses.clear_messages(interaction=interaction, count=count, oldest_first=oldest_first, reason=reason)

async def setup(client: commands.Bot) -> None:
    """Setup function to add the cog to the client."""
    await client.add_cog(Admin(client))
