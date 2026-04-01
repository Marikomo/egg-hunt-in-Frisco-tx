import streamlit as st
import pandas as pd

# 1. ページ設定
st.set_page_config(
    page_title="Easter Scout 2026",
    page_icon="🐰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. デザインの修正 (ここを丸ごと上書きしてください)
st.markdown("""
    <style>
    /* 全体のフォント */
    html, body, [class*="css"] {
        font-family: 'sans serif';
    }
    
    /* タイトル部分の背景 */
    .hero-bg {
        background-color: #FFF0F5;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* タイトルの色 */
    .main-title {
        color: #7B68EE;
        font-size: 3rem;
        font-weight: bold;
    }

    /* ボタンの色 */
    div.stButton > button {
        background-color: #66c2a5 !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
    }

    /* タブのデザイン */
    div.stTabs [data-baseweb="tab-list"] button {
        background-color: #FFF0F5;
        border-radius: 10px;
        margin-right: 5px;
    }
    div.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #7B68EE;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. タイトル表示
st.markdown("""
    <div class="hero-bg">
        <div style="font-size: 3rem;">🐰 🥚</div>
        <div class="main-title">Easter Scout 2026</div>
        <div style="color: #555; font-size: 1.2rem;">Plano, Frisco, Allen, McKinney & Little Elm</div>
    </div>
    """, unsafe_allow_html=True)

# 4. データの読み込み
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("easter_events.csv")
        df['date'] = pd.to_datetime(df['date'])
        df['period'] = df['time'].apply(lambda x: '☀️ Morning' if 'AM' in x.upper() else '🌙 Afternoon')
        return df
    except:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # フィルター
    st.sidebar.title("Search Filter")
    city_list = st.sidebar.multiselect("Cities", options=df['city'].unique(), default=df['city'].unique())
    
    filtered_df = df[df['city'].isin(city_list)]

    # タブ
    tab1, tab2 = st.tabs(["📍 Map View", "📋 List View"])
    
    with tab1:
        st.map(filtered_df)
        
    with tab2:
        for _, row in filtered_df.sort_values(by='date').iterrows():
            with st.expander(f"{row['name']} ({row['city']})"):
                st.write(f"📅 Date: {row['date'].strftime('%m/%d')}")
                st.write(f"⏰ Time: {row['time']}")
                st.link_button("Directions 🚗", f"https://www.google.com/maps/search/?api=1&query={row['lat']},{row['lon']}")
                st.link_button("Official Site 🌐", row['url'])
else:
    st.warning("Please upload 'easter_events.csv' to GitHub to see the events!")
