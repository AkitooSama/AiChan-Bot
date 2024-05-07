import io
from typing import Dict, List, Optional
import discord
from discord_ui.views.buttons import AnimeInfoButtonsView
from functions.anime_functions import *
from functions.random_media import detect_anime
# from discord_ui.embeds.functional_embeds import AnimeEmbed
from functions.Fnchatresponse import TenorAI

tenor = TenorAI()

class FunctionResponses:

    @staticmethod
    async def emo_response(interaction: discord.Interaction, member: discord.Member, search_term: str) -> None:
        """Reply to someone with an emotion like (hugs, welcome, thanks)"""
        await interaction.response.send_message(content="💗", ephemeral=True, delete_after=0.5)
        gif_link = await tenor.get_gif(search_term=search_term)
        embed = discord.Embed(title="", color=discord.Color.random())
        embed.add_field(name=search_term, value=member.mention)
        embed.set_image(url=gif_link)
        webhook = await interaction.channel.create_webhook(name=interaction.user.display_name)
        await webhook.send(
            content=member.mention,
            embed=embed,
            username=interaction.user.display_name,
            avatar_url=interaction.user.display_avatar
        )

        webhooks = await interaction.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()

    @staticmethod
    async def impersonate_response(interaction: discord.Interaction, member: discord.Member, message: str) -> None:
        """Impersonate a member by sending a message."""
        await interaction.response.send_message(content="✨reading the magic spell✨ uwu", ephemeral=True, delete_after=0.1)
        webhook = await interaction.channel.create_webhook(name=member.display_name)
        await webhook.send(
            str(message), username=member.display_name, avatar_url=member.display_avatar
        )

        webhooks = await interaction.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()

    # @staticmethod
    # async def anime_detector_response(interaction: discord.Interaction, media: discord.Attachment):
    #     await interaction.response.send_message("lemme remember if I watched this one (∩ ⌣̀_⌣́)...")

    #     url: str = media.proxy_url
    #     detection_details: Dict[str, str] = await detect_anime(url=url)
    #     video_bytes_io = io.BytesIO(detection_details['video_content'])
    #     video_file = discord.File(video_bytes_io, filename="anime.mp4")

    #     embed = await AnimeEmbed.detect_anime_embed(detection_details=detection_details)

    #     await interaction.edit_original_response(content=interaction.user.mention, embed=embed)
    #     await interaction.channel.send(file=video_file)

    # @staticmethod
    # async def search_anime(interaction: discord.Interaction, anime_name: str):
    #     await interaction.response.send_message(f"Searching for the **{anime_name}**...✨")

    #     anime_info: Anime = Anime(query=anime_name)
    #     buttons: AnimeInfoButtonsView = AnimeInfoButtonsView(interaction=interaction, get_embed=AnimeEmbed.search_anime_embed, anime_info=anime_info)

    #     await buttons.send_buttons()

    @staticmethod
    async def clear_messages(interaction: discord.Interaction, count: int, oldest_first: str|None, reason: str) -> None:
        if count>0:
            channel: discord.TextChannel = interaction.channel
            
            await interaction.response.send_message("Yes, Starting Deletion! 📝")
            await interaction.channel.purge(limit=count+1, oldest_first=oldest_first, reason=reason)
            
            oldest_first_bool = oldest_first.lower() == "yes" if oldest_first else False
            where = "top" if oldest_first_bool else "last"
            
            delete_embed: discord.Embed = discord.Embed(title="", color=discord.Color.red())
            delete_embed.add_field(name="📝Message Deletion", value=f"{where} {count} messages deleted, as asked by {interaction.user.mention}", inline=False)
            delete_embed.add_field(name="Reason", value=reason, inline=False)
            delete_embed.set_thumbnail(url=interaction.user.avatar.url)

            await channel.send(content=interaction.user.mention, embed=delete_embed)
        else: await interaction.response.send_message(content='Look at this dumbo asking me to delete "0" messages x-x"')