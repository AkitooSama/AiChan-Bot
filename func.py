import requests
import googletrans
from urllib.parse import urlencode
import loader
from functions.Fnchatresponse import AiChan
from dotenv import load_dotenv
import os

load_dotenv()

conversation = []

ai_response = AiChan()

config_data = loader.load_config("config.json")

BASE_URL = os.getenv('BASE_URL')
REQUEST_TIMEOUT = config_data["REQUEST_TIMEOUT"]
VOICE_ID = config_data["VOICE_ID"]
accent_type = config_data["accent_type"]

speedScale = config_data["speedScale"]
volumeScale = config_data["volumeScale"]
intonationScale = config_data["intonationScale"]
prePhonemeLength = config_data["prePhonemeLength"]
postPhonemeLength = config_data["postPhonemeLength"]

class SpeechProcessing:
    def __init__(self):
        self.translator = googletrans.Translator()

    def process_speech(self, file, language="en"):
        try:
            eng_speech = self.speech_to_text(file, "transcribe", language)
            print(eng_speech)
            conversation = [{"role": "user", "content": eng_speech}]

            response, response_edited = self.get_response(
                eng_speech, conversation)
            if response and response_edited:
                filtered_response = self.filter_words(response_edited)
                translated_speech = self.translate_text(response, language, "ja")
                if translated_speech:
                    japanese_audio = self.speak_jp(translated_speech)
                    if japanese_audio:
                        return [filtered_response, eng_speech, translated_speech, japanese_audio]
        except requests.exceptions.JSONDecodeError:
            print("Too many requests to process at once")

    async def get_response(self, eng_speech):
        response = await ai_response.get_response(input=eng_speech)
        
        word_mapping = {
            "Ohayou": "Good Morning",
            "ohayou": "Good Morning",
            "gozaimasu": " ",
            "Gozaimasu": " "
        }

        response_edited = response

        for word, replacement in word_mapping.items():
            response = response.replace(word, replacement)
        return response, response_edited

if __name__ == "__main__":
    pass