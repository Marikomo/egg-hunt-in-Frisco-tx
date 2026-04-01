import streamlit as st
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="Easter Scout 2026", page_icon="🐰", layout="wide")

# 2. Data Loading
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("easter_events.csv", encoding='utf-8-sig')
        df.columns = df.columns.str.strip().str.lower()
        if 'date' in df.columns:
            # 日付型に変換
            df['date_dt'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date_dt'])
            # 【UXポイント】表示用の曜日付き文字列を作成 "03/28 (Sat)"
            df['display_date'] = df['date_dt'].dt.strftime('%m/%d (%a)')
        return df
    except:
        return pd.DataFrame()

df = load_data()

# --- UI ---
st.title("🐰 Easter Scout 2026")

if not df.empty:
    # Sidebar Filters
    st.sidebar.header("🌷 Filters")
    
    # フィルターの選択肢も曜日付きにする
    date_options = sorted(df['date_dt'].unique())
    selected_dates = st.sidebar.multiselect(
        "Select Date", 
        options=date_options, 
        default=date_options,
        format_func=lambda x: x.strftime('%m/%d (%a)') # フィルター内も曜日表示
    )
    
    # 午前/午後フィルター
    if 'time' in df.columns:
        df['period'] = df['time'].apply(lambda x: '☀️ AM' if 'AM' in str(x).upper() else '🌙 PM')
        selected_periods = st.sidebar.multiselect("Time", options=['☀️ AM', '🌙 PM'], default=['☀️ AM', '🌙 PM'])
        f_df = df[(df['date_dt'].isin(selected_dates)) & (df['period'].isin(selected_periods))]
    else:
        f_df = df[df['date_dt'].isin(selected_dates)]

    # Tabs
    tab_map, tab_list = st.tabs(["📍 Map View", "📝 List View"])
    
    with tab_map:
        st.map(f_df)

    with tab_list:
        # リスト表示でも曜日を出す
        show_df = f_df.sort_values('date_dt').copy()
        # カラム名を整理して表示
        if 'display_date' in show_df.columns:
            # 元の'date'を曜日付きの'display_date'に置き換えて見やすく
            show_df['date'] = show_df['display_date']
            
        cols_to_show = ['name', 'date', 'time', 'location', 'city', 'url']
        existing_cols = [c for c in cols_to_show if c in show_df.columns]
        st.dataframe(show_df[existing_cols], use_container_width=True)

else:
    st.warning("Please check your 'easter_events.csv' on GitHub.")
