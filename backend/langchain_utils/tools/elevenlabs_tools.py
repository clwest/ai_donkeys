from langchain.tools import ElevenLabsText2SpeechTool
import logging
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()
eleven_labs = os.environ.get("ELEVEN_LABS_API")

text_to_speak = "Hello world! I am the real slim shady"

tts = ElevenLabsText2SpeechTool()
tts.name
print(tts.name)
speech_file = tts.run(text_to_speak)
tts.play(speech_file)
print(tts.play(speech_file))

tts.stream_speech(text_to_speak)
print(tts.stream_speech(text_to_speak))
