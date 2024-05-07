# Importing discord modules
import discord
from discord.ext import commands
#Importing local modules
from custom_classes.responses import FunctionResponses

class Impersonate(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.app_commands.command(name="impersonate", description="Slash command for impersonating a member.")
    @discord.app_commands.describe(member="Member you want to impersonate.")
    @discord.app_commands.describe(message="Message you want to send.")
    async def _impersonate(self, interaction: discord.Interaction, member: discord.Member, message: str) -> None:
        await FunctionResponses.impersonate_response(interaction=interaction,
                                                    member=member,
                                                    message=message)

async def setup(client: commands.Bot) -> None:
    """Setup function to add the cog to the client."""
    await client.add_cog(Impersonate(client))
