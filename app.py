import streamlit as st
import feedparser

feeds = {
    "EPO": "https://www.epo.org/en/news-events/rss",
    "EUIPO": "https://euipo.europa.eu/rss/news",
    "European Commission": "https://ec.europa.eu/newsroom/rss",
}

st.title("EU IP News Watcher")

articles = []

for source, url in feeds.items():

    feed = feedparser.parse(url)

    for entry in feed.entries[:5]:

        articles.append({
            "source": source,
            "title": entry.title,
            "date": entry.published,
            "url": entry.link
        })

for a in articles:

    st.subheader(a["title"])
    st.write("Source:", a["source"])
    st.write("Date:", a["date"])
    st.write(a["url"])

    st.divider()
