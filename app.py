import streamlit as st
import pandas as pd

# 1. ページ設定 (モバイル最適化)
st.set_page_config(
    page_title="Easter Scout 2026",
    page_icon="🐰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. パステルカラー & 可愛いデザイン (CSS)
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .hero {
        background: linear-gradient(135deg, #FFF0F5 0%, #F0FFF0 100%);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        border: 2px dashed #7B68EE;
        margin-bottom: 20px;
    }
    h1 { color: #7B68EE !important; }
    /* サイドバーのパステルグリーン */
    [data-testid="stSidebar"] { background-color: #F0FFF0; }
    </style>
    """, unsafe_allow_html=True)

# 3. タイトル
st.markdown("""
    <div class="hero">
        <h1>🐰 Easter Scout 2026 🥚</h1>
        <p>Plano, Frisco, Allen, McKinney & Little Elm</p>
    </div>
    """, unsafe_allow_html=True)

# 4. データの読み込み
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("easter_events.csv")
        # 列名をすべて小文字に強制変換 (KeyError対策)
        df.columns = [c.lower().strip() for c in df.columns]
        # 日付を変換
        df['date'] = pd.to_datetime(df['date']).dt.date
        # 午前/午後の判定
        df['period'] = df['time'].apply(lambda x: '☀️ Morning (AM)' if 'AM' in str(x).upper() else '🌙 Afternoon (PM)')
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- サイドバー・フィルター ---
    st.sidebar.header("🌷 Search Filters")
    
    # 日付フィルター
    date_options = sorted(df['date'].unique())
    selected_dates = st.sidebar.multiselect(
        "Select Date", 
        options=date_options, 
        default=date_options,
        format_func=lambda x: x.strftime('%m/%d (%a)')
    )
    
    # 午前/午後フィルター
    period_options = ['☀️ Morning (AM)', '🌙 PM (Afternoon)']
    # データ内の表記に合わせるための変換
    selected_periods_raw = st.sidebar.multiselect(
        "Time of Day", 
        options=['☀️ Morning (AM)', '🌙 Afternoon (PM)'], 
        default=['☀️ Morning (AM)', '🌙 Afternoon (PM)']
    )

    # フィルタリング実行
    mask = (df['date'].isin(selected_dates)) & (df['period'].isin(selected_periods_raw))
    filtered_df = df[mask]

    # --- メインコンテンツ ---
    tab1, tab2 = st.tabs(["📍 Map View", "📝 List View"])

    with tab1:
        st.subheader(f"Found {len(filtered_df)} Events")
        # ズーム可能な地図
        st.map(filtered_df)

    with tab2:
        # 日付と時間でソート
        sorted_df = filtered_df.sort_values(by=['date', 'time'])
        for _, row in sorted_df.iterrows():
            with st.expander(f"【{row['city']}】 {row['name']} "):
                st.write(f"📅 **Date:** {row['date'].strftime('%b %d')}")
                st.write(f"⏰ **Time:** {row['time']}")
                st.write(f"📍 **Loc:** {row['location']}")
                
                # エラー回避のための .get() メソッド
                url = row.get('url', 'https://planomoms.com/easter-egg-hunts/')
                
                col1, col2 = st.columns(2)
                with col1:
                    st.link_button("Directions 🚗", f"https://www.google.com/maps/search/?api=1&query={row['lat']},{row['lon']}")
                with col2:
                    st.link_button("Official Site 🌐", url)
else:
    st.warning("Please check if 'easter_events.csv' is uploaded to GitHub.")
