import streamlit as st
import pandas as pd

# データの読み込み（キャッシュを使わずに強制的に最新を見に行く設定）
def load_data():
    try:
        # sep=None を使うことで、カンマでもセミコロンでも自動判別します
        df = pd.read_csv("easter_events.csv", sep=None, engine='python', encoding='utf-8-sig')
        # 全ての列名を小文字＋空白削除
        df.columns = df.columns.str.strip().str.lower()
        
        # 'date'列を日付型に
        if 'date' in df.columns:
            df['date_dt'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date_dt'])
            # 曜日付きの表示用列を作成
            df['display_date'] = df['date_dt'].dt.strftime('%m/%d (%a)')
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

df = load_data()

# --- 以降、表示処理 ---
if not df.empty:
    st.title("🐰 Easter Scout 2026 🥚")
    # ここに以前作成したマップやリストのコードが続きます...
    st.map(df)
    st.dataframe(df[['name', 'display_date', 'time', 'location', 'city']])
else:
    st.info("Loading latest data... Please check your CSV on GitHub.")
