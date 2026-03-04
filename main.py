import streamlit as st
import requests

# ============================================================
#   WEATHER APP — STREAMLIT VERSION
#   Codespaces mein run karo:
#   pip install streamlit requests
#   streamlit run weather_app.py
# ============================================================

API_KEY = "1f1d9ef37d3321cc8251e999ab560086"   # ⚠️ Purani key delete karke nayi dalo

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Weather Terminal",
    page_icon="🌤️",
    layout="centered"
)

# ── Custom CSS — Dark glassmorphism theme ─────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Syne:wght@400;700;800&display=swap');

/* Background */
.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #0d1117 40%, #0a0f1e 100%);
    font-family: 'JetBrains Mono', monospace;
}

/* Hide streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 700px; }

/* Title */
.weather-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #00d4ff, #0099cc, #00ffcc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 4px;
    margin-bottom: 0.2rem;
}

.weather-subtitle {
    text-align: center;
    color: #4a5568;
    font-size: 0.75rem;
    letter-spacing: 2px;
    margin-bottom: 2rem;
}

/* City banner card */
.city-banner {
    background: linear-gradient(135deg, rgba(0,212,255,0.08), rgba(0,153,204,0.05));
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 16px;
    padding: 1.8rem;
    text-align: center;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
}

.city-name {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #00d4ff;
    margin: 0;
}

.city-condition {
    font-size: 1rem;
    color: #718096;
    margin-top: 0.3rem;
    letter-spacing: 1px;
}

.city-icon {
    font-size: 3rem;
    margin-bottom: 0.5rem;
}

/* Metric cards */
.metric-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    margin-bottom: 0.8rem;
    transition: border-color 0.3s;
}

.metric-card:hover {
    border-color: rgba(0,212,255,0.3);
}

