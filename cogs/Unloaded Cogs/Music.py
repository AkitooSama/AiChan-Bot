import discord
from discord.ext import commands, tasks
import wavelink
from random import randint
from discord.app_commands import Choice
import os
import pylrc
from typing import Literal
import syncedlyrics
import asyncio
from functions.Fnreplacetext import replace_word_txt

class MusicBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.guild_info = {}

    def get_guild_info(self, guild_id):
        return self.guild_info.setdefault(guild_id, {
            'vc': None,
            'task': None,
            'task2': None,
            'message': None,
            'colorembed': None,
            'path': None,
            'title': None,
            'thumbnail': None
        })

    def load_lyrics_lrc(self, name):
        num = randint(123232, 99999999)
        filepath = f"{num}.lrc"
        matter = syncedlyrics.search(name)

        if matter is not None:
            with open(filepath, 'w', encoding='utf-8') as fil:
                fil.write(matter)

            with open(filepath, 'r', encoding='utf-8') as lrc_file:
                lrc_data = lrc_file.read()
                lrc = pylrc.parse(lrc_data)
                return lrc, filepath

        filepath = r"D:\Discord Bot version-1\lyricsnotfound.lrc"
        with open(filepath, 'r', encoding='utf-8') as lrc_file:
            lrc_data = lrc_file.read()
            lrc = pylrc.parse(lrc_data)
            return lrc, filepath

    async def fruit_autocomplete(
        interaction: discord.Interaction, current: str):
        fruits = ['Banana', 'Pineapple', 'Apple', 'Watermelon', 'Melon', 'Cherry']
        return [
            discord.app_commands.Choice(name=fruit, value=fruit)
            for fruit in fruits if current.lower() in fruit.lower()
        ]

    async def autocomplete_name(self):
        name = self.options["name"] or "english pop songs latest"
        tracks = await wavelink.YouTubeTrack.search(name)
        song = [track.title for track in tracks]
        return song[:6]
    
    @discord.app_commands.command(name="play",description="plays song")        
    async def play(self, interaction: discord.Interaction, song_name: str):
        await interaction.response.defer()
        print("yolo")
        guild_info = self.get_guild_info(interaction.guild.id)
        if guild_info['task'] and guild_info['task2']:
            print("Yo!")
            if guild_info['vc'].playing:
                await guild_info['vc'].stop()
            guild_info['task'].cancel()
            guild_info['task'] = None
            guild_info['task2'].cancel()
            guild_info['task2'] = None
            guild_info['colorembed'].stop()
            guild_info['colorembed'] = None
            try:
                os.remove(guild_info['path'])
            except:pass
        try:
            vc: wavelink.Player= await interaction.user.voice.channel.connect(cls=wavelink.Player)
            guild_info['vc'] = vc
        except: pass
        if guild_info['vc'].playing:
            await guild_info['vc'].stop()
        print("hohasjis")
        tracks = await wavelink.Playable.search(song_name, source=wavelink.TrackSource.YouTubeMusic)
        if not tracks:
            await interaction.followup.send(f'No tracks found with query: `{song_name}`')
            return

        track = tracks[0]

        guild_info['task'] = self.client.loop.create_task(self.karoakely(track=track, vc=vc, interaction=interaction))
    async def karoakely(self, track, vc, interaction: discord.Interaction):
        guild_info = self.get_guild_info(guild_id=interaction.guild.id)
        try:
            tracs = await wavelink.Playable.search(track.title, source=wavelink.TrackSource.YouTubeMusic)
            tp: wavelink.Playable = tracs[0]
            trk = f"{tp.author} - {tp.title}"
            #replace_word_txt(filepath=r'D:\Discord Bot 2023\prompts\prompt_chat_ai_chan.txt', search_text="nothing", replace_text=tp.title)
            print(trk)
            lyrics, filepath = self.load_lyrics_lrc(trk)
            a = True
            first_time = lyrics[0].time
            for lyric_line, lyric_line2 in zip(lyrics, lyrics[1:]):
                seconds = lyric_line.time - first_time
                line = lyric_line.text
                if a:
                    a = False
                    await interaction.followup.send("Playing...🎵")
                    await vc.play(track)
                    print(line)
                    message = await interaction.followup.send(embed=discord.Embed(color=discord.Color.random()).add_field(
                        name="",
                        value=f"💿 **Playing ・❥・** {track.title} ✅",
                        inline=True
                    ).set_thumbnail(url=tp.artwork))
                    guild_info['message'] = message
                    guild_info['title'] = track
                    guild_info['vc'] = vc
                    guild_info['thumbnail'] = tp.artwork
                    guild_info['path'] = filepath
                    guild_info['task2'] = self.client.loop.create_task(self.startcolor(interaction=interaction))
                    await asyncio.sleep(first_time)
                    #guild_info['title'] = f"{track}\n- ***{line}*** 🎤\n-{lyric_line2.text}"
                    guild_info['title'] = f"{track}\n```diff\n-{line} 🎤\n```\n-{lyric_line2.text}"
                else:
                    await asyncio.sleep(seconds)
                    if not seconds<1.6:
                        guild_info['title'] = f"{track}\n- ***{line}*** 🎤\n-{lyric_line2.text}"
                    else:
                        guild_info['title'] = f"{track}\n```diff\n-{line} 🎤\n```\n-{lyric_line2.text}"
                first_time = lyric_line.time
        except asyncio.CancelledError:
            pass

    async def startcolor(self, interaction: discord.Interaction):
        guild_info = self.get_guild_info(interaction.guild.id)
        if guild_info['colorembed'] is None:
            print("yolo")
            colorembed_loop = tasks.loop()(self.colorembed)
            colorembed_loop.start(interaction.guild.id)
            guild_info['colorembed'] = colorembed_loop            

    async def colorembed(self, guild_id):
        guild_info = self.get_guild_info(guild_id)
        a = True
        if not guild_info['vc'].playing:
            guild_info['task'].cancel()
            guild_info['task'] = None
            guild_info['task2'].cancel()
            guild_info['task2'] = None
            a = False
            await guild_info['message'].edit(embed=discord.Embed(color=discord.Color.red()).add_field(
                name="",
                value="Player Empty x-x"
            ))
            if not guild_info['path'] == r"D:\Discord Bot 2023\lyricsnotfound.lrc":
                os.remove(guild_info['path'])
            guild_info['colorembed'].stop()
            guild_info['colorembed'] = None
        if a:
            await guild_info['message'].edit(embed=discord.Embed(color=discord.Color.random()).add_field(
                name="",
                value=f"💿 **Playing ・❥・** {guild_info['title']}"
            ).set_thumbnail(url=guild_info['thumbnail']))
            
    @discord.app_commands.command(name="set_volume",description="stops and disconnects.")
    @discord.app_commands.describe(volume = "how much volume? (0-1000).")
    async def set_volume(self, interaction: discord.Interaction, volume: int):
        guild_info = self.get_guild_info(interaction.guild.id)
        await guild_info['vc'].set_volume(volume)
        await interaction.response.send_message(f"Set volume: {volume} ✅")
         
    @discord.app_commands.command(name="disconnect",description="stops and disconnects.")
    async def disconnect(self, interaction: discord.Interaction):
        guild_info = self.get_guild_info(interaction.guild.id)
        await guild_info['vc'].stop()
        await guild_info['vc'].disconnect()
        await interaction.response.send_message("Disconnected ✅")

async def setup(client):
    await client.add_cog(MusicBot(client), guilds=[discord.Object(id=1154376568173506592)])
