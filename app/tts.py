import os
from gtts import gTTS


def tts_speak(text):
    language = "hi"
    speech = gTTS(text=text, lang=language, slow=False)
    save_path = r'C:\Users\Saumya\PycharmProjects\news_scraper\audio'
    file_path = os.path.join(save_path, 'output.mp3')
    speech.save(file_path)