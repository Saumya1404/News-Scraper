import feedparser
import streamlit as st


@st.cache_data
def fetch_news(rss_url, query,max_results=5):
    # fetching news articles about query from different rss sources
    feed = feedparser.parse(rss_url)
    relavent_articles = []
    query.lower()
    for entry in feed.entries:
        if query.lower() in entry.title.lower() or query.lower() in entry.summary.lower():
            relavent_articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", "No summary available"),
                "published": entry.get("published", "Unknown date")
            })
        if len(relavent_articles) >= max_results:
            break
    return relavent_articles
