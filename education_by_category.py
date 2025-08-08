import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import json
import pydeck as pdk
from streamlit_extras.stylable_container import stylable_container
from streamlit.components.v1 import html

st.set_page_config(
    page_title="Cosmic Education Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-color: #0f172a;
        --card-color: rgba(30, 41, 59, 0.7);
        --text-color: #e2e8f0;
        --accent-color: #7dd3fc;
        --secondary-color: #38bdf8;
    }

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, #020617 100%) !important;
        background-image: url('https://i.imgur.com/JtQ6W0a.jpg') !important;
        background-size: cover !important;
        background-blend-mode: overlay !important;
    }

    #particles-js {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        opacity: 0.3;
    }
</style>

<div id="particles-js"></div>
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script>
    particlesJS("particles-js", {
        "particles": {
            "number": {"value": 80, "density": {"enable": true, "value_area": 800}},
            "color": {"value": "#7dd3fc"},
            "shape": {"type": "circle"},
            "opacity": {"value": 0.5, "random": true},
            "size": {"value": 3, "random": true},
            "line_linked": {"enable": true, "distance": 150, "color": "#7dd3fc", "opacity": 0.4, "width": 1},
            "move": {"enable": true, "speed": 2, "direction": "none", "random": true, "straight": false, "out_mode": "out"}
        },
        "interactivity": {
            "events": {"onhover": {"enable": true, "mode": "repulse"}}
        }
    });
</script>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("education_state_income_detailed.csv")

df = load_data()

def render_3d_map():
    india_geojson = "https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson"
    map_layer = pdk.Layer(
        "PolygonLayer",
        data=india_geojson,
        get_polygon="coordinates",
        extruded=True,
        get_elevation="properties.literacy_rate * 1000",
        get_fill_color="[255, (1 - properties.literacy_rate) * 255, 100]",
        pickable=True,
        auto_highlight=True
    )
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=pdk.ViewState(
            latitude=20.5937,
            longitude=78.9629,
            zoom=4,
            pitch=45
        ),
        layers=[map_layer],
        tooltip={"text": "State: {NAME_1}\nLiteracy: {literacy_rate}%"},
        height=600
    ))

def metric_card(title, value, delta=None, unique_key=None):
    with stylable_container(
        key=f"holographic-card-{unique_key}",
        css_styles="""
        {
            background: rgba(125, 211, 252, 0.15) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(125, 211, 252, 0.3) !important;
            box-shadow: 0 0 15px rgba(125, 211, 252, 0.5) !important;
            backdrop-filter: blur(5px) !important;
            padding: 20px !important;
            transition: all 0.3s ease !important;
        }
        :hover {
            transform: translateY(-5px) !important;
            box-shadow: 0 0 25px rgba(125, 211, 252, 0.8) !important;
        }
        """
    ):
        st.metric(title, value, delta)

st.title("🌌 Cosmic Education Dashboard")
st.markdown("""
<div style="color: var(--accent-color); font-size: 1.1rem;">
    Interactive visualization of education metrics with futuristic UI
</div>
""", unsafe_allow_html=True)

selected_state = st.selectbox(
    "Select State",
    options=df['State'].unique(),
    key="state_selector"
)

state_df = df[df['State'] == selected_state]
avg_literacy = state_df['Literacy Rate (%)'].mean()
primary_avg = state_df['Primary (%)'].mean()
secondary_avg = state_df['Secondary (%)'].mean()
higher_sec_avg = state_df['Higher Secondary (%)'].mean()
grad_avg = state_df['Graduation (%)'].mean()

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    metric_card("🚀 Literacy Rate", f"{avg_literacy:.1f}%", unique_key="1")
with col2:
    metric_card("📚 Primary", f"{primary_avg:.1f}%", f"{(primary_avg - avg_literacy):.1f}%", unique_key="2")
with col3:
    metric_card("🎓 Secondary", f"{secondary_avg:.1f}%", f"{(secondary_avg - primary_avg):.1f}%", unique_key="3")
with col4:
    metric_card("🏛️ Higher Sec", f"{higher_sec_avg:.1f}%", f"{(higher_sec_avg - secondary_avg):.1f}%", unique_key="4")
with col5:
    metric_card("🎓 Graduation", f"{grad_avg:.1f}%", f"{(grad_avg - higher_sec_avg):.1f}%", unique_key="5")

st.subheader("🗺️ Interactive 3D India Map")
render_3d_map()

tab1, tab2, tab3 = st.tabs(["📈 Trends", "📊 Comparison", "⚠️ Challenges"])

with tab1:
    fig = px.line(
        state_df, 
        x="Income Class", 
        y=["Primary (%)", "Secondary (%)", "Higher Secondary (%)", "Graduation (%)"],
        title=f"Education Progression in {selected_state}",
        template="plotly_dark",
        color_discrete_sequence=["#7dd3fc", "#38bdf8", "#0ea5e9", "#0369a1"],
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = px.bar(
        state_df,
        x="Income Class",
        y=["Primary (%)", "Secondary (%)", "Higher Secondary (%)", "Graduation (%)"],
        title=f"Income Class Comparison in {selected_state}",
        barmode="group",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    for idx, income_class in enumerate(state_df['Income Class'].unique()):
        issues = state_df[state_df['Income Class'] == income_class]['Issues Faced'].values[0]
        with stylable_container(
            key=f"challenge-card-{idx}",
            css_styles="""
            {
                background: rgba(30, 41, 59, 0.7) !important;
                border-radius: 12px !important;
                border: 1px solid rgba(255, 0, 0, 0.3) !important;
                box-shadow: 0 0 15px rgba(255, 0, 0, 0.3) !important;
                padding: 15px !important;
                margin-bottom: 15px !important;
            }
            """
        ):
            st.markdown(f"""
            <h3 style="color: #f87171; margin-bottom: 5px;">{income_class} Class Challenges</h3>
            <p style="color: var(--text-color);">{issues}</p>
            """, unsafe_allow_html=True)

st.markdown("---")
st_lottie("https://assets1.lottiefiles.com/packages/lf20_q5qeoo3q.json", height=100)
st.markdown("""
<div style="text-align: center; color: var(--accent-color);">
    Cosmic Education Dashboard • Made with Streamlit • 2023
</div>
""", unsafe_allow_html=True)

html("""
<script>
    document.addEventListener('click', function(e) {
        const ripple = document.createElement('div');
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(125, 211, 252, 0.5);
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
        `;
        document.body.appendChild(ripple);

        const diameter = Math.max(e.target.clientWidth, e.target.clientHeight);
        ripple.style.width = ripple.style.height = `${diameter}px`;
        ripple.style.left = `${e.clientX - diameter/2}px`;
        ripple.style.top = `${e.clientY - diameter/2}px`;

        setTimeout(() => ripple.remove(), 600);
    });
</script>
""")


