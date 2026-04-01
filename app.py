import streamlit as st
import pandas as pd
import io

# 1. Page Config
st.set_page_config(page_title="Easter Scout 2026", page_icon="🐰", layout="wide")

# 2. Strong Data Loading (Force CSV split)
@st.cache_data
def load_data():
    try:
        # まずはファイルを文字列として直接読み込む
        with open("easter_events.csv", "r", encoding="utf-8-sig") as f:
            lines = f.readlines()
        
        # 1行目が引用符で囲まれている場合を想定し、中身を直接分解する
        header = lines[0].strip().replace('"', '').split(',')
        data = [line.strip().replace('"', '').split(',') for line in lines[1:]]
        
        # 強制的に正しい列名でデータフレームを作成
        df = pd.DataFrame(data)
        # 列数が合わない場合を想定し、見出しの数だけ採用
        df = df.iloc[:, :len(header)]
        df.columns = [h.strip().lower() for h in header]
        
        # 日付処理
        if 'date' in df.columns:
            df['date_dt'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date_dt'])
            # 緯度経度を数値に変換
            df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
            df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Read Error: {e}")
        return pd.DataFrame()

df = load_data()

# 3. Main UI
st.markdown("<h1 style='text-align: center; color: #7B68EE;'>🐰 Easter Scout 2026 🥚</h1>", unsafe_allow_html=True)

if not df.empty:
    # Sidebar Filters
    st.sidebar.header("🌷 Filters")
    date_options = sorted(df['date_dt'].unique())
    selected_dates = st.sidebar.multiselect(
        "Select Date", 
        options=date_options, 
        default=date_options,
        format_func=lambda x: x.strftime('%m/%d (%a)')
    )
    
    f_df = df[df['date_dt'].isin(selected_dates)]

    # Tabs
    tab1, tab2 = st.tabs(["📍 Map View", "📋 List View"])
    
    with tab1:
        if not f_df.empty:
            st.map(f_df)
    
    with tab2:
        # 1. データのコピーを作成
        show_df = f_df.copy()
        
        # 2. 【重要】元の 'date'（日付）から、曜日付きの新しい表示用データを作る
        # ※ 'date_dt' は読み込み時に日付型に変換したもの
        show_df['date_display'] = show_df['date_dt'].dt.strftime('%m/%d (%a)')
        
        # 3. 表示したい列のリスト（曜日付きの 'date_display' を指定）
        cols_to_show = ['name', 'date_display', 'time', 'location', 'city', 'url']
        
        # 4. CSVの中に存在する列だけを抽出（安全策）
        existing = [c for c in cols_to_show if c in show_df.columns]
        
        # 5. テーブルを表示
        st.dataframe(show_df[existing], use_container_width=True)
else:
    st.info("💡 Make sure to 'Clear Cache' and Refresh your browser!")
