import streamlit as st
import feedparser
import requests
from datetime import datetime

# ページ設定
st.set_page_config(page_title="Global IP News Hub", layout="centered")

st.title("🇪🇺 Global IP News Hub")
st.caption("欧州各国の知財庁・国際機関の最新ニュース")

# RSSソースの辞書（Google News経由に変換してブロックを回避）
SOURCES = {
    "EPO (欧州特許庁)": "https://news.google.com/rss/search?q=site:epo.org+when:7d&hl=en-GB&gl=GB&ceid=GB:en",
    "EUIPO (欧州連合知的財産庁)": "https://news.google.com/rss/search?q=site:euipo.europa.eu+when:7d&hl=en-GB&gl=GB&ceid=GB:en",
    "European Commission (欧州委員会)": "https://news.google.com/rss/search?q=site:ec.europa.eu+intellectual+property+when:7d&hl=en-GB&gl=GB&ceid=GB:en",
    "WIPO (世界知的所有権機関)": "https://www.wipo.int/pressroom/en/rss.xml", # WIPOはそのままでOK
    "DPMA (ドイツ特許商標庁)": "https://news.google.com/rss/search?q=site:dpma.de+when:30d&hl=de&gl=DE&ceid=DE:de",
    "INPI (フランス)": "https://news.google.com/rss/search?q=site:inpi.fr+when:30d&hl=fr&gl=FR&ceid=FR:fr",
    "EUR-Lex (欧州法)": "https://news.google.com/rss/search?q=site:eur-lex.europa.eu+when:7d&hl=en-GB&gl=GB&ceid=GB:en",
    "Curia (欧州司法裁判所)": "https://news.google.com/rss/search?q=site:curia.europa.eu+when:7d&hl=en-GB&gl=GB&ceid=GB:en"
}

# ニュース取得関数
def fetch_news(url):
    # セッション（ブラウザのセッション維持）を利用する
    session = requests.Session()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
        'Accept': 'application/rss+xml,application/xml,text/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/', # Googleから来たふりをする
        'DNT': '1' # Do Not Track（追跡拒否）の設定
    }
    
    try:
        # verify=False は一部の古いサイトのエラーを回避するため
        response = session.get(url, headers=headers, timeout=15, verify=False)
        response.raise_for_status()
        
        # 文字化け対策
        response.encoding = response.apparent_encoding
        
        return feedparser.parse(response.content)
    except Exception as e:
        # デバッグ用にエラーメッセージを小さく表示
        st.sidebar.warning(f"詳細エラー: {selected_name} が応答しませんでした")
        return None
        
# サイドバーまたは上部に選択ボックスを表示
selected_name = st.selectbox("ニュースソースを選択してください", list(SOURCES.keys()))
url = SOURCES[selected_name]

st.divider()

# 取得と表示
with st.spinner(f'{selected_name} から取得中...'):
    feed = fetch_news(url)

if feed and feed.entries:
    st.success(f"{len(feed.entries)} 件の記事が見つかりました")
    for entry in feed.entries[:20]:  # 最大20件
        with st.container(border=True):
            st.subheader(entry.title)
            
            # 日付の取得を柔軟に
            date_str = entry.get('published', entry.get('updated', '日付不明'))
            st.caption(f"📅 {date_str}")
            
            if 'summary' in entry:
                # 概要を表示（HTMLタグを除去して200文字まで）
                clean_summary = entry.summary.split('<')[0] if '<' in entry.summary else entry.summary
                st.write(clean_summary[:200] + "..." if len(clean_summary) > 200 else clean_summary)
                
            st.link_button("記事を詳しく読む", entry.link)
else:
    st.error("データの取得に失敗しました。ソースが一時的にダウンしているか、アクセス制限がかかっている可能性があります。")
    st.info("別のソースを選択してみてください。")
