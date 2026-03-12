import streamlit as st
import requests
import urllib.parse

# ページ設定
st.set_page_config(page_title="Global IP News Hub", layout="centered")

st.title("🇪🇺 Global IP News Hub")
st.caption("API中継方式により、欧州各国の知財庁ニュースを高速表示します。")

# 全28ソースのRSS URLリスト
SOURCES = {
    "EPO (欧州特許庁)": "https://www.epo.org/en/news-events/rss",
    "EUIPO (欧州連合知的財産庁)": "https://euipo.europa.eu/rss/news",
    "European Commission": "https://ec.europa.eu/newsroom/rss",
    "Curia (欧州司法裁判所)": "https://curia.europa.eu/jcms/jcms/rss_7000/en/",
    "European Parliament": "https://www.europarl.europa.eu/rss/en/news.xml",
    "IP Helpdesk (EU)": "https://intellectual-property-helpdesk.ec.europa.eu/rss.xml",
    "EUR-Lex": "https://eur-lex.europa.eu/rss.xml",
    "WIPO (世界知的所有権機関)": "https://www.wipo.int/pressroom/en/rss.xml",
    "DPMA (ドイツ)": "https://www.dpma.de/service/rss/rss.xml",
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

# ニュース取得関数（API経由）
def get_news(rss_url):
    # RSS URLをエンコードしてAPIに渡す
    encoded_url = urllib.parse.quote_plus(rss_url)
    api_url = f"https://api.rss2json.com/v1/api.json?rss_url={encoded_url}"
    
    try:
        response = requests.get(api_url, timeout=15)
        data = response.json()
        if data.get("status") == "ok":
            return data.get("items", [])
        return []
    except Exception:
        return []

# サイドバーでソース選択
selected_name = st.selectbox("ニュースソースを選択してください", list(SOURCES.keys()))
rss_url = SOURCES[selected_name]

st.divider()

# 実行と表示
with st.spinner('データを取得中...'):
    items = get_news(rss_url)

if items:
    st.success(f"{selected_name} の最新記事 {len(items)} 件を表示します")
    for item in items:
        with st.container(border=True):
            st.subheader(item.get("title", "No Title"))
            
            # 日付の表示
            pub_date = item.get("pubDate", "日付不明")
            st.caption(f"📅 {pub_date}")
            
            # 要約（description）からHTMLタグを簡易的に除去して表示
            desc = item.get("description", "")
            if desc:
                # 文字数制限（スマホで見やすく）
                clean_desc = desc.split('<')[0] if '<' in desc else desc
                st.write(clean_desc[:150] + "..." if len(clean_desc) > 150 else clean_desc)
            
            st.link_button("記事を詳しく読む", item.get("link", "#"))
else:
    st.error("データの取得に失敗しました。")
    st.info("理由: サイト側でRSS配信が一時停止しているか、APIの制限に達した可能性があります。")
