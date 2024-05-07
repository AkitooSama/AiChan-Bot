# Importing discord modules.
import discord
from discord.ext import commands
#Importing local 
from discord_helpers import message_sender
from database_helpers import get_specific_value_db, change_key_value_db
from custom_classes.actions import MemberActions, ToggleActions, EmbedActions
from decorators.permissions import requires_permission
from decorators.commands import check_status, check_reminder
from discord_ui.views.status import GreetingsReminderToggleView
from data_classes.greetings import ChannelGreetings

# Defining Greetings Class.
class GreetingCommands(commands.Cog):
    def __init__(self, client):
        self.client: discord.Client = client
    
    # Whenever user joins.
    @commands.Cog.listener()
    @check_reminder(key="greetings_reminder", status_key="greetings_status", content="🍒Reminder: Greetings Functionality is not [ON]🍒", view=GreetingsReminderToggleView)
    @check_status(key="greetings_status")
    async def on_member_join(self, member: discord.Member):
        channel_name = await get_specific_value_db(member=member, key="greetings_channel_name")
        await MemberActions.member_join(member = member, channel_name=channel_name)
        dm_greetings = await get_specific_value_db(member=member, key="dm_greetings", default_value="on")
        if dm_greetings == "on":
            await MemberActions.dm_greetings(member=member)

    # Whenever member leaves.
    @commands.Cog.listener()
    @check_reminder(key="greetings_reminder", status_key="greetings_status", content="🍒Reminder: Greetings Functionality is not [ON]🍒", view=GreetingsReminderToggleView)
    @check_status(key="greetings_status")
    async def on_member_remove(self, member: discord.Member):
        channel_name = await get_specific_value_db(member=member, key="greetings_channel_name")
        await MemberActions.member_remove(member = member, channel_name=channel_name)
    
    @discord.app_commands.command(name = "toggle_greetings", description = "Slash command for toggling the greetings functionality On or Off.")
    @discord.app_commands.describe(channel="Select greeting text-channel.")
    @requires_permission(permission="administrator")
    async def _toggle_greetings(self, interaction: discord.Interaction, channel: discord.TextChannel):
        await get_specific_value_db(member=interaction.user, key="greetings_channel_name", default_value=channel.name)
        await ToggleActions.greetings_toggler(interaction=interaction)
        
    @discord.app_commands.command(name = "toggle_greetings_reminder", description = "Slash command for toggling the greetings reminder On or Off.")
    @requires_permission(permission="administrator")
    async def _toggle_greetings_reminder(self, interaction: discord.Interaction):
        status = await get_specific_value_db(member=interaction.user, key="greetings_status", default_value="off")
        if status == "off":
            await ToggleActions.greetings_reminder_toggler(interaction=interaction)
        else: await interaction.response.send_message("Greetings Functionality is On, so can't toggle this.")
    
    @discord.app_commands.command(name = "toggle_dm_greetings", description = "Slash command for toggling the private dm greetings On or Off.")
    @requires_permission(permission="administrator")
    @check_status(key="greetings_status", alt_func=message_sender, extra_kwargs={"message":"You need to turn on Greetings Functionality first."})
    async def _toggle_dm_greetings(self, interaction: discord.Interaction):
        await ToggleActions.dm_greetings_toggler(interaction=interaction)
        
    @discord.app_commands.command(name="set_greetings_channel", description="Slash command for selecting the new greetings text-channel.")
    @discord.app_commands.describe(channel="Select new text-channel.")
    @requires_permission(permission="administrator")
    @check_status(key="greetings_status", alt_func=message_sender, extra_kwargs={"message":"You need to turn on Greetings Functionality first."})
    async def _set_greetings_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        await change_key_value_db(member=interaction.user, key="greetings_channel_name", new_value=channel.name)
        await interaction.response.send_message(embed=discord.Embed(color=discord.Colour.from_rgb(255, 167, 194)).add_field(name="",value= f"✎ **Greetings Channel ・❥・** Set to {channel.mention}✅", inline=True))

    @discord.app_commands.command(name="set_bot_channel", description="Slash command for selecting the new bot text-channel.")
    @discord.app_commands.describe(channel="Select bot text-channel.")
    @requires_permission(permission="administrator")
    async def _set_bot_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        await change_key_value_db(member=interaction.user, key="bot_channel_name", new_value=channel.name)
        await interaction.response.send_message(embed=discord.Embed(color=discord.Colour.from_rgb(255, 167, 194)).add_field(name="",value= f"✎ **{self.client.user.name} Channel ・❥・** Set to {channel.mention}✅", inline=True))
        
# Setup.
async def setup(client):
    await client.add_cog(GreetingCommands(client), guilds=[discord.Object(id=1154376568173506592)])