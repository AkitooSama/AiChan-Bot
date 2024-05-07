#Importing discord module.
import discord

async def message_sender(*args, **extra_kwargs):
    interaction: discord.Interaction = args[1]
    message: str = extra_kwargs['message']
    await interaction.response.send_message(message)
    
async def if_not_channel(member: discord.Member) -> discord.TextChannel:
    for channel in member.guild.text_channels:
        if channel.permissions_for(member.guild.me).send_messages and channel.permissions_for(member).send_messages:
            return channel
        
if __name__ == "__main__":
    pass