import streamlit as st
import feedparser
import requests

st.title("🇪🇺 EPO News Watcher")

# EPOのRSSフィードURL
RSS_URL = "https://www.epo.org/en/news-events/news/feed"

# 1. requestsを使ってブラウザからのアクセスを装う
def fetch_rss(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # エラーがあれば例外を出す
        return response.content
    except Exception as e:
        st.error(f"データの取得に失敗しました: {e}")
        return None

# 実行
xml_data = fetch_rss(RSS_URL)

if xml_data:
    # 2. 取得したXMLをfeedparserで解析
    feed = feedparser.parse(xml_data)
    
    if not feed.entries:
        st.warning("ニュースが見つかりませんでした。")
    
    # 3. スマホで見やすく表示
    for entry in feed.entries:
        with st.container(border=True): # 枠で囲って見やすく
            st.subheader(entry.title)
            st.caption(f"📅 {entry.published}")
            
            # 要約があれば表示（HTMLタグを除去して表示される）
            if 'summary' in entry:
                st.write(entry.summary)
            
            st.link_button("記事を詳しく見る", entry.link)
