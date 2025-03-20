import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from keybert import KeyBERT

kw_model = KeyBERT()
sia = SentimentIntensityAnalyzer()


# summarizer = pipeline("summarization", model="google/pegasus-xsum")


def analyze_sentiment_vader(text):
    """Performs sentiment analysis using VADER (Positive, Neutral, Negative)"""
    score = sia.polarity_scores(text)["compound"]
    return "Positive" if score > 0.05 else "Negative" if score < -0.05 else "Neutral"


def chunk_text(text, chunk_size=500):
    """Breaks large text into smaller chunks for summarization."""
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


#
# def summarize(text, chunk_size=500):
#     chunks = chunk_text(text, chunk_size)
#     summaries = []
#     for chunk in chunks:
#         summary = summarizer(text, max_length=50, min_length=20, do_sample=False)
#         print(summary[0]['summary_text'])
#     return "".join(summaries)






