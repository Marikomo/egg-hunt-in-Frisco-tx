import streamlit as st
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="Easter Scout 2026", page_icon="🐰", layout="wide")

# 2. Advanced Data Loading (Error-Proof)
@st.cache_data
def load_data():
    try:
        # Read CSV with BOM handling
        df = pd.read_csv("easter_events.csv", encoding='utf-8-sig')
        # Standardize column names (lowercase & no spaces)
        df.columns = df.columns.str.strip().str.lower()
        
        # Ensure 'date' column exists for filtering
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
            df = df.dropna(subset=['date'])
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

# --- Main App ---
st.title("🐰 Easter Scout 2026")

if not df.empty:
    # Sidebar Filter
    st.sidebar.header("🌷 Filters")
    if 'date' in df.columns:
        date_list = sorted(df['date'].unique())
        sel_dates = st.sidebar.multiselect("Select Date", options=date_list, default=date_list)
        f_df = df[df['date'].isin(sel_dates)]
    else:
        f_df = df

    # Tabs
    tab_map, tab_list = st.tabs(["📍 Map View", "📋 List View"])
    
    with tab_map:
        # Only show map if lat/lon exist
        if 'lat' in f_df.columns and 'lon' in f_df.columns:
            st.map(f_df)
        else:
            st.warning("Location data (lat/lon) missing in CSV.")

    with tab_list:
        # ERROR FIX: Only show columns that actually exist in your CSV
        cols_to_show = ['name', 'date', 'time', 'location', 'city', 'url']
        existing_cols = [c for c in cols_to_show if c in f_df.columns]
        
        if existing_cols:
            st.subheader("Event List")
            st.dataframe(f_df[existing_cols], use_container_width=True)
        else:
            st.write("Full data table:")
            st.dataframe(f_df) # Show everything if specific columns aren't found
            
else:
    st.warning("⚠️ CSV data could not be loaded. Please check 'easter_events.csv' on GitHub.")
