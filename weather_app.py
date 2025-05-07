import streamlit as st
import requests
from datetime import datetime, timedelta
import urllib3

# Disable SSL warning (for development only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(page_title="Current Weather - Open-Meteo", layout="wide")

st.title("🌦️ Current Weather Info")

# User inputs for coordinates
st.markdown("### 📍 Enter Coordinates")
col1, col2 = st.columns(2)
with col1:
    latitude = st.number_input("Latitude", value=22.398, format="%.6f")
with col2:
    longitude = st.number_input("Longitude", value=69.906, format="%.6f")

# On button click: Fetch weather
if st.button("🔍 Get Weather"):
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}"
            f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
            f"is_day,wind_speed_10m,wind_gusts_10m,wind_direction_10m,"
            f"precipitation,rain,cloud_cover,surface_pressure"
        )

        response = requests.get(url, verify=False, timeout=10)
        response.raise_for_status()
        data = response.json()
        weather = data.get("current", {})

        # Convert GMT time to IST
        gmt_time = datetime.strptime(weather['time'], '%Y-%m-%dT%H:%M')
        ist_time = gmt_time + timedelta(hours=5, minutes=30)
        formatted_time = ist_time.strftime('%Y-%m-%d %H:%M IST')

        st.markdown(f"### 🕒 Weather at {formatted_time}")
        st.divider()

        # Display in grid (3 columns x 4 rows)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🌡️ Temperature", f"{weather['temperature_2m']} °C")
            st.metric("💧 Humidity", f"{weather['relative_humidity_2m']} %")
            st.metric("🔥 Feels Like", f"{weather['apparent_temperature']} °C")
            st.metric("🌞 Daylight", "Yes" if weather["is_day"] else "No")
        with col2:
            st.metric("🌬️ Wind Speed", f"{weather['wind_speed_10m']} km/h")
            st.metric("💨 Wind Gusts", f"{weather['wind_gusts_10m']} km/h")
            st.metric("🧭 Wind Direction", f"{weather['wind_direction_10m']} °")
        with col3:
            st.metric("🌧️ Precipitation", f"{weather['precipitation']} mm")
            st.metric("☔ Rain", f"{weather['rain']} mm")
            st.metric("☁️ Cloud Cover", f"{weather['cloud_cover']} %")
            st.metric("🧪 Surface Pressure", f"{weather['surface_pressure']} hPa")

    except Exception as e:
        st.error(f"Failed to fetch weather data: {e}")
