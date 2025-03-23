from newspaper import Article
from .rss import rss_feeds
from .scrape import fetch_news
from .sentiment_analysis import analyze_sentiment_vader, kw_model, weighted_analysis
from .translate_to_hindi import translate
from .tts import tts_speak, audio_template
from .comparative_analysis import compare

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()


class NewsRequest(BaseModel):
    query: str


@app.post('/analyze-news')
async def analyze_news(request: NewsRequest):
    try:
        company_name = request.query.strip().lower()

        all_filtered_news = []
        article_keywords = {}
        summaries = {}
        sentiment_analysis_title = {}
        sentiment_analysis_text = {}

        for rss in rss_feeds:
            all_filtered_news.extend(fetch_news(rss, company_name, max_results=5))

        for news in all_filtered_news:
            article = Article(news['link'])
            article.download()
            article.parse()
            print(news['title'])
            sentiment_analysis_title[news['title']] = analyze_sentiment_vader(news['title'])
            sentiment_analysis_text[news['title']] = analyze_sentiment_vader(article.text)
            summaries[news['title']] = news['summary']

            keywords = kw_model.extract_keywords(article.text, keyphrase_ngram_range=(1, 3), top_n=7,
                                                 diversity=0.7, use_mmr=True)
            article_keywords[article.title] = [kw[0] for kw in keywords] if keywords else 'No Keywords Found'

        result = compare(article_keywords)
        final_sentiments = weighted_analysis(sentiment_analysis_title, sentiment_analysis_text)
        tts_audio = audio_template(company_name, summaries, final_sentiments)
        translated_audio = translate(tts_audio)
        audio_file_path = tts_speak(translated_audio)

        return {"summaries": summaries, "sentiments": final_sentiments, "audio_path": audio_file_path, "result": result}
    except Exception as e:
        return {"error": str(e)}