.metric-label {
    font-size: 0.7rem;
    color: #4a5568;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

.metric-value {
    font-size: 1.6rem;
    font-weight: 700;
    margin: 0;
}

.metric-sub {
    font-size: 0.75rem;
    color: #718096;
    margin-top: 0.2rem;
}

/* Temperature specific */
.temp-hot   { color: #ff6b6b; }
.temp-warm  { color: #ffd93d; }
.temp-cool  { color: #00d4ff; }
.temp-cold  { color: #74b9ff; }

/* Humidity bar */
.humidity-bar-bg {
    background: rgba(255,255,255,0.05);
    border-radius: 999px;
    height: 8px;
    margin: 0.5rem 0;
    overflow: hidden;
}

.humidity-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #00d4ff, #00ffcc);
    transition: width 1s ease;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 1.5rem 0;
}

/* Input styling */
.stTextInput > div > div > input {
    background: #1a1f2e;
    border: 1px solid rgba(0,212,255,0.2) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.95rem !important;
}

.stTextInput > div > div > input::placeholder {
    color: #718096 !important;
    opacity: 1 !important;
}

.stTextInput > div > div > input:focus {
    border-color: rgba(0,212,255,0.6) !important;
    box-shadow: 0 0 0 2px rgba(0,212,255,0.1) !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #00d4ff, #0099cc) !important;
    color: #0a0a0f !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    letter-spacing: 2px !important;
    font-size: 0.85rem !important;
    width: 100% !important;
    padding: 0.6rem !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #00ffcc, #00d4ff) !important;
    transform: translateY(-1px);
}

/* Error */
.error-box {
    background: rgba(255,107,107,0.08);
    border: 1px solid rgba(255,107,107,0.3);
    border-radius: 10px;
    padding: 1rem;
    color: #ff6b6b;
    text-align: center;
    font-size: 0.85rem;
}

/* Footer */
.footer {
    text-align: center;
    color: #2d3748;
    font-size: 0.7rem;
    letter-spacing: 1px;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


# ── Weather Icons ─────────────────────────────────────────────
WEATHER_ICONS = {
    "Clear":        "☀️",
    "Clouds":       "⛅",
    "Rain":         "🌧️",
    "Drizzle":      "🌦️",
    "Thunderstorm": "⛈️",
    "Snow":         "❄️",
    "Mist":         "🌫️",
    "Fog":          "🌫️",
    "Haze":         "🌫️",
    "Smoke":        "💨",
    "Dust":         "🌪️",
    "Tornado":      "🌪️",
}

def get_icon(condition: str) -> str:
    for key in WEATHER_ICONS:
        if key.lower() in condition.lower():
            return WEATHER_ICONS[key]
    return "🌡️"

def get_temp_class(temp: float) -> str:
    if temp <= 10: return "temp-cold"
    if temp <= 20: return "temp-cool"
    if temp <= 30: return "temp-warm"
    return "temp-hot"

def wind_label(speed: float) -> str:
    if speed < 5:  return "🍃 Calm"
    if speed < 15: return "💨 Breezy"
    if speed < 30: return "🌬️ Windy"
    return "🌪️ Strong Wind"


# ── API Call ──────────────────────────────────────────────────
def get_weather(city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("cod") != 200:
            return None, data.get("message", "City not found")
        return {
            "city":       data["name"],
            "country":    data["sys"]["country"],
            "condition":  data["weather"][0]["main"],
            "desc":       data["weather"][0]["description"].title(),
            "temp":       round(data["main"]["temp"], 1),
            "feels_like": round(data["main"]["feels_like"], 1),
            "temp_min":   round(data["main"]["temp_min"], 1),
            "temp_max":   round(data["main"]["temp_max"], 1),
            "humidity":   data["main"]["humidity"],
            "wind_speed": round(data["wind"]["speed"] * 3.6, 1),  # m/s → km/h
            "visibility": data.get("visibility", 0) // 1000,
            "pressure":   data["main"]["pressure"],
        }, None
    except Exception as e:
        return None, str(e)


# ── UI ────────────────────────────────────────────────────────

# Title
st.markdown('<div class="weather-title">◈ WEATHER ◈</div>', unsafe_allow_html=True)
st.markdown('<div class="weather-subtitle">ATMOSPHERIC INTELLIGENCE TERMINAL</div>', unsafe_allow_html=True)

# Search bar
col1, col2 = st.columns([3, 1])
with col1:
    city_input = st.text_input("", placeholder="Enter city name...", label_visibility="collapsed")
with col2:
    search = st.button("SEARCH")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# On search
if search and city_input:
    with st.spinner("Fetching weather data..."):
        data, error = get_weather(city_input.strip())

    if error:
        st.markdown(f'<div class="error-box">❌ {error}</div>', unsafe_allow_html=True)

    elif data:
        icon       = get_icon(data["condition"])
        temp_class = get_temp_class(data["temp"])

        # ── City Banner ───────────────────────────────────────
        st.markdown(f"""
        <div class="city-banner">
            <div class="city-icon">{icon}</div>
            <div class="city-name">📍 {data['city']}, {data['country']}</div>
            <div class="city-condition">{data['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Temperature Row ───────────────────────────────────
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🌡️ Temperature</div>
                <div class="metric-value {temp_class}">{data['temp']}°C</div>
                <div class="metric-sub">Feels like {data['feels_like']}°C</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🔺 Max / Min</div>
                <div class="metric-value" style="color:#ff6b6b; font-size:1.1rem;">
                    {data['temp_max']}° / {data['temp_min']}°
                </div>
                <div class="metric-sub">Today's range</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📊 Pressure</div>
                <div class="metric-value" style="color:#b794f4;">{data['pressure']}</div>
                <div class="metric-sub">hPa</div>
            </div>""", unsafe_allow_html=True)

        # ── Humidity Bar ──────────────────────────────────────
        hum = data["humidity"]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💧 Humidity</div>
            <div class="metric-value" style="color:#00d4ff;">{hum}%</div>
            <div class="humidity-bar-bg">
                <div class="humidity-bar-fill" style="width:{hum}%;"></div>
            </div>
            <div class="metric-sub">0% &nbsp;&nbsp;&nbsp; ←────────────────────→ &nbsp;&nbsp;&nbsp; 100%</div>
        </div>""", unsafe_allow_html=True)

        # ── Wind & Visibility ─────────────────────────────────
        c4, c5 = st.columns(2)
        with c4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">💨 Wind Speed</div>
                <div class="metric-value" style="color:#68d391;">{data['wind_speed']} km/h</div>
                <div class="metric-sub">{wind_label(data['wind_speed'])}</div>
            </div>""", unsafe_allow_html=True)
        with c5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">👁️ Visibility</div>
                <div class="metric-value" style="color:#fbd38d;">{data['visibility']} km</div>
                <div class="metric-sub">Clear view distance</div>
            </div>""", unsafe_allow_html=True)

        # ── Footer ────────────────────────────────────────────
        st.markdown('<div class="footer">◈ POWERED BY OPENWEATHERMAP ◈</div>', unsafe_allow_html=True)

elif search and not city_input:
    st.markdown('<div class="error-box">⚠️ Please enter a city name</div>', unsafe_allow_html=True)

else:
    # Default state — placeholder UI
    st.markdown("""
    <div style="text-align:center; color:#2d3748; padding: 3rem 0;">
        <div style="font-size:3rem; margin-bottom:1rem;">🌍</div>
        <div style="font-size:0.85rem; letter-spacing:2px;">ENTER A CITY TO BEGIN</div>
    </div>
    """, unsafe_allow_html=True)
