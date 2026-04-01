import streamlit as st
import pandas as pd
from datetime import datetime

# 1. ページ設定：スマホ向けデフォルト設定
st.set_page_config(
    page_title="Easter Egg Hunt Map 2026", 
    page_icon="🐰", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. カスタムCSS（デザイナーの本能！）
# パステルカラーとフォントを設定
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Varela+Round&display=swap" rel="stylesheet">
    <style>
    /* 全体のフォント */
    html, body, [class*="css"]  {
        font-family: 'Varela Round', sans-serif;
    }
    
    /* ヘッダー（ウサギとエッグのイラストをここに挿入） */
    .header-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
        background-color: #FFF0F5; /* パステルピンク背景 */
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 25px;
    }
    .header-icon { font-size: 3rem; }
    
    /* タイトル */
    h1 {
        color: #7B68EE; /* パステルパープル */
        text-align: center;
        font-size: 2.5rem !important;
    }
    h3 { color: #66c2a5; } /* ミントグリーン */
    
    /* サイドバー */
    [data-testid="stSidebar"] {
        background-color: #F0FFF0; /* パステルグリーン背景 */
    }
    
    /* タブ（選択中：ラベンダー、未選択：パステルピンク） */
    div.stTabs [data-baseweb="tab-list"] button {
        border-color: #FFF0F5;
        background-color: #FFF0F5;
        border-radius: 10px;
        margin-right: 5px;
        padding: 10px 20px;
        font-size: 1.1rem;
    }
    div.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #7B68EE;
        color: white;
    }

    /* ボタン（ミントグリーン） */
    div.stButton > button:first-child {
        background-color: #66c2a5;
        color: white;
        border-radius: 20px;
        border: none;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #7B68EE;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ヘッダー（イラスト入り）
st.markdown("""
    <div class="header-container">
        <span class="header-icon">🐰</span>
        <h1>Easter Scout 2026</h1>
        <span class="header-icon">🥚</span>
    </div>
    """, unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Plano, Frisco, Allen, McKinney & Little Elm</h3>", unsafe_allow_html=True)

# 4. データの読み込み
@st.cache_data
def load_data():
    df = pd.read_csv("easter_events.csv")
    df['date'] = pd.to_datetime(df['date'])
    df['period'] = df['time'].apply(lambda x: '☀️ AM' if 'AM' in x.upper() else '🌙 PM')
    return df

try:
    df = load_data()

    # --- モバイル向けサイドバー設定 (パステルグリーン背景) ---
    st.sidebar.markdown("<h1 style='color: #7B68EE;'>🔍 Filters</h1>", unsafe_allow_html=True)
    selected_dates = st.sidebar.multiselect(
        "Date", options=sorted(df['date'].unique()), 
        default=sorted(df['date'].unique()),
        format_func=lambda x: x.strftime('%m/%d')
    )
    selected_periods = st.sidebar.multiselect(
        "Time", options=['☀️ AM', '🌙 PM'], default=['☀️ AM', '🌙 PM']
    )

    filtered_df = df[(df['date'].isin(selected_dates)) & (df['period'].isin(selected_periods))]

    # --- タブ表示 (パステルピンク背景) ---
    tab1, tab2 = st.tabs(["📍 Map", "📋 List"])

    with tab1:
        # ズーム可能な地図。スマホでもピンチイン・アウトが可能
        # ※地図内のピンの色はStreamlitのテーマに依存します
        st.map(filtered_df, use_container_width=True)
        st.caption("Tip: Pinch to zoom in/out")

    with tab2:
        # ソートして表示
        display_df = filtered_df.sort_values(by=['date', 'time'])
        for _, row in display_df.iterrows():
            with st.expander(f"{row['name']} ({row['city']})"):
                st.write(f"📅 **Date:** {row['date'].strftime('%m/%d')}")
                st.write(f"⏰ **Time:** {row['time']}")
                st.write(f"📍 **Loc:** {row['location']}")
                
                # パステルカラーのボタン
                google_map_url = f"https://www.google.com/maps/search/?api=1&query={row['lat']},{row['lon']}"
                col1, col2 = st.columns(2)
                with col1: st.link_button("Map 🚗", google_map_url)
                with col2: st.link_button("Website 🌐", row['url'])

except Exception as e:
    st.info("Please upload 'easter_events.csv' to your GitHub repository.")
