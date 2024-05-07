#Importing built-in modules.
from functools import wraps
from typing import Callable, Coroutine, Any
#Importing discord modules.
import discord
#Importing local modules.
from database_helpers import get_specific_value_db

def check_status(key: str, default_value: str = "off", alt_func: Callable[..., Coroutine[Any, Any, Any]] = None, **extra_kwargs):
    """
    Decorator to check the status of a member's key.
    If status is 'on', execute the decorated function.
    If status is not 'on', either do nothing or execute an alternative function if provided.

    Args:
    - member: Discord member object.
    - key: Key to check for the status.
    - default_value: str (optional) - Default value if the key is not found.
    - alt_func: Async/Callable - (optional) Async function to execute if status is not 'on'.
    - extra_kwargs: dict - (optional) Extra argument alt_func may need.

    Returns:
    - Wrapper function to handle the check before executing the decorated function.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            member: discord.Member = args[1]
            status = await get_specific_value_db(member=member, key=key, default_value=default_value)
            if status == "on":
                return await func(*args, **kwargs)
            elif alt_func is not None:
                if extra_kwargs:
                    return await alt_func(*args, **extra_kwargs['extra_kwargs'])
                else:
                    return await alt_func(*args, **kwargs)
            # If status is not 'on' and no alternative function provided, do nothing
        return wrapper
    return decorator

def check_reminder(key: str, content:str, status_key: str, view: discord.ui.View, default_value: str = "on"):
    """
    A decorator that checks the status of the reminder. 
    If status is 'on', execute the decorated function.
    If status is not 'on', do nothing,

    Parameters:
    - key: str - Key to check for the reminders.
    - content: str - Content to send when reminding.
    - status_key: Status str for specific functionality
    - view: discord.ui.View - The interactive UI view if the reminder status is 'on'.
    - default_value: str (optional) - Default value is set to "on".
    
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            member: discord.Member = args[1]
            reminder_status = await get_specific_value_db(member=member, key=key, default_value="on")
            print(reminder_status)
            functionality_status = await get_specific_value_db(member=member, key=status_key, default_value="off")
            print(functionality_status)
            if functionality_status == "off":
                if reminder_status == "on":
                    channel_name = await get_specific_value_db(member=member, key="bot_channel_name")
                    print(channel_name)
                    channel: discord.TextChannel = discord.utils.get(member.guild.text_channels, name=channel_name)
                    await channel.send(content=content, view=view(), delete_after=60)
                    await channel.send("*this reminder will be automatically get delete after some time", delete_after=60)
            return await func(*args, **kwargs)
        return wrapper
    return decorator

if __name__ == "__main__":
    pass