import streamlit as st
import feedparser
import requests

# ページ設定
st.set_page_config(page_title="EU IP News Hub", layout="centered")

st.title("🇪🇺 Global IP News Hub")
st.caption("Google News Indexを利用して欧州全域の知財ニュースを網羅します。")

# Google News検索を利用した全拠点リスト
SOURCES = {
    "EPO (欧州特許庁)": "https://news.google.com/rss/search?q=site:epo.org+when:30d&hl=en-GB&gl=GB&ceid=GB:en",
    "EUIPO (欧州連合知財庁)": "https://news.google.com/rss/search?q=site:euipo.europa.eu+when:30d&hl=en-GB&gl=GB&ceid=GB:en",
    "WIPO (世界知的所有権機関)": "https://www.wipo.int/pressroom/en/rss.xml",
    "European Commission (知財)": "https://news.google.com/rss/search?q=site:ec.europa.eu+intellectual+property+when:30d&hl=en-GB&gl=GB&ceid=GB:en",
    "Curia (欧州司法裁判所)": "https://news.google.com/rss/search?q=site:curia.europa.eu+when:30d&hl=en-GB&gl=GB&ceid=GB:en",
    "EUR-Lex (欧州法)": "https://news.google.com/rss/search?q=site:eur-lex.europa.eu+when:30d&hl=en-GB&gl=GB&ceid=GB:en",
    "DPMA (ドイツ)": "https://news.google.com/rss/search?q=site:dpma.de+when:30d&hl=de&gl=DE&ceid=DE:de",
    "INPI (フランス)": "https://news.google.com/rss/search?q=site:inpi.fr+when:30d&hl=fr&gl=FR&ceid=FR:fr",
    "OEPM (スペイン)": "https://news.google.com/rss/search?q=site:oepm.es+when:30d&hl=es&gl=ES&ceid=ES:es",
    "RVO (オランダ)": "https://news.google.com/rss/search?q=site:rvo.nl+when:30d&hl=nl&gl=NL&ceid=NL:nl",
    "PRV (スウェーデン)": "https://news.google.com/rss/search?q=site:prv.se+when:30d&hl=en&gl=SE&ceid=SE:en",
    "DKPTO (デンマーク)": "https://news.google.com/rss/search?q=site:dkpto.org+when:30d&hl=en&gl=DK&ceid=DK:en",
    "PRH (フィンランド)": "https://news.google.com/rss/search?q=site:prh.fi+when:30d&hl=en&gl=FI&ceid=FI:en",
    "Patentamt (オーストリア)": "https://news.google.com/rss/search?q=site:patentamt.at+when:30d&hl=de&gl=AT&ceid=AT:de",
    "BOIP (ベネルクス)": "https://news.google.com/rss/search?q=site:boip.int+when:30d&hl=en&gl=BE&ceid=BE:en",
    "UPRP (ポーランド)": "https://news.google.com/rss/search?q=site:uprp.gov.pl+when:30d&hl=en&gl=PL&ceid=PL:en",
    "UPV (チェコ)": "https://news.google.com/rss/search?q=site:upv.cz+when:30d&hl=en&gl=CZ&ceid=CZ:en",
    "INDPROP (スロバキア)": "https://news.google.com/rss/search?q=site:indprop.gov.sk+when:30d&hl=en&gl=SK&ceid=SK:en",
    "HIPO (ハンガリー)": "https://news.google.com/rss/search?q=site:hipo.gov.hu+when:30d&hl=en&gl=HU&ceid=HU:en",
    "INPI (ポルトガル)": "https://news.google.com/rss/search?q=site:inpi.justica.gov.pt+when:30d&hl=pt&gl=PT&ceid=PT:pt",
    "OBI (ギリシャ)": "https://news.google.com/rss/search?q=site:obi.gr+when:30d&hl=en&gl=GR&ceid=GR:en",
    "OSIM (ルーマニア)": "https://news.google.com/rss/search?q=site:osim.ro+when:30d&hl=en&gl=RO&ceid=RO:en",
    "BPO (ブルガリア)": "https://news.google.com/rss/search?q=site:bpo.bg+when:30d&hl=en&gl=BG&ceid=BG:en",
    "EPA (エストニア)": "https://news.google.com/rss/search?q=site:epa.ee+when:30d&hl=en&gl=EE&ceid=EE:en",
    "LRPV (ラトビア)": "https://news.google.com/rss/search?q=site:lrpv.gov.lv+when:30d&hl=en&gl=LV&ceid=LV:en",
    "VPB (リトアニア)": "https://vpb.lrv.lt/rss" # ここは直接でOK
}

def get_news(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        feed = feedparser.parse(response.content)
        return feed.entries
    except:
        return []

# ソース選択
selected_name = st.selectbox("ニュースソースを選択", list(SOURCES.keys()))
entries = get_news(SOURCES[selected_name])

if entries:
    for entry in entries[:15]:
        with st.container(border=True):
            st.subheader(entry.title)
            st.caption(f"📅 {entry.get('published', '日付不明')}")
            
            # AI要約用のテキスト作成（コピーしやすくするため）
            copy_text = f"Title: {entry.title}\nURL: {entry.link}"
            
            col1, col2 = st.columns(2)
            with col1:
                st.link_button("記事を読む", entry.link)
            with col2:
                # スマホでもコピーしやすいようテキストエリアに配置
                st.text_edit_area = st.code(copy_text, language="markdown")

else:
    st.warning("現在、表示できる新しいニュースはありません。")
