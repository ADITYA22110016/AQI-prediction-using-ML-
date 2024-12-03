import streamlit as st
import numpy as np
import joblib
import lightgbm as lgb
from sklearn.preprocessing import StandardScaler

# Load the trained model and scaler
model = joblib.load('lightgbm_model.pkl')
scaler = joblib.load('scaler.pkl')

# Mapping of numeric labels to air quality categories
quality_mapping_reverse = {
    0: 'Good',
    1: 'Moderate',
    2: 'Unhealthy for Sensitive Groups',
    3: 'Poor',
    4: 'Very Unhealthy',
    5: 'Hazardous'
}

# Set page config for better layout
st.set_page_config(page_title="Air Quality Prediction", layout="wide")

# Title and Introduction
st.title("🌍 **Air Quality Prediction App** 🌍")
st.markdown("""
    Welcome to the **Air Quality Prediction App**! Enter the following details to get an instant prediction
    of the air quality based on your location's environmental parameters.
    The prediction will tell you if the air quality is **Good**, **Moderate**, **Poor**, **Hazardous**, etc.
    """)

# Input Fields for User
st.sidebar.header("Enter Environmental Data")

temperature = st.sidebar.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0)
humidity = st.sidebar.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=50.0)
pm25 = st.sidebar.number_input("PM2.5 (µg/m³)", min_value=0.0, max_value=300.0, value=35.0)
pm10 = st.sidebar.number_input("PM10 (µg/m³)", min_value=0.0, max_value=500.0, value=50.0)
no2 = st.sidebar.number_input("NO2 (ppb)", min_value=0.0, max_value=200.0, value=30.0)
so2 = st.sidebar.number_input("SO2 (ppb)", min_value=0.0, max_value=100.0, value=20.0)
co = st.sidebar.number_input("CO (ppm)", min_value=0.0, max_value=10.0, value=1.0)
proximity_industrial = st.sidebar.number_input("Proximity to Industrial Areas (km)", min_value=0.0, max_value=100.0, value=10.0)
population_density = st.sidebar.number_input("Population Density (persons/km²)", min_value=0.0, max_value=10000.0, value=500.0)

# Create an array of the inputs
user_input = np.array([[
    temperature, humidity, pm25, pm10, no2, so2, co, proximity_industrial, population_density
]])

# Scale the input using the same scaler that was used during training
user_input_scaled = scaler.transform(user_input)

# Predict the air quality using the model
prediction = model.predict(user_input_scaled)
predicted_quality = quality_mapping_reverse[prediction[0]]

# Define AQI ranges based on the predicted quality
aqi_range = {
    'Good': '0-50',
    'Moderate': '51-100',
    'Unhealthy for Sensitive Groups': '101-150',
    'Poor': '151-200',
    'Very Unhealthy': '201-300',
    'Hazardous': '301-500'
}

# Add a button for prediction
if st.sidebar.button("Predict Air Quality"):
    st.subheader("Prediction Result")
    st.markdown(f"### **Predicted Air Quality: {predicted_quality}**")
    st.markdown(f"**AQI Range:** {aqi_range[predicted_quality]}")
    
    # Display a detailed interpretation of the air quality
    st.markdown("""
    - **Good**: Air quality is considered satisfactory, and air pollution poses little or no risk.
    - **Moderate**: Air quality is acceptable; however, there may be a risk for some people who are unusually sensitive to air pollution.
    - **Unhealthy for Sensitive Groups**: Members of sensitive groups may experience health effects. The general public is less likely to be affected.
    - **Poor**: Health effects may be experienced by the general population.
    - **Very Unhealthy**: Health alert; everyone may experience more serious health effects.
    - **Hazardous**: Serious health effects may occur across the entire population.
    """)
    
    # Include a recommendation based on the prediction
    if predicted_quality in ['Poor', 'Very Unhealthy', 'Hazardous']:
        st.warning("🚨 **Warning**: The air quality is hazardous! It's advisable to stay indoors and limit outdoor activities.")
    else:
        st.success("✅ **Good**: The air quality is safe for outdoor activities.")

# Footer
st.markdown("---")
st.markdown("""
    Developed with ❤️ by the Aditya Patil  
    """)
