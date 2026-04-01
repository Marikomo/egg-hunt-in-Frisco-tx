import streamlit as st
import pandas as pd
import io

# 1. ページ設定
st.set_page_config(page_title="Easter Scout 2026", page_icon="🐰", layout="wide")

# 2. データの読み込み (区切り文字を自動判別する最強版)
@st.cache_data
def load_data():
    try:
        # sep=None, engine='python' を使うと、pandasが自動で区切り文字を判別します
        df = pd.read_csv("easter_events.csv", sep=None, engine='python', encoding='utf-8-sig')
        
        # 列名のクリーニング（空白削除・小文字化）
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # date列を日付型に変換
        if 'date' in df.columns:
            df['date_dt'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date_dt']) # 変換に失敗した行（空行など）を除去
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

df = load_data()

# --- UI表示 ---
st.markdown("<h1 style='text-align: center; color: #7B68EE;'>🐰 Easter Scout 2026 🥚</h1>", unsafe_allow_html=True)

if not df.empty and 'date_dt' in df.columns:
    # フィルター設定
    st.sidebar.header("🌷 Filters")
    date_options = sorted(df['date_dt'].unique())
    selected_dates = st.sidebar.multiselect(
        "Select Date", 
        options=date_options, 
        default=date_options,
        format_func=lambda x: x.strftime('%m/%d (%a)')
    )
    
    f_df = df[df['date_dt'].isin(selected_dates)]

    # タブ表示
    tab1, tab2 = st.tabs(["📍 Map View", "📋 List View"])
    
    with tab1:
        # 地図。lat/lonがあれば表示
        if 'lat' in f_df.columns and 'lon' in f_df.columns:
            st.map(f_df)
    
    with tab2:
        # 表示用に曜日付きの日付を作成
        show_df = f_df.copy()
        show_df['date_with_day'] = show_df['date_dt'].dt.strftime('%m/%d (%a)')
        
        # リストに表示する列（存在する物だけ）
        display_cols = ['name', 'date_with_day', 'time', 'location', 'city', 'url']
        actual_cols = [c for c in display_cols if c in show_df.columns]
        st.dataframe(show_df[actual_cols], use_container_width=True)

else:
    st.info("💡 Make sure 'easter_events.csv' is saved as a standard CSV (Comma Separated).")
