import streamlit as st
import pandas as pd
import io

# 1. ページ設定
st.set_page_config(page_title="Easter Scout 2026", page_icon="🐰", layout="wide")

# 2. データの読み込み (区切りエラーを強制修正する最強版)
@st.cache_data
def load_data():
    try:
        # まずは普通に読み込む
        df = pd.read_csv("easter_events.csv", encoding='utf-8-sig')
        
        # 【最重要：修正ポイント】
        # もし1列目にカンマが含まれていたら、それは区切りに失敗しているので強制分割する
        if len(df.columns) == 1 or 'name,date' in str(df.columns[0]):
            # 文字列として読み込み直し、明示的にカンマで区切る
            df = pd.read_csv("easter_events.csv", sep=',', encoding='utf-8-sig', on_bad_lines='skip')
        
        # 列名の空白除去と小文字化
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # date列を日付型に変換
        if 'date' in df.columns:
            df['date_dt'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date_dt'])
            return df
        else:
            # まだ解決しない場合はデバッグ情報を出す
            st.error(f"Debug: Still finding columns {list(df.columns)}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Read Error: {e}")
        return pd.DataFrame()

df = load_data()

# 3. メイン表示 (パステルカラーデザイン)
st.markdown("<h1 style='text-align: center; color: #7B68EE;'>🐰 Easter Scout 2026 🥚</h1>", unsafe_allow_html=True)

if not df.empty and 'date_dt' in df.columns:
    # 曜日付きの日付を作成
    df['display_date'] = df['date_dt'].dt.strftime('%m/%d (%a)')
    
    # フィルター (サイドバー)
    st.sidebar.header("🌷 Filters")
    date_list = sorted(df['date_dt'].unique())
    sel_dates = st.sidebar.multiselect(
        "Select Date", 
        options=date_options, 
        default=date_options, 
        format_func=lambda x: x.strftime('%m/%d (%a)')
    )
    
    f_df = df[df['date_dt'].isin(sel_dates)]

    # タブ
    tab1, tab2 = st.tabs(["📍 Map View", "📋 List View"])
    with tab1:
        # lat/lon列が存在するかチェックして地図を表示
        if 'lat' in f_df.columns and 'lon' in f_df.columns:
            st.map(f_df)
    with tab2:
        # 表示する列を動的に選択
        cols = ['name', 'display_date', 'time', 'location', 'city', 'url']
        existing = [c for c in cols if c in f_df.columns]
        st.dataframe(f_df[existing], use_container_width=True)
else:
    st.info("💡 Please refresh the page after updating the code in GitHub!")
