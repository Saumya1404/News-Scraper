import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from keybert import KeyBERT
nltk.download('vader_lexicon')
kw_model = KeyBERT()
sia = SentimentIntensityAnalyzer()


def analyze_sentiment_vader(text):
    """Performs sentiment analysis using VADER (Positive, Neutral, Negative)"""
    score = sia.polarity_scores(text)["compound"]
    return "Positive" if score > 0.05 else "Negative" if score < -0.05 else "Neutral"


def chunk_text(text, chunk_size=512):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_length += len(word) + 1
        if current_length > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word) + 1
        else:
            current_chunk.append(word)
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks


def weighted_analysis(sentiment_analysis_title, sentiment_analysis_text):

    title_weight = 0.3
    text_weight = 0.7
    final_sentiment = {}
    for keys in sentiment_analysis_title:
        title_score = 1 if sentiment_analysis_title[keys] == 'Positive' else -1 if sentiment_analysis_title[
                                                                                        keys] == 'Negative' else 0
        text_score = 1 if sentiment_analysis_text[keys] == 'Positive' else -1 if sentiment_analysis_text[
                                                                                      keys] == 'Negative' else 0
        combined_score = title_weight * title_score + text_weight * text_score
        if combined_score > 0.05:
            final_sentiment[keys] = "Positive"
        elif combined_score > -0.05:
            final_sentiment[keys] = "Negative"
        else:
            final_sentiment[keys] = "Neutral"
    return final_sentiment
