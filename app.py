import streamlit as st
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="Easter Scout 2026", page_icon="🐰", layout="wide")

# 2. Data Loading (防御力を最大に)
@st.cache_data
def load_data():
    try:
        # BOM対策、空白対策をして読み込み
        df = pd.read_csv("easter_events.csv", encoding='utf-8-sig')
        # 全ての列名を小文字にして空白を消す
        df.columns = df.columns.str.strip().str.lower()
        
        # 'date'列を日付型に変換。失敗した行は消す
        if 'date' in df.columns:
            df['date_dt'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date_dt'])
            return df
        else:
            # date列が見つからない場合、列名を表示してデバッグしやすくする
            st.error(f"Found columns: {list(df.columns)}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"File Load Error: {e}")
        return pd.DataFrame()

df = load_data()

# --- UI ---
st.title("🐰 Easter Scout 2026")

# データが正しく読み込めている場合のみメイン処理を行う
if not df.empty and 'date_dt' in df.columns:
    # Sidebar Filters
    st.sidebar.header("🌷 Filters")
    
    date_options = sorted(df['date_dt'].unique())
    selected_dates = st.sidebar.multiselect(
        "Select Date", 
        options=date_options, 
        default=date_options,
        format_func=lambda x: x.strftime('%m/%d (%a)')
    )
    
    # フィルタリング
    f_df = df[df['date_dt'].isin(selected_dates)]

    # Tabs
    tab_map, tab_list = st.tabs(["📍 Map View", "📋 List View"])
    
    with tab_map:
        if 'lat' in f_df.columns and 'lon' in f_df.columns:
            st.map(f_df)
        else:
            st.warning("Location coordinates (lat/lon) not found.")

    with tab_list:
        # 表示用に曜日付きの日付を作成
        show_df = f_df.copy()
        show_df['date_display'] = show_df['date_dt'].dt.strftime('%m/%d (%a)')
        
        # 存在する列だけを表示（'date'の代わりに'date_display'を表示）
        cols_to_show = ['name', 'date_display', 'time', 'location', 'city', 'url']
        existing = [c for c in cols_to_show if c in show_df.columns]
        
        st.dataframe(show_df[existing], use_container_width=True)

else:
    # 読み込み失敗時のメッセージ
    st.info("💡 Please check your 'easter_events.csv' file on GitHub.")
    st.write("The first row must be: `name,date,time,location,city,lat,lon,url` (no spaces after commas)")
