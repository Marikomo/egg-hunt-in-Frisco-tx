import streamlit as st
import pandas as pd

# 1. Page Config
st.set_page_config(
    page_title="Easter Scout 2026",
    page_icon="🐰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Modern Pastel UI (CSS)
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Varela+Round&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"] {
        font-family: 'Varela Round', sans-serif;
    }
    .main {
        background-color: #FFFFFF;
    }
    /* Header Style */
    .hero {
        background: linear-gradient(135deg, #FFF0F5 0%, #E6E6FA 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 20px;
        border: 2px dashed #FFB6C1;
    }
    h1 { color: #6A5ACD !important; font-size: 2.2rem !important; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
    }
    /* Button Style */
    div.stButton > button {
        background-color: #B2FAB4 !important; /* Pastel Green */
        color: #4B0082 !important;
        border-radius: 15px !important;
        border: none !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Hero Section
st.markdown("""
    <div class="hero">
        <span>🐰 🥚 🌸</span>
        <h1>Easter Scout 2026</h1>
        <p style="color: #888;">Find the best Egg Hunts in North Texas</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Data Loading
@st.cache_data
def load_data():
    df = pd.read_csv("easter_events.csv")
    df['date'] = pd.to_datetime(df['date'])
    # Add AM/PM Period for filtering
    df['period'] = df['time'].apply(lambda x: 'Morning' if 'AM' in x.upper() else 'Afternoon')
    return df

try:
    df = load_data()

    # --- Sidebar Filters ---
    st.sidebar.title("🔍 Search Filters")
    
    cities = st.sidebar.multiselect("Select City", options=sorted(df['city'].unique()), default=sorted(df['city'].unique()))
    
    periods = st.sidebar.multiselect("Time of Day", options=['Morning', 'Afternoon'], default=['Morning', 'Afternoon'])

    # Filtering Logic
    mask = (df['city'].isin(cities)) & (df['period'].isin(periods))
    filtered_df = df[mask]

    # --- Main UI Tabs ---
    tab_map, tab_list = st.tabs(["📍 Map View", "📝 List View"])

    with tab_map:
        st.map(filtered_df)
        st.caption("Pinch to zoom. Tap markers for details.")

    with tab_list:
        if filtered_df.empty:
            st.warning("No events found. Try adjusting the filters!")
        else:
            # Sort by date and time
            sorted_df = filtered_df.sort_values(by=['date', 'time'])
            
            for index, row in sorted_df.iterrows():
                with st.expander(f"{row['name']} | {row['city']}"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"📅 **Date:** {row['date'].strftime('%A, %b %d')}")
                        st.write(f"⏰ **Time:** {row['time']}")
                        st.write(f"📍 **Location:** {row['location']}")
                    with col2:
                        map_link = f"https://www.google.com/maps/search/?api=1&query={row['lat']},{row['lon']}"
                        st.link_button("Directions 🚗", map_link)
                        st.link_button("Official Site 🌐", row['url'])

except Exception as e:
    st.error("Error loading data. Please check your 'easter_events.csv' file.")
