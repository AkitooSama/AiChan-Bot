from pydub import AudioSegment
import discord
import asyncio
import io
from queue import Queue
from pytube import YouTube
import ffmpeg
from discord.ext import tasks
from youtube_search import YoutubeSearch

def get_audio_data(link: str):
    yt = YouTube(link)
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    stream_url = audio_stream.url
    audio, _ = (
        ffmpeg
        .input(stream_url)
        .output("pipe:", format='wav', acodec='pcm_s16le')
        .run(capture_stdout=True, capture_stderr=True)
    )
    return audio

class RealTimeAudioMixer:
    def __init__(self, background_audio_bytes):
        self.background_audio_data = background_audio_bytes
        self.reset_data = background_audio_bytes
        self.dialogue_queue = Queue()
        self.is_playing = False
        self.voice_client = None
        self.playing_dialogue = False
        self.start_time = None
        self.next_time = None
        self.current_position = None
        self.player = True
        self.volume = 0.050
        self.volume_transformer = None
        self.background_volume = 25
        self.dialogue_volume = 0

    def mix_audio(self, dialogue_audio_bytes, background_audio_bytes, current_position):
        dialogue_audio = AudioSegment.from_file(io.BytesIO(dialogue_audio_bytes))
        background_audio = AudioSegment.from_file(io.BytesIO(background_audio_bytes))
        offset = 0.78
        d_offset = -0.10

        # Cut the background audio from the current position to end
        background_audio = background_audio[current_position + offset * 1000:]

        # Normalize audio properties
        dialogue_audio = dialogue_audio.set_frame_rate(44100).set_channels(2)
        dialogue_duration = len(dialogue_audio)
        new = background_audio[dialogue_duration + (d_offset * 1000):]

        output_buffer = io.BytesIO()
        new.export(output_buffer, format='wav')
        output_buffer.seek(0)
        mixed_audio_bytes = output_buffer.read()
        
        self.background_audio_data = mixed_audio_bytes

        background_audio = background_audio.set_frame_rate(44100).set_channels(2) - self.background_volume

        # Slice background audio to match the duration of the dialogue audio
        mixed_audio = background_audio[:dialogue_duration].overlay(dialogue_audio) - self.dialogue_volume

        # Export the mixed audio as bytes
        output_buffer = io.BytesIO()
        mixed_audio.export(output_buffer, format='wav')
        output_buffer.seek(0)
        mixed_audio_bytes = output_buffer.read()

        return mixed_audio_bytes

    async def start_audio_mixer(self, voice_client: discord.VoiceClient):
        self.voice_client = voice_client
        self.player = True
        self.is_playing = True

        # Play the background music by default
        audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(io.BytesIO(self.background_audio_data), pipe=True), volume=self.volume)
        self.volume_transformer = audio_source
        self.voice_client.play(audio_source)
        self.start_time = discord.utils.utcnow()  # Record the start time of background music
        print(len(self.background_audio_data))
        if not self.final_mixer.is_running():
            await self.final_mixer.start()
            
    def add_dialogue(self, dialogue_audio_bytes):
        self.dialogue_queue.put(dialogue_audio_bytes)
        print(len(self.background_audio_data))
        
    def _continue_playback(self, error=None):
        if error:
            print("Error in playback:", error)
        else:
            # Play the background music by default
            audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(io.BytesIO(self.background_audio_data), pipe=True), volume=self.volume)
            self.volume_transformer = audio_source
            if not self.voice_client.is_playing():
                self.voice_client.play(audio_source)
            self.start_time = discord.utils.utcnow()
            self.playing_dialogue = False
            self.next_time = discord.utils.utcnow()  # Record the start time of background music

    def stop_audio_mixer(self):
        self.is_playing = False

    def set_volumes(self, background_volume: float = None, dialogue_volume: float = None, main_volume: float = None):
        if not background_volume: background_volume = self.background_volume
        if not dialogue_volume: dialogue_volume = self.dialogue_volume
        if not main_volume: main_volume = self.volume
        
        self.background_volume = background_volume
        self.dialogue_volume = dialogue_volume
        self.volume = main_volume
        self.volume_transformer.volume = main_volume

    async def reset_player(self, name):
        self.is_playing = False
        self.player = False
        results = YoutubeSearch(name, max_results=1).to_dict()
        video_id = results[0]['id']
        link = f"https://www.youtube.com/watch?v={video_id}"
        audio_data = await get_audio_data(link=link)
        self.background_audio_data = audio_data
        self.reset_data = audio_data
        self.voice_client.stop()
        await self.start_audio_mixer(self.voice_client)

    async def toggle_low_pass_filter(self):
        # Low-pass filter settings
        low_pass_cutoff = 1000  # Adjust this value based on your requirements

        # Applying low-pass filter to background audio
        background_audio = AudioSegment.from_file(io.BytesIO(self.background_audio_data))
        background_audio_low_pass = background_audio.low_pass_filter(low_pass_cutoff)

        # Export the low-pass filtered background audio as bytes
        output_buffer = io.BytesIO()
        background_audio_low_pass.export(output_buffer, format='wav')
        output_buffer.seek(0)
        low_pass_background_audio_bytes = output_buffer.read()

        # If currently playing, stop and restart with the new filtered background audio
        if self.is_playing:
            self.voice_client.stop()
            self.background_audio_data = low_pass_background_audio_bytes
            await self.start_audio_mixer(self.voice_client)
        else:
            self.background_audio_data = low_pass_background_audio_bytes

    @tasks.loop()
    async def final_mixer(self):
        if self.player:
            if self.is_playing:
                if len(self.background_audio_data) < 60:
                    print(len(self.background_audio_data))
                    print("reset")
                    self.background_audio_data = self.reset_data
                    self.voice_client.stop()
                    self._continue_playback()
                
                if not self.dialogue_queue.empty() and not self.playing_dialogue:
                    self.playing_dialogue = True
                    dialogue_audio_data = self.dialogue_queue.get()
                    current_position = None
                    next_time = None             
                    
                    if not next_time:
                        # Calculate the elapsed time since the background music started playing
                        current_time = discord.utils.utcnow()
                        current_position = (current_time - self.start_time).total_seconds() * 1000  # Convert to milliseconds
                        self.current_position = current_position
                        
                    if next_time:
                        # Calculate the elapsed time since the background music started playing
                        current_time = discord.utils.utcnow()
                        current_position = (current_time - (self.start_time + self.next_time)).total_seconds() * 1000  # Convert to milliseconds
                        self.current_position = current_position

                    merged_audio = self.mix_audio(dialogue_audio_data, self.background_audio_data, current_position)

                    # Stop background music playback if it's ongoing
                    if self.voice_client.is_playing():
                        self.voice_client.stop()

                    # Play the overlaid dialogue audio
                    print('inside dialogue')
                    audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(io.BytesIO(merged_audio), pipe=True), volume=self.volume)
                    self.volume_transformer = audio_source
                    self.voice_client.play(audio_source, after=lambda e: self._continue_playback(e))

if __name__=="__main__":
    results = YoutubeSearch("bts butter", max_results=1).to_dict()
    video_id = results[0]['id']
    link = f"https://www.youtube.com/watch?v={video_id}"
    print(link)
    print(get_audio_data(link=link))
    # audio_data = await get_audio_data(link=link)