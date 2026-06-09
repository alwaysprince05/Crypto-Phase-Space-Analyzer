import streamlit as st
import plotly.graph_objects as go
import numpy as np

from data_loader import download_btc_data, get_close_prices
from state_space import compute_phase_space

st.set_page_config(page_title="Crypto Phase Space", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Premium HFT Glassmorphism look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }

    /* Subtle radial gradient background */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #1a1f35 0%, #090a0f 100%);
    }

    /* Glassmorphism cards */
    .metric-card {
        background: rgba(20, 24, 36, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 24px 20px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 255, 255, 0.15);
    }

    .metric-value-up {
        color: #00FF88;
        font-size: 34px;
        font-weight: 800;
        text-shadow: 0px 0px 20px rgba(0, 255, 136, 0.2);
        margin: 10px 0 5px 0;
        line-height: 1.1;
    }

    .metric-value-down {
        color: #FF2A5F;
        font-size: 34px;
        font-weight: 800;
        text-shadow: 0px 0px 20px rgba(255, 42, 95, 0.2);
        margin: 10px 0 5px 0;
        line-height: 1.1;
    }

    .metric-label {
        color: #8C9BB4;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }

    .metric-subtext {
        font-size: 14px;
        font-weight: 600;
    }

    /* Titles */
    h1 {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px;
        text-align: center;
        padding-top: 2rem;
    }
    
    .subtitle {
        text-align: center;
        color: #8C9BB4;
        font-size: 18px;
        margin-bottom: 40px;
        font-weight: 300;
        letter-spacing: 1px;
    }

    /* Hide default header */
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚡ CRYPTO PHASE SPACE</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>High-Frequency Dynamics & Market Trajectory</div>", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_data():
    df = download_btc_data()
    prices = get_close_prices(df)
    log_returns, velocity, acceleration = compute_phase_space(prices)
    return df, prices, log_returns, velocity, acceleration

with st.spinner("Synchronizing real-time market data..."):
    df, prices, log_returns, velocity, acceleration = load_data()

latest_price = prices[-1]
prev_price = prices[-2]
price_change = latest_price - prev_price
price_change_pct = (price_change / prev_price) * 100

latest_return = log_returns[-1]
latest_velocity = velocity[-1]
latest_accel = acceleration[-1]

def format_metric(label, value, is_pct=False):
    color_class = "metric-value-up" if value >= 0 else "metric-value-down"
        
    val_str = f"{value:.4f}"
    if is_pct:
        val_str += "%"
        
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="{color_class}">{val_str}</div>
    </div>
    """

cols = st.columns(4)

with cols[0]:
    price_color = "metric-value-up" if price_change >= 0 else "metric-value-down"
    sub_color = "#00FF88" if price_change >= 0 else "#FF2A5F"
    arrow = "▲" if price_change >= 0 else "▼"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">BTC/USD PRICE</div>
        <div class="{price_color}">${latest_price:,.2f}</div>
        <div class="metric-subtext" style="color: {sub_color};">
            {arrow} {abs(price_change_pct):.2f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with cols[1]:
    st.markdown(format_metric("Log Return (Daily)", latest_return), unsafe_allow_html=True)

with cols[2]:
    st.markdown(format_metric("Velocity", latest_velocity), unsafe_allow_html=True)

with cols[3]:
    st.markdown(format_metric("Acceleration", latest_accel), unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 3D Phase Space Trajectory Plotly Chart
fig = go.Figure()

x = log_returns
y = velocity
z = acceleration
n = len(x)
colors = np.linspace(0, 1, n)

fig.add_trace(go.Scatter3d(
    x=x, y=y, z=z,
    mode='lines+markers',
    marker=dict(
        size=4,
        color=colors,
        colorscale='Turbo',
        opacity=0.9,
        line=dict(width=0)
    ),
    line=dict(
        color=colors,
        colorscale='Turbo',
        width=5
    ),
    hovertemplate="<b>Return:</b> %{x:.4f}<br><b>Velocity:</b> %{y:.4f}<br><b>Accel:</b> %{z:.4f}<extra></extra>"
))

# Sleek layout for Plotly
fig.update_layout(
    scene=dict(
        xaxis_title='LOG RETURN',
        yaxis_title='VELOCITY',
        zaxis_title='ACCELERATION',
        xaxis=dict(
            showbackground=False, 
            gridcolor='rgba(255,255,255,0.05)', 
            zerolinecolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#8C9BB4')
        ),
        yaxis=dict(
            showbackground=False, 
            gridcolor='rgba(255,255,255,0.05)', 
            zerolinecolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#8C9BB4')
        ),
        zaxis=dict(
            showbackground=False, 
            gridcolor='rgba(255,255,255,0.05)', 
            zerolinecolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#8C9BB4')
        ),
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#8C9BB4', family="Outfit, sans-serif"),
    height=800
)

st.plotly_chart(fig, width='stretch')
