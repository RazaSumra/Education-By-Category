import streamlit as st
import pandas as pd
import plotly.express as px
import json
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(
    page_title="India Education Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    return pd.read_csv("education_state_income_detailed.csv")

@st.cache_data
def load_geojson():
    with open("india.json", "r") as f:
        return json.load(f)

df = load_data()
india_geojson = load_geojson()

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Space Grotesk', sans-serif;
        }

        .stApp {
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: #e2e8f0;
        }

        .stPlotlyChart, .stSelectbox, .stTextInput, .stMetric, .metric-card {
            background: rgba(30, 41, 59, 0.7) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(6px);
            padding: 10px;
        }

        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px -5px rgba(125, 211, 252, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 India Education Dashboard")
st.subheader("Statewise Education Data by Income Class")

col1, col2 = st.columns([1, 3])
with col1:
    selected_state = st.selectbox("Select State", options=df['State'].unique())

with col2:
    st.markdown("Education Data Visualization Across Income Classes")

state_df = df[df['State'] == selected_state]

m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    avg_lit = state_df['Literacy Rate (%)'].mean()
    st.metric("Avg Literacy", f"{avg_lit:.1f}%")

with m2:
    primary = state_df['Primary (%)'].mean()
    st.metric("Primary", f"{primary:.1f}%", delta=f"{primary - avg_lit:.1f}%")

with m3:
    secondary = state_df['Secondary (%)'].mean()
    st.metric("Secondary", f"{secondary:.1f}%", delta=f"{secondary - primary:.1f}%")

with m4:
    higher_sec = state_df['Higher Secondary (%)'].mean()
    st.metric("Higher Sec", f"{higher_sec:.1f}%", delta=f"{higher_sec - secondary:.1f}%")

with m5:
    grad = state_df['Graduation (%)'].mean()
    st.metric("Graduation", f"{grad:.1f}%", delta=f"{grad - higher_sec:.1f}%")

style_metric_cards(
    background_color="rgba(30, 41, 59, 0.7)",
    border_color="rgba(255,255,255,0.1)",
    box_shadow="0 4px 6px -1px rgba(0,0,0,0.2)"
)

tab1, tab2, tab3 = st.tabs(["📈 Trends", "🗺 State Map", "⚠️ Issues"])

with tab1:
    fig = px.line(
        state_df,
        x="Income Class",
        y=["Primary (%)", "Secondary (%)", "Higher Secondary (%)", "Graduation (%)"],
        markers=True,
        title=f"Education Progression in {selected_state}",
        template="plotly_dark",
        color_discrete_sequence=["#7dd3fc", "#38bdf8", "#0ea5e9", "#0369a1"]
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    state_avg = df.groupby("State")[["Literacy Rate (%)"]].mean().reset_index()

    fig_map = px.choropleth(
        state_avg,
        geojson=india_geojson,
        featureidkey="properties.st_nm",
        locations="State",
        color="Literacy Rate (%)",
        color_continuous_scale="Blues",
        title="Literacy Rate by State",
    )

    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_map, use_container_width=True)

with tab3:
    st.subheader(f"Issues Faced in {selected_state}")
    for income_class in state_df['Income Class'].unique():
        issue = state_df[state_df['Income Class'] == income_class]['Issues Faced'].values[0]
        st.markdown(f"""
        <div class="metric-card" style="margin-bottom: 10px;">
            <h4 style="color: #7dd3fc;">{income_class} Class</h4>
            <p>{issue}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#38bdf8;'>Made with ❤️ using Streamlit | Updated 2023</p>",
    unsafe_allow_html=True
)

