import streamlit as st
import pandas as pd

# 1. ページ設定
st.set_page_config(page_title="Easter Scout 2026", page_icon="🐰", layout="wide")

# 2. データの読み込み（どんなCSVでも読み込む防弾仕様）
@st.cache_data
def load_data():
    try:
        # encoding='utf-8-sig' でExcel特有の目に見えない文字（BOM）を除去
        df = pd.read_csv("easter_events.csv", encoding='utf-8-sig')
        
        # 全ての列名から空白を除去し、小文字に統一
        df.columns = df.columns.str.strip().str.lower()
        
        # もし 'date' という列がなければ、最初に見つかった「日付っぽい列」を強制的に 'date' と命名
        if 'date' not in df.columns:
            # 1列目が日付である可能性が高いので、名前を無理やり変える
            df.rename(columns={df.columns[1]: 'date'}, inplace=True)
        
        # 日付変換（エラーは空欄にする）
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
        df = df.dropna(subset=['date'])
        
        # lat/lon, url なども同様にクリーンアップ
        for col in ['lat', 'lon', 'url', 'time', 'city', 'name']:
            if col not in df.columns:
                df[col] = "Check Website" if col == 'url' else "N/A"
        
        return df
    except Exception as e:
        st.error(f"Critical Error: {e}")
        return pd.DataFrame()

df = load_data()

# --- メイン表示 ---
if not df.empty:
    st.title("🐰 Easter Scout 2026")
    
    # フィルター設定
    st.sidebar.header("🌷 Filters")
    date_list = sorted(df['date'].unique())
    sel_dates = st.sidebar.multiselect("Select Date", options=date_list, default=date_list)
    
    # フィルタリング
    f_df = df[df['date'].isin(sel_dates)]

    # 地図とリストの表示
    tab1, tab2 = st.tabs(["📍 Map View", "📋 List View"])
    with tab1:
        st.map(f_df)
    with tab2:
        st.dataframe(f_df[['name', 'date', 'time', 'location', 'city']])
else:
    st.warning("⚠️ Still having trouble reading 'easter_events.csv'. Please check the file on GitHub.")
