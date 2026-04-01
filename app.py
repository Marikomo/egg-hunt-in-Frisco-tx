import streamlit as st
import pandas as pd

# 1. ページ設定
st.set_page_config(page_title="Easter Scout 2026", page_icon="🐰", layout="wide")

# 2. デザイン (CSS) - パステルカラー
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .hero { background: linear-gradient(135deg, #FFF0F5 0%, #F0FFF0 100%); padding: 20px; border-radius: 15px; text-align: center; border: 2px dashed #7B68EE; }
    h1 { color: #7B68EE !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🐰 Easter Scout 2026 🥚</h1><p>Plano, Frisco, Allen, McKinney & Little Elm</p></div>', unsafe_allow_html=True)

# 3. データの読み込み（エラー回避機能付き）
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("easter_events.csv")
        # 列名をきれいにする（大文字小文字、空白を無視）
        df.columns = [c.lower().strip() for c in df.columns]
        
        # 'date'列が存在するかチェック
        if 'date' in df.columns:
            # 日付形式を自動判別して変換（エラーは無視）
            df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
            # 日付が空の行を削除
            df = df.dropna(subset=['date'])
        
        # 午前/午後の判定（time列があれば）
        if 'time' in df.columns:
            df['period'] = df['time'].apply(lambda x: '☀️ Morning (AM)' if 'AM' in str(x).upper() else '🌙 Afternoon (PM)')
        else:
            df['period'] = '☀️ Morning (AM)'
            
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

# 4. アプリのメイン表示
if not df.empty:
    # サイドバーフィルター
    st.sidebar.header("🌷 Filters")
    
    # 日付フィルター
    date_list = sorted(df['date'].unique())
    sel_dates = st.sidebar.multiselect("Select Date", options=date_list, default=date_list, format_func=lambda x: x.strftime('%m/%d'))
    
    # 午前/午後フィルター
    sel_periods = st.sidebar.multiselect("Time of Day", options=['☀️ Morning (AM)', '🌙 Afternoon (PM)'], default=['☀️ Morning (AM)', '🌙 Afternoon (PM)'])

    # フィルタリング
    f_df = df[(df['date'].isin(sel_dates)) & (df['period'].isin(sel_periods))]

    tab1, tab2 = st.tabs(["📍 Map View", "📋 List View"])

    with tab1:
        st.subheader(f"Found {len(f_df)} Events")
        # 地図を表示
        st.map(f_df)

    with tab2:
        for _, row in f_df.sort_values(by='date').iterrows():
            with st.expander(f"{row.get('name', 'Event')} ({row.get('city', 'Area')})"):
                st.write(f"📅 Date: {row['date']}")
                st.write(f"⏰ Time: {row.get('time', 'Check Website')}")
                st.link_button("Directions 🚗", f"https://www.google.com/maps/search/?api=1&query={row['lat']},{row['lon']}")
                st.link_button("Website 🌐", row.get('url', 'https://planomoms.com/'))
else:
    st.warning("⚠️ Data could not be loaded. Please check your CSV format on GitHub.")
