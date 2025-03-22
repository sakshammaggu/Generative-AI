from gtts import gTTS

text = "This is a sample voice audio generated using Python. You can modify the text to create different audio clips."

tts = gTTS(text=text, lang='en')
tts.save("sample_audio.mp3")

print("Audio file saved as sample_audio.mp3")