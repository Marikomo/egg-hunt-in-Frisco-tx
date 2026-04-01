import streamlit as st
import pandas as pd
import io

# 1. ページ設定
st.set_page_config(page_title="Easter Scout 2026", page_icon="🐰", layout="wide")

# 2. データの読み込み (最強の防御力)
def load_data():
    try:
        # ファイルを開いて中身を直接確認
        with open("easter_events.csv", "r", encoding="utf-8-sig") as f:
            content = f.read()
        
        # カンマ、セミコロン、タブなど、どんな区切りでも自動判別して読み込む
        df = pd.read_csv(io.StringIO(content), sep=None, engine='python')
        
        # 全ての列名を「小文字＋空白なし」に統一
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # 'date'列を日付型に変換。失敗した行（空行など）は消す
        if 'date' in df.columns:
            df['date_dt'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date_dt'])
            # 曜日付きの表示用列を作成 "03/28 (Sat)"
            df['display_date'] = df['date_dt'].dt.strftime('%m/%d (%a)')
            return df
        else:
            # デバッグ用：今認識している列名を表示
            st.error(f"Debug: Found columns {list(df.columns)}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Read Error: {e}")
        return pd.DataFrame()

# キャッシュを介さず読み込む
df = load_data()

# --- UI表示 ---
st.markdown("<h1 style='text-align: center; color: #7B68EE;'>🐰 Easter Scout 2026 🥚</h1>", unsafe_allow_html=True)

if not df.empty and 'date_dt' in df.columns:
    # サイドバー・フィルター
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

    # タブ表示
    tab1, tab2 = st.tabs(["📍 Map View", "📋 List View"])
    
    with tab1:
        if 'lat' in f_df.columns and 'lon' in f_df.columns:
            st.map(f_df)
        else:
            st.warning("Latitude/Longitude data not found in CSV.")
    
    with tab2:
        # 表示する列を動的に選択（存在する物だけ）
        cols = ['name', 'display_date', 'time', 'location', 'city', 'url']
        existing = [c for c in cols if c in f_df.columns]
        st.dataframe(f_df[existing], use_container_width=True)

else:
    st.info("💡 Please refresh the page or check your CSV format on GitHub.")
