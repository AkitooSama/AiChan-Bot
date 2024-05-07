from typing import Optional, Literal
import random
import aiohttp
import json
from urllib.parse import urlencode
import googletrans

import asyncio

import discord
from discord.ext import commands

from functions.Fnchatresponse import TenorAI, AiChan
from functions.mixer import RealTimeAudioMixer
from func import SpeechProcessing

chat_members: dict = {}

BASE_URL = "http://127.0.0.1:50021"
VOICE_ID = 25
SPEED_SCALE = 1.2
VOLUME_SCALE = 1.8
INTONATION_SCALE = 1.5
PRE_PHONEME_LENGTH = 1.0
POST_PHONEME_LENGTH = 1.0
ACCENT_TYPE = 2

speak: bool = False

tenor = TenorAI()
translator = googletrans.Translator()
speech = SpeechProcessing()
ai_chan = AiChan()

soundboard: list[str] = []

background_audio_path = r"D:\LMAOOOOOOOOOOOO\Download\x2mate.com - 5 MINUTES OF (No Copyright Music) CHILL LOFI HIP HOP BEAT (Royalty free) (128 kbps).wav"


def wave_to_bytes(file_path):
    with open(file_path, 'rb') as wf:
        frames = wf.read()
        return frames

audio_mixer = RealTimeAudioMixer(wave_to_bytes(background_audio_path))

def ai_bool(num1: int, num2: int, number_list: list):
    number = random.randint(num1, num2)
    if number in number_list:
        return True
    else:return False

