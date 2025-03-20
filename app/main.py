from newspaper import Article
from rss import rss_feeds
from scrape import fetch_news
from sentiment_analysis import analyze_sentiment_vader, kw_model
from translate_to_hindi import translate
from tts import tts_speak
from comparative_analysis import compare

query = "nvidia"
all_filtered_news = []
for rss in rss_feeds:
    all_filtered_news.extend(fetch_news(rss, query, max_results=5))
article_keywords = {}
translated_summary=[]

# Display results
print(f"\n Total  articles found: {len(all_filtered_news)}")
for news in all_filtered_news:
    print(news['title'])
    print(news['link'])
    article = Article(news['link'])
    article.download()
    article.parse()
    # print(article.text)
    print(analyze_sentiment_vader(article.text))
    print(analyze_sentiment_vader(news['summary']))
    print("👍🏻👍🏻👍🏻")
    keywords = kw_model.extract_keywords(article.text, keyphrase_ngram_range=(1, 1), top_n=10,
                                         diversity=0.5, use_mmr=True)
    print(f"Keywords: {[kw[0] for kw in keywords] if keywords else 'No Keywords Found'}")
    article_keywords[article.title] = [kw[0] for kw in keywords] if keywords else 'No Keywords Found'
    translated_summary.append(translate(news['summary']))
for summaries in translated_summary:
    print(summaries)
    tts_speak(summaries)

for i in article_keywords:
    print(f'{i} : {article_keywords[i]}')

result = compare(article_keywords)
print(result)
