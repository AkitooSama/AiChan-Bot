import discord
from discord.ext import commands
from custom_classes.responses import FunctionResponses

class Emo(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.app_commands.command(name="emo", description="Slash command for replying someone with emo like (hugs, welcome, thanks)")
    @discord.app_commands.describe(member="member you want to reply.")
    @discord.app_commands.describe(emo="emotion like (hugs, welcome, thanks)")
    async def _emo(self, interaction: discord.Interaction, member: discord.Member, emo: str) -> None:
        await FunctionResponses.emo_response(interaction=interaction, member=member, search_term=emo)

async def setup(client: commands.Bot) -> None:
    """Setup function to add the cog to the client."""
    await client.add_cog(Emo(client))
