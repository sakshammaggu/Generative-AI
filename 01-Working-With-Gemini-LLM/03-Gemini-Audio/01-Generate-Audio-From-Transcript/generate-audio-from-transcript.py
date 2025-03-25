"""
This script demonstrates how to convert text to speech using Google Text-to-Speech (gTTS).
It takes a text input and generates an MP3 audio file containing the spoken version of the text.
The generated audio can be used for various purposes like creating voiceovers, audio content, etc.
"""

from gtts import gTTS

text = "This is a sample voice audio generated using Python. You can modify the text to create different audio clips."
tts = gTTS(text=text, lang='en')
tts.save("sample_audio.mp3")
print("Audio file saved as sample_audio.mp3")