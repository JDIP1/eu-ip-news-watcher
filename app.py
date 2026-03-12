import streamlit as st
import feedparser
import requests
from datetime import datetime

# ページ設定
st.set_page_config(page_title="Global IP News Hub", layout="centered")

st.title("🇪🇺 Global IP News Hub")
st.caption("欧州各国の知財庁・国際機関の最新ニュース")

# RSSソースの辞書（名称: URL）
SOURCES = {
    "EPO (欧州特許庁)": "https://www.epo.org/en/news-events/rss",
    "EUIPO (欧州連合知的財産庁)": "https://euipo.europa.eu/rss/news",
    "European Commission (欧州委員会)": "https://ec.europa.eu/newsroom/rss",
    "Curia (欧州司法裁判所)": "https://curia.europa.eu/jcms/jcms/rss_7000/en/",
    "European Parliament (欧州議会)": "https://www.europarl.europa.eu/rss/en/news.xml",
    "IP Helpdesk (EU)": "https://intellectual-property-helpdesk.ec.europa.eu/rss.xml",
    "EUR-Lex (欧州法)": "https://eur-lex.europa.eu/rss.xml",
    "WIPO (世界知的所有権機関)": "https://www.wipo.int/pressroom/en/rss.xml",
    "DPMA (ドイツ特許商標庁)": "https://www.dpma.de/service/rss/rss.xml",
    "INPI (フランス)": "https://www.inpi.fr/fr/rss/actualites",
    "OEPM (スペイン)": "https://www.oepm.es/export/sites/oepm/comun/rss/rss_noticias.xml",
    "RVO (オランダ)": "https://www.rvo.nl/rss/octrooien.xml",
    "PRV (スウェーデン)": "https://www.prv.se/en/rss/news/",
    "DKPTO (デンマーク)": "https://www.dkpto.org/rss/news",
    "PRH (フィンランド)": "https://www.prh.fi/en/rss/news.xml",
    "Patentamt (オーストリア)": "https://www.patentamt.at/en/rss/news",
    "BOIP (ベネルクス)": "https://www.boip.int/en/rss/news",
    "UPRP (ポーランド)": "https://uprp.gov.pl/en/rss.xml",
    "UPV (チェコ)": "https://www.upv.cz/en/rss/news",
    "INDPROP (スロバキア)": "https://www.indprop.gov.sk/en/rss.xml",
    "HIPO (ハンガリー)": "https://www.hipo.gov.hu/en/rss",
    "INPI (ポルトガル)": "https://inpi.justica.gov.pt/rss",
    "OBI (ギリシャ)": "https://www.obi.gr/rss",
    "OSIM (ルーマニア)": "https://www.osim.ro/rss",
    "BPO (ブルガリア)": "https://www.bpo.bg/rss",
    "EPA (エストニア)": "https://www.epa.ee/rss",
    "LRPV (ラトビア)": "https://www.lrpv.gov.lv/rss",
    "VPB (リトアニア)": "https://vpb.lrv.lt/rss"
}

# ニュース取得関数
def fetch_news(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return feedparser.parse(response.content)
    except Exception as e:
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
