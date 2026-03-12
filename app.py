import streamlit as st
import feedparser
import requests

# ページ設定
st.set_page_config(page_title="EU IP News Hub", layout="wide")

st.title("🇪🇺 EU Intellectual Property News Hub")
st.write("EPO, EUIPO, および欧州委員会の最新ニュースをまとめてチェックできます。")

# ニュースサイトの設定（サイト名: RSSのURL）
SOURCES = {
    "EPO (欧州特許庁)": "https://www.epo.org/en/news-events/news/feed",
    "EUIPO (欧州連合知的財産庁)": "https://www.euipo.europa.eu/en/news-and-events/news/rss",
    "European Commission (欧州委員会 - 知財関連)": "https://ec.europa.eu/newsroom/seaipr/rss/items"
}

def fetch_news(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return feedparser.parse(response.content)
    except:
        return None

# タブを作成
tabs = st.tabs(list(SOURCES.keys()))

for i, (name, url) in enumerate(SOURCES.items()):
    with tabs[i]:
        st.header(f"{name} の最新ニュース")
        feed = fetch_news(url)
        
        if feed and feed.entries:
            for entry in feed.entries[:10]: # 最新10件を表示
                with st.container(border=True):
                    st.subheader(entry.title)
                    # 日付表示（サイトによって形式が異なる場合があるためケア）
                    date = entry.get('published', entry.get('updated', '日付不明'))
                    st.caption(f"📅 {date}")
                    
                    if 'summary' in entry:
                        # タグを除去して150文字程度表示
                        summary = entry.summary[:150] + "..."
                        st.write(summary)
                        
                    st.link_button(f"{name} で記事を読む", entry.link)
        else:
            st.error(f"{name} のデータを取得できませんでした。URLが変更されているか、一時的なエラーです。")
