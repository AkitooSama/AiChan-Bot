#Importing built-in modules.
from functools import wraps
#Importing discord module.
import discord

# Decorator function to check permissions
def requires_permission(permission=None):
    """
    A decorator that checks whether the user invoking a command has a specific permission within a guild.

    Args:
    - permission (str): The required permission to execute the command.

    Returns:
    - decorator: The decorator function.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract the interaction object from the arguments
            interaction: discord.Interaction = args[1]

            # Check if the interaction's user has the required permission
            if not getattr(interaction.user.guild_permissions, permission):
                # If the permission is not present, send a message indicating the lack of permission
                await interaction.response.send_message(
                    f"You don't have the required permission ({permission}) to use this command."
                )
                return

            # If permission check passes, execute the original function
            return await func(*args, **kwargs)

        return wrapper

    return decorator

if __name__ == "__main__":
    pass