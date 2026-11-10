import streamlit as st
import joblib
import requests
model = joblib.load('crop_model.pkl')
if "weather_data" not in st.session_state:
    st.session_state.weather_data = None

st.set_page_config(
    page_title="SmartCrop",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 SmartCrop")
st.subheader("AI-Powered Crop Recommendation System")

st.header("📍 Farm Location")

location = st.text_input(
    "Search your village, town, or nearby location",
    placeholder="Example: Asansol, West Bengal"
)

search = st.button("🔍 Search Location")

if search:
    api_key = st.secrets["OPENWEATHER_API_KEY"]

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        rainfall = 0.0

        if "rain" in data:
            rainfall = data["rain"].get("1h", 0.0)
        st.session_state.weather_data = {
    "temperature": temperature,
    "humidity": humidity,
    "rainfall": rainfall
}

        description = data["weather"][0]["description"]

        st.success(f"Location found: {data['name']}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🌡️ Temperature", f"{temperature:.1f} °C")

        with col2:
            st.metric("💧 Humidity", f"{humidity}%")

        with col3:
            st.metric("☁️ Weather", description.title())

    else:
        st.error("Location not found. Please check the location name.")


st.header("🌱 Soil Information")

col1, col2, col3, col4 = st.columns(4)

with col1:
    N = st.number_input(
        "Nitrogen (N)",
        min_value=0.0,
        value=50.0
    )

with col2:
    P = st.number_input(
        "Phosphorus (P)",
        min_value=0.0,
        value=50.0
    )

with col3:
    K = st.number_input(
        "Potassium (K)",
        min_value=0.0,
        value=50.0
    )

with col4:
    ph = st.number_input(
        "Soil pH",
        min_value=0.0,
        max_value=14.0,
        value=6.5
    )

st.subheader("🌦️ Environmental Information")

# Get saved weather data
weather = st.session_state.weather_data

if weather is not None:

    temperature_input = st.number_input(
        "Temperature (°C)",
        value=float(weather["temperature"]),
        disabled=True
    )

    humidity_input = st.number_input(
        "Humidity (%)",
        value=float(weather["humidity"]),
        disabled=True
    )

    rainfall_input = st.number_input(
        "Rainfall (mm)",
        value=float(weather["rainfall"]),
        disabled=True
    )

else:

    temperature_input = st.number_input(
        "Temperature (°C)",
        value=0.0,
        
    )
    humidity_input = st.number_input(
        "Humidity (%)",
        value=0.0,
    )
    rainfall_input = st.number_input(
        "Rainfall (mm)",
        value=0.0,
    )
#submit button for crop recommendation
st.header("🌱 Crop Recommendation")
recommend = st.button("🌱 Recommend Crop")
if recommend:
    input_data = [[
        N,
        P,
        K,
        temperature_input,
        humidity_input,
        ph,
        rainfall_input
    ]]
    prediction = model.predict(input_data)
    st.success(f"Recommended Crop: {prediction[0]}")