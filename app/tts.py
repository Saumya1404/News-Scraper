import os
from gtts import gTTS
from bs4 import BeautifulSoup
import tempfile

def clean_html(text):
    return BeautifulSoup(text, "html.parser").get_text()


def tts_speak(text):
    language = "hi"
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(tmp_file.name)
        audio_file = tmp_file.name
    return audio_file


def audio_template(query, summaries, final_sentiments):
    if not summaries:
        return f"Sorry, no news articles were found for {query.capitalize()} today."

    audio_text = f"Hello! Here is your news update for {query.capitalize()}.\n\n"
    audio_text += "Let's take a look at the top articles of the day.\n\n"
    for i, (title,  sentiment) in enumerate(final_sentiments.items()):
        summary = summaries.get(title)
        summary_clean = clean_html(summary)
        audio_text += f"\nArticle {i}: {title}"
        audio_text += f"\nSummary: {summary_clean}"
        audio_text += f"\nSentiment: {sentiment}"

    positive_count = sum(1 for s in final_sentiments.values() if s == "Positive")
    negative_count = sum(1 for s in final_sentiments.values() if s == "Negative")
    neutral_count = sum(1 for s in final_sentiments.values() if s == "Neutral")

    if positive_count > negative_count and positive_count > neutral_count:
        overall_sentiment = "Positive"
    elif negative_count > positive_count and negative_count > neutral_count:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"
    audio_text += f"\nThat is all for today's news on {query.capitalize()}.\n\n"
    audio_text += f"The overall sentiment for {query.capitalize()} seems to be {overall_sentiment}.\n\n"
    return audio_text