class AiChat(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def process_message(self, message: discord.Message):
        if message.author == self.client.user:
            return
        
        user_id = message.author.id

        if user_id in chat_members:
            content = message.content

            if content.startswith("aichan play"):
                await audio_mixer.reset_player(content[11:])

            elif content.startswith("-ps"):
                audio_data = wave_to_bytes(random.choice(soundboard))
                audio_mixer.add_dialogue(audio_data)

            elif content.startswith("-"):
                print("Ignoring command")
                return
            
            else:
                reply = await ai_chan.get_response(input=f"{message.author.display_name}: {content}")
                print(reply)
                bool_val = ai_bool(num1=1, num2=10, number_list=[1, 2]) 

                reply_json = json.loads(reply)
                if reply_json:
                    tasks = []

                    # Process main_reply and other actions concurrently
                    tasks.append(message.reply(reply_json["full_reply"]))

                    if speak:
                        voice = translator.translate(reply_json["main_reply"], src="en", dest="ja").text
                        if voice and not len(reply_json["main_reply"]) > 1000:
                            tasks.append(self.speak_ai(voice))

                    if bool_val:
                        tasks.append(tenor.get_gif(search_term=reply_json["full_reply"]))

                    join_action = reply_json["action_reply"].get("join")
                    if join_action:
                        tasks.append(self.process_action("join", join_action, user_id, message))

                    other_actions = [(action, value) for action, value in reply_json["action_reply"].items() if action != "join"]
                    for action, value in other_actions:
                        tasks.append(self.process_action(action, value, user_id, message))

                    await asyncio.gather(*tasks)
    
    async def speak_ai(self, voice):
        voice_bytes = await self.speak_jp(voice)
        audio_mixer.add_dialogue(voice_bytes)

    async def process_action(self, action, value, user_id, message):
        global speak
        if action == "join" and value:
            if chat_members[user_id] != "yes":
                chat_members[user_id] = "yes"
                if not audio_mixer.is_playing:
                    try:
                        vc = await message.author.voice.channel.connect()
                        self.client.loop.create_task(audio_mixer.start_audio_mixer(voice_client=vc))
                    except: await message.channel.send("Please join any voice channel so that I can join lah~")
        else:
            if action == "play" and value:
                if chat_members[user_id] != "yes":
                    chat_members[user_id] = "yes"
                    if not audio_mixer.is_playing:
                        vc = await message.author.voice.channel.connect()
                        self.client.loop.create_task(audio_mixer.start_audio_mixer(voice_client=vc))
                await audio_mixer.reset_player(value)

            elif action == "gif" and value:
                gif_link = await tenor.get_gif(search_term=f"{value} anime")
                await message.channel.send(gif_link)

            elif action == "emote" and value:
                gif_link = await tenor.get_gif(search_term=f"{value} anime")
                embed = discord.Embed(title="", color=discord.Color.random())
                embed.set_image(url=gif_link)
                embed.add_field(name="", value=f"***{value}***")
                await message.channel.send(embed=embed)

            elif action == "change_song" and value:
                if chat_members[user_id] == "yes":
                    await audio_mixer.reset_player(value)

            elif action == "speak" and value:
                if chat_members[user_id] != "yes":
                    chat_members[user_id] = "yes"
                    if not audio_mixer.is_playing:
                        vc = await message.author.voice.channel.connect()
                        self.client.loop.create_task(audio_mixer.start_audio_mixer(voice_client=vc))

    async def speak_jp(self, sentence):
        params_encoded = urlencode({'text': sentence, 'speaker': VOICE_ID})
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{BASE_URL}/audio_query?{params_encoded}') as response:
                if response.status == 404:
                    print('Unable to reach Voicevox, ensure that it is running, or the VOICEVOX_BASE_URL variable is set correctly')
                    return

                voicevox_query = await response.json()
                voicevox_query.update({
                    'speedScale': SPEED_SCALE,
                    'volumeScale': VOLUME_SCALE,
                    'intonationScale': INTONATION_SCALE,
                    'prePhonemeLength': PRE_PHONEME_LENGTH,
                    'postPhonemeLength': POST_PHONEME_LENGTH
                })

                params_encoded = urlencode({'speaker': VOICE_ID, 'is_kana': True})
                async with session.post(f'{BASE_URL}/synthesis?{params_encoded}', json=voicevox_query) as synthesis_response:
                    return await synthesis_response.read()



    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await self.process_message(message)

    @discord.app_commands.command(name="chat", description="Slash command for chatting with me.")
    @discord.app_commands.describe(voice="Want me to speak?")
    async def _chat(self, interaction: discord.Interaction, voice: Optional[Literal['Yes','No']]):
        if not voice: voice="no"
        user_id: int = interaction.user.id
        if user_id not in chat_members.keys():
            await interaction.response.send_message("Hello~~")
            chat_members[user_id] = voice.lower()
            
            if not audio_mixer.is_playing and voice.lower()=="yes":
                vc = await interaction.user.voice.channel.connect()
                self.client.loop.create_task(audio_mixer.start_audio_mixer(voice_client=vc))
        else:
            await interaction.response.send_message("I'm already talkinngggggg")
        
    @discord.app_commands.command(name="speak", description="Slash command for talking with you.")
    async def _speak(self, interaction: discord.Interaction):
        global speak
        speak = not speak
        await interaction.response.send_message("Okaaa")

    @discord.app_commands.command(name="set_background_volume", description="Slash command for setting the background volume.")
    @discord.app_commands.describe(volume="volume between 0.0 to 1.0.")
    async def _set_background_volume(self, interaction: discord.Interaction, volume: float):
        audio_mixer.set_volumes(background_volume=volume)
        await interaction.response.send_message(f"background volume set to: {volume}")

    @discord.app_commands.command(name="toggle_low_pass", description="Slash command for toggling low pass filter")
    async def _toggle_low_pass(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await audio_mixer.toggle_low_pass_filter()
        await interaction.followup.send("Toggled!")

    @discord.app_commands.command(name="set_dialogue_volume", description="Slash command for setting the dialogue volume.")
    @discord.app_commands.describe(volume="volume between 0.0 to 1.0.")
    async def _set_dialogue_volume(self, interaction: discord.Interaction, volume: float):
        audio_mixer.set_volumes(dialogue_volume=volume)
        await interaction.response.send_message(f"dialogue volume set to: {volume}")

    @discord.app_commands.command(name="set_volume", description="Slash command for setting the volume.")
    @discord.app_commands.describe(volume="volume between 0.0 to 1.0.")
    async def _set_volume(self, interaction: discord.Interaction, volume: float):
        audio_mixer.set_volumes(main_volume=volume)
        await interaction.response.send_message(f"volume set to: {volume}")

async def setup(client: commands.Bot) -> None:
    """Setup function to add the cog to the client."""
    await client.add_cog(AiChat(client))