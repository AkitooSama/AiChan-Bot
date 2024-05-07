#Importing built-in module.
import asyncio
#Importing discord module.
import discord
#Importing local module.
from database_helpers import get_specific_value_db, change_key_value_db
from data_edit.greetings_change import welcome_greetings_change, exit_greetings_change, dm_greetings_change
# from data_classes import greetings

async def update_status_interaction(interaction: discord.Interaction, key: str, new_value: str, success_message: str, *async_funcs) -> None:
    await change_key_value_db(member=interaction.user, key=key, new_value=new_value)
    await interaction.response.edit_message(view=None, content=success_message, delete_after = 60)

    if async_funcs:
        await asyncio.gather(*[func(interaction=interaction) for func in async_funcs])

class GreetingsToggleView(discord.ui.View):
    """
    A custom Discord UI View representing a dropdown menu with "On" and "Off" options.

    This class creates a view containing a Select dropdown with options for toggling.
    Users can choose between "On" and "Off" options, and a message is sent when an
    option is selected. The dropdown menu disappears after a selection is made.

    Methods:
    - @discord.ui.select: Initializes the ToggleView class, creates a Select dropdown with options,
      and adds it to the view.
    - callback(): Triggered when an option is chosen, sends a message displaying the selected
      option and then disables the view, making the dropdown disappear.

    Attributes:
    - select: An instance of discord.Select representing the dropdown menu with options.
      Contains "On" and "Off" options for users to select.
    """

    # Create a select dropdown with options

    @discord.ui.select(
        placeholder="Choose the option!",
        options=[
            discord.SelectOption(label="ON ✅", value="1", description="Set the greetings command to [ON]"),
            discord.SelectOption(label="OFF ❌", value="2", description="Set the greetings command to [OFF]"),
        ]
    )
    async def callback(self, interaction: discord.Interaction, select: discord.ui.select):
        """
        Triggered when an option is chosen from the dropdown.
        Sends a message displaying the selected option and disables the view.
        """

        status_key = "greetings_status"
        status = await get_specific_value_db(member=interaction.user, key=status_key, default_value="off")

        if select.values[0] == "1":
          
          if status == "off":
            await change_key_value_db(member=interaction.user, key="greetings_reminder", new_value="off")
            await update_status_interaction(
              interaction, status_key, "on", "Greetings turned ON ✅",
              welcome_greetings_change, exit_greetings_change, dm_greetings_change
            )
            await change_key_value_db(member=interaction.user, key="activated_embeds", new_value=["welcome_greetings_embed", "exit_greetings_embed", "dm_greetings_embed"])
          else:
            await interaction.response.edit_message(view=None, content="Greetings are already turned ON :0", delete_after = 60)

        elif select.values[0] == "2":
          if status == "on":
            await change_key_value_db(member=interaction.user, key="greetings_reminder", new_value="on")
            await update_status_interaction(
              interaction=interaction, key=status_key,new_value="off",
              success_message="Greetings turned OFF ❌")
          else:
            await interaction.response.edit_message(view=None, content="Greetings are already turned OFF :0", delete_after = 60)

class GreetingsReminderToggleView(discord.ui.View):
    """
    A custom Discord UI View representing a dropdown menu with "On" and "Off" options.

    This class creates a view containing a Select dropdown with options for toggling.
    Users can choose between "On" and "Off" options, and a message is sent when an
    option is selected. The dropdown menu disappears after a selection is made.

    Methods:
    - @discord.ui.select: Initializes the ToggleView class, creates a Select dropdown with options,
      and adds it to the view.
    - callback(): Triggered when an option is chosen, sends a message displaying the selected
      option and then disables the view, making the dropdown disappear.

    Attributes:
    - select: An instance of discord.Select representing the dropdown menu with options.
      Contains "On" and "Off" options for users to select.
    """
 
    # Create a select dropdown with options
    @discord.ui.select(
        placeholder="Choose the option!",
        options=[
            discord.SelectOption(label="ON ✅", value="1", description="Turn on the reminder"),
            discord.SelectOption(label="OFF ❌", value="2", description="Turn off the reminder"),
        ]
    )
    async def callback(self, interaction: discord.Interaction, select: discord.ui.select):
        """
        Triggered when an option is chosen from the dropdown.
        Sends a message displaying the selected option and disables the view.
        """

        status = await get_specific_value_db(member=interaction.user, key="greetings_reminder", default_value="on")
        if select.values[0] == "1":
          if status == "off":
            await change_key_value_db(member=interaction.user, key="greetings_reminder", new_value="on")
            await interaction.response.edit_message(view=None, content="Reminder turned ON ✅, you will be having reminders from now", delete_after = 60)
          else:
            await interaction.response.edit_message(view=None, content="Reminder are already turned ON :0", delete_after = 60)

        if select.values[0] == "2":
          await interaction.response.edit_message(view=self, delete_after=60)
          if status == "on":
            await change_key_value_db(member=interaction.user, key="greetings_reminder", new_value="off")
            await interaction.response.edit_message(view=None, content="Reminder turned OFF ❌, you won't be having any reminders from now.", delete_after = 60)
          else:
              await interaction.response.edit_message(view=None, content="Reminder are already turned OFF :0", delete_after = 60)
              
              
class DMGreetingsToggleView(discord.ui.View):
    """
    A custom Discord UI View representing a dropdown menu with "On" and "Off" options.

    This class creates a view containing a Select dropdown with options for toggling.
    Users can choose between "On" and "Off" options, and a message is sent when an
    option is selected. The dropdown menu disappears after a selection is made.

    Methods:
    - @discord.ui.select: Initializes the ToggleView class, creates a Select dropdown with options,
      and adds it to the view.
    - callback(): Triggered when an option is chosen, sends a message displaying the selected
      option and then disables the view, making the dropdown disappear.

    Attributes:
    - select: An instance of discord.Select representing the dropdown menu with options.
      Contains "On" and "Off" options for users to select.
    """
 
    # Create a select dropdown with options
    @discord.ui.select(
        placeholder="Choose the option!",
        options=[
            discord.SelectOption(label="ON ✅", value="1", description="Turn on the private dm greetings"),
            discord.SelectOption(label="OFF ❌", value="2", description="Turn off the private dm greetings"),
        ]
    )
    async def callback(self, interaction: discord.Interaction, select: discord.ui.select):
        """
        Triggered when an option is chosen from the dropdown.
        Sends a message displaying the selected option and disables the view.
        """
        
        status = await get_specific_value_db(member=interaction.user, key="dm_greetings", default_value="on")
        if select.values[0] == "1":
          if status == "off":
            await change_key_value_db(member=interaction.user, key="dm_greetings", new_value="on")
            await interaction.response.edit_message(view=None, content="Private DM Greetings Turned ON ✅, users will get private greetings from now.", delete_after = 60)
          else:
              await interaction.response.edit_message(view=None, content="Private dm greetings are already turned ON :0", delete_after = 60)

        if select.values[0] == "2":
          if status == "on":
            await change_key_value_db(member=interaction.user, key="dm_greetings", new_value="off")
            await interaction.response.edit_message(view=None, content="Private DM Greetings Turned OFF ❌, users will not get private greetings from now.", delete_after = 60)
          else:
            await interaction.response.edit_message(view=None, content="Private dm greetings are already turned OFF :0", delete_after = 60)
            
if __name__ == "__main__":
    pass