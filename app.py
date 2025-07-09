import streamlit as st
import pandas as pd
import numpy as np
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static
import time
from datetime import datetime, date
import os
import requests
import re

# Import configuration
from config import CITY_DATA, AQI_CATEGORIES, WEATHER_RANGES, ML_MODEL, MAP_CONFIG, APP_CONFIG

# Import CPCB validation utilities
from cpcb_utils import get_cpcb_data_for_city_date, display_validation_metrics, get_available_cpcb_cities, get_available_cpcb_dates

# Import MERRA-2 utilities
from merra2_utils import get_met_data

import streamlit as st
from PIL import Image
import os
from insat_aod_utils import get_aod_at_latlon

AOD_TIF_DIR = "data/insat_aod/"
AOD_IMG_DIR = "data/insat_aod/images/"

# Ensure the image directory exists
os.makedirs(AOD_IMG_DIR, exist_ok=True)

AOD_LINKS_CSV = "INSAT3DR_AOD_Links.csv"

def get_aod_url_for_date(selected_date):
    # Format: 3RIMG_DDMMMYYYY_HHMM_L2G_AOD_V02R00_AOD.tif
    date_str = selected_date.strftime('%d%b%Y').upper()
    df = pd.read_csv(AOD_LINKS_CSV)
    for url in df['Download_URL']:
        if date_str in url:
            filename = url.split('/')[-1]
            return url, filename
    return None, None

def download_aod_file_if_needed(selected_date):
    aod_url, filename = get_aod_url_for_date(selected_date)
    if not aod_url:
        return None
    local_path = os.path.join(AOD_TIF_DIR, filename)
    if not os.path.exists(local_path):
        try:
            st.info(f"Downloading INSAT-3DR AOD file for {selected_date.strftime('%Y-%m-%d')}...")
            r = requests.get(aod_url, stream=True)
            r.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            st.success(f"Downloaded {local_path}")
        except Exception as e:
            st.error(f"Failed to download AOD file: {e}")
            return None
    return local_path

def get_date_from_filename(filename):
    # Example: 3RIMG_28JUN2025_0745_L2G_AOD_V02R00_AOD.tif
    match = re.search(r'_(\d{2}[A-Z]{3}\d{4})_', filename)
    if match:
        date_str = match.group(1)
        try:
            return datetime.strptime(date_str, '%d%b%Y').date()
        except Exception:
            return None
    return None

# --- Dynamic Satellite AOD Image Header ---
def show_satellite_aod_image(selected_date):
    # Try to find a matching image for the selected date
    img_file = None
    for f in os.listdir(AOD_IMG_DIR):
        if f.endswith('.jpg') and selected_date.strftime('%d%b%Y').upper() in f:
            img_file = f
            break
    if img_file:
        img_path = os.path.join(AOD_IMG_DIR, img_file)
        img_date = get_date_from_filename(img_file)
        if img_date:
            header = f"Satellite AOD Image ({img_date.strftime('%d %B %Y')})"
            caption = f"EOS-06 AOD over India - {img_date.strftime('%d %B %Y')}"
        else:
            header = f"Satellite AOD Image"
            caption = f"EOS-06 AOD over India"
        st.header(header)
        image = Image.open(img_path)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image, caption=caption, width=600)
    else:
        # Fallback: use aod_20250625.png if present
        fallback_img = "aod_20250625.png"
        if os.path.exists(fallback_img):
            st.header("Satellite AOD Image (28 June 2025)")
            image = Image.open(fallback_img)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(image, caption="EOS-06 AOD over India - 25 June 2025", width=600)
        else:
            st.header(f"Satellite AOD Image")
            st.info("No satellite AOD image available for the selected date.")


# Page configuration
st.set_page_config(
    page_title=APP_CONFIG["page_title"],
    page_icon=APP_CONFIG["page_icon"],
    layout=APP_CONFIG["layout"],
    initial_sidebar_state=APP_CONFIG["initial_sidebar_state"]
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .aqi-display {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px solid #1f77b4;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        text-align: center;
    }
    .aqi-category {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .aqi-value {
        font-size: 1.2rem;
        font-weight: 600;
        color: #333333;
        margin: 0.5rem 0;
    }
    .health-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for caching
if 'city_data' not in st.session_state:
    st.session_state.city_data = {}

def get_city_coordinates(city_name):
    """
    Get coordinates for a city using predefined data or geopy as fallback
    
    Args:
        city_name (str): Name of the city
        
    Returns:
        tuple: (latitude, longitude) or (None, None) if not found
    """
    if city_name in CITY_DATA:
        return CITY_DATA[city_name]["lat"], CITY_DATA[city_name]["lon"]
    
    # Fallback to geopy if city not in predefined data
    try:
        geolocator = Nominatim(user_agent="airscan_lite")
        location = geolocator.geocode(f"{city_name}, India")
        if location:
            return location.latitude, location.longitude
        else:
            st.error(f"Could not find coordinates for {city_name}")
            return None, None
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        st.error(f"Geocoding service unavailable: {e}")
        return None, None

def simulate_weather_data(city_name):
    """
    Simulate weather and AOD data using random values
    
    Args:
        city_name (str): Name of the city for consistent seeding
        
    Returns:
        dict: Dictionary containing weather parameters
    """
    # Use city name hash for consistent results
    np.random.seed(hash(city_name) % 2**32)
    
    weather_data = {}
    
    # Simulate each weather parameter using ranges from config
    for param, ranges in WEATHER_RANGES.items():
        value = np.random.uniform(ranges["min"], ranges["max"])
        weather_data[param] = round(value, 1 if param != "aod" else 3)
    
    return weather_data

def predict_pm25(weather_data):
    """
    Simple ML model to predict PM2.5 based on AOD and temperature
    
    Args:
        weather_data (dict): Dictionary containing weather parameters
        
    Returns:
        float: Predicted PM2.5 value
    """
    aod = weather_data['aod']
    temperature = weather_data['temperature']
    
    # Base PM2.5 calculation using model parameters
    base_pm25 = (aod * ML_MODEL["aod_weight"] + 
                 temperature * ML_MODEL["temperature_weight"])
    
    # Add random variation
    variation = np.random.uniform(-ML_MODEL["variation_range"], 
                                 ML_MODEL["variation_range"])
    pm25 = base_pm25 * (1 + variation)
    
    # Ensure PM2.5 is within reasonable bounds
    pm25 = max(ML_MODEL["pm25_min"], min(ML_MODEL["pm25_max"], pm25))
    
    return round(pm25, 1)

def calculate_aqi_category(pm25):
    """
    Convert PM2.5 to AQI category and health message
    
    Args:
        pm25 (float): PM2.5 value in µg/m³
        
    Returns:
        tuple: (category, color, health_message)
    """
    for category, info in AQI_CATEGORIES.items():
        if info["min"] <= pm25 <= info["max"]:
            return category, info["color"], info["message"]
    
    # Fallback for values outside defined ranges
    return "Severe", "darkred", "Air quality is severe. Stay indoors."

def create_map(city_name, lat, lon, aqi_category, pm25):
    """
    Create a folium map showing the selected location and AQI
    
    Args:
        city_name (str): Name of the city
        lat (float): Latitude
        lon (float): Longitude
        aqi_category (str): AQI category
        pm25 (float): PM2.5 value
        
    Returns:
        folium.Map: Interactive map object
    """
    # Create map centered on the city
    m = folium.Map(location=[lat, lon], zoom_start=MAP_CONFIG["zoom_start"])
    
    # Color mapping for AQI categories
    color_map = {category: info["color"] for category, info in AQI_CATEGORIES.items()}
    
    # Add marker for the city
    folium.Marker(
        [lat, lon],
        popup=f"{city_name}<br>PM2.5: {pm25} µg/m³<br>AQI: {aqi_category}",
        tooltip=f"{city_name} - {aqi_category}",
        icon=folium.Icon(color=color_map.get(aqi_category, "gray"))
    ).add_to(m)
    
    return m

def create_aqi_chart(aqi_data):
    """
    Create a pie chart showing AQI level breakdown
    
    Args:
        aqi_data (dict): Dictionary with city names as keys and PM2.5 values as values
        
    Returns:
        plotly.graph_objects.Figure: Pie chart figure
    """
    cities = list(aqi_data.keys())
    pm25_values = list(aqi_data.values())
    
    # Create pie chart
    fig = px.pie(
        values=pm25_values,
        names=cities,
        title="PM2.5 Levels Across Cities",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def display_weather_metrics(weather_data):
    """
    Display weather metrics in a grid layout
    
    Args:
        weather_data (dict): Dictionary containing weather parameters
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌡️ Temperature", f"{weather_data['temperature']}°C")
    
    with col2:
        st.metric("💧 Humidity", f"{weather_data['humidity']}%")
    
    with col3:
        st.metric("💨 Wind Speed", f"{weather_data['wind_speed']} km/h")
    
    with col4:
        st.metric("🌫️ AOD", f"{weather_data['aod']}")

def display_aqi_info(aqi_category, color, health_message, pm25):
    """
    Display AQI information and health advisory
    
    Args:
        aqi_category (str): AQI category
        color (str): Color for styling
        health_message (str): Health advisory message
        pm25 (float): PM2.5 value
    """
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="aqi-display">
            <h3 style="color: #333333; margin-bottom: 1rem;">📊 Air Quality Index</h3>
            <div class="aqi-category" style="color: {color}; font-size: 2.8rem; font-weight: 800;">
                {aqi_category}
            </div>
            <div class="aqi-value">
                <strong>PM2.5:</strong> {pm25} µg/m³
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="health-message" style="background-color: {color}; color: white; font-weight: 500;">
            <h4 style="color: white; margin-bottom: 1rem;">🏥 Health Advisory</h4>
            <p style="color: white; font-size: 1.1rem; line-height: 1.5;">{health_message}</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """
    Main function to run the AirScan Lite application
    """
    # Header
    st.markdown('<h1 class="main-header">🌤️ AirScan Lite</h1>', unsafe_allow_html=True)
    
    # Sidebar for user inputs
    st.sidebar.header("📍 Location Selection")
    
    # City selection dropdown
    available_cpcb_cities = get_available_cpcb_cities()
    if available_cpcb_cities:
        if 'selected_city' not in st.session_state or st.session_state['selected_city'] not in available_cpcb_cities:
            st.session_state['selected_city'] = available_cpcb_cities[0]
        selected_city = st.sidebar.selectbox(
            "Select a City:",
            available_cpcb_cities,
            index=available_cpcb_cities.index(st.session_state['selected_city']),
            help="Choose a city to analyze air quality"
        )
        st.session_state['selected_city'] = selected_city
    else:
        selected_city = st.sidebar.selectbox(
            "Select a City:",
            list(CITY_DATA.keys()),
            help="Choose a city to analyze air quality"
        )
    
    # Date selection for CPCB validation
    st.sidebar.header("📅 Date Selection")
    
    # Get available CPCB dates
    available_dates = get_available_cpcb_dates()
    if available_dates:
        selected_date = st.sidebar.selectbox(
            "Select Date for CPCB Validation:",
            available_dates,
            format_func=lambda x: x.strftime('%Y-%m-%d'),
            help="Choose a date to compare with CPCB data"
        )
    else:
        # Fallback to today's date if no CPCB data available
        selected_date = date.today()
        st.sidebar.info("No CPCB data available. Using today's date.")
    
    # Update button
    update_data = st.sidebar.button("🔄 Update Data", help="Refresh air quality data")
    
    # After selected_date is set:
    show_satellite_aod_image(selected_date)

    # Move this section below the image
    st.markdown("### Real-time Air Quality Monitoring & Prediction")

    # Main content area
    if selected_city:
        lat, lon = get_city_coordinates(selected_city)

        # --- INSAT-3DR AOD Integration with On-Demand Download ---
        aod_tif_file = None
        # Try to find a matching AOD .tif for the selected date
        for f in os.listdir(AOD_TIF_DIR):
            if f.endswith('.tif') and selected_date.strftime('%d%b%Y').upper() in f:
                aod_tif_file = f
                break
        if not aod_tif_file:
            # Try to download if not present
            downloaded = download_aod_file_if_needed(selected_date)
            if downloaded:
                aod_tif_file = os.path.basename(downloaded)
        real_aod = None
        if aod_tif_file:
            tif_path = os.path.join(AOD_TIF_DIR, aod_tif_file)
            try:
                real_aod = get_aod_at_latlon(tif_path, lat, lon)
                st.success(f"Using real INSAT-3DR AOD for {selected_date.strftime('%Y-%m-%d')}: {real_aod:.3f}")
                # Show corresponding image if available
                img_name = aod_tif_file.replace('.tif', '.jpg')
                img_path = os.path.join(AOD_IMG_DIR, img_name)
                if os.path.exists(img_path):
                    st.image(img_path, caption=f"INSAT-3DR AOD Image: {img_name}", use_column_width=True)
            except Exception as e:
                st.warning(f"Could not extract AOD from INSAT-3DR: {e}")

        # --- Weather Data (MERRA-2 or simulated) ---
        nc4_filename = f"MERRA2_400.tavg1_2d_slv_Nx.{selected_date.strftime('%Y%m%d')}.nc4"
        if os.path.exists(nc4_filename):
            try:
                weather_data = get_met_data(lat, lon, selected_date, nc4_filename)
                st.info(f"Using real MERRA-2 meteorological data for {selected_date.strftime('%Y-%m-%d')}")
            except Exception as e:
                st.warning(f"Error reading MERRA-2 data: {e}. Using simulated data instead.")
                weather_data = simulate_weather_data(selected_city)
        else:
            st.info(
                f"Real meteorological data is only available up to June 1, 2025. "
                f"For {selected_date.strftime('%Y-%m-%d')}, simulated weather data is shown because satellite/meteorological datasets are not yet available from providers."
            )
            weather_data = simulate_weather_data(selected_city)

        # If real AOD is available, override in weather_data
        if real_aod is not None:
            weather_data['aod'] = float(real_aod)

        # Predict PM2.5
        pm25 = predict_pm25(weather_data)
        
        # Calculate AQI category
        aqi_category, color, health_message = calculate_aqi_category(pm25)
        
        # Display weather metrics
        display_weather_metrics(weather_data)
        
        # AQI and PM2.5 display
        st.markdown("---")
        display_aqi_info(aqi_category, color, health_message, pm25)
        
        # CPCB Data Validation
        if available_dates:
            # Get actual PM2.5 from CPCB data
            actual_pm25 = get_cpcb_data_for_city_date(selected_city, selected_date)
            
            # Display validation metrics
            display_validation_metrics(pm25, actual_pm25, selected_city, selected_date)
        
        # Map visualization
        st.markdown("---")
        st.subheader("🗺️ Location Map")
        
        # Create and display map
        map_obj = create_map(selected_city, lat, lon, aqi_category, pm25)
        folium_static(map_obj, width=MAP_CONFIG["width"], height=MAP_CONFIG["height"])

        # Pollution Heatmap for Multiple Cities
        st.markdown("---")
        st.subheader("🔥 Pollution Heatmap (Predicted PM2.5)")
        
        # Sample city data with coordinates
        sample_cities = [
            {"city": "Delhi", "lat": 28.6139, "lon": 77.2090},
            {"city": "Mumbai", "lat": 19.0760, "lon": 72.8777},
            {"city": "Lucknow", "lat": 26.8467, "lon": 80.9462},
            {"city": "Kolkata", "lat": 22.5726, "lon": 88.3639},
            {"city": "Bengaluru", "lat": 12.9716, "lon": 77.5946},
            {"city": "Chennai", "lat": 13.0827, "lon": 80.2707},
            {"city": "Hyderabad", "lat": 17.3850, "lon": 78.4867},
            {"city": "Ahmedabad", "lat": 23.0225, "lon": 72.5714},
            {"city": "Jaipur", "lat": 26.9124, "lon": 75.7873},
            {"city": "Pune", "lat": 18.5204, "lon": 73.8567},
            {"city": "Bhopal", "lat": 23.2599, "lon": 77.4126},
            {"city": "Patna", "lat": 25.5941, "lon": 85.1376},
            {"city": "Chandigarh", "lat": 30.7333, "lon": 76.7794},
            {"city": "Guwahati", "lat": 26.1445, "lon": 91.7362},
            {"city": "Srinagar", "lat": 34.0837, "lon": 74.7973}
        ]
        
        # Predict PM2.5 for each city
        heat_data = []
        for city in sample_cities:
            weather = simulate_weather_data(city["city"])
            pm25_pred = predict_pm25(weather)
            heat_data.append([city["lat"], city["lon"], pm25_pred])
        
        # Create Folium map for heatmap
        heatmap_map = folium.Map(location=[22.5937, 78.9629], zoom_start=5)
        from folium.plugins import HeatMap
        HeatMap(
            [[row[0], row[1], row[2]] for row in heat_data],
            radius=25,
            min_opacity=0.5,
            max_zoom=5,
            blur=15,
        ).add_to(heatmap_map)
        
        # Render Folium map in Streamlit using st.components.v1.html
        folium_html = heatmap_map._repr_html_()
        st.components.v1.html(folium_html, height=500, width=900)
        
        # AQI Chart (optional)
        st.markdown("---")
        st.subheader("📈 Air Quality Comparison")
        
        # Generate sample data for multiple cities
        sample_aqi_data = {}
        for city in list(CITY_DATA.keys())[:6]:  # Show first 6 cities
            sample_weather = simulate_weather_data(city)
            sample_pm25 = predict_pm25(sample_weather)
            sample_aqi_data[city] = sample_pm25
        
        # Create and display chart
        chart = create_aqi_chart(sample_aqi_data)
        st.plotly_chart(chart, use_container_width=True)
        
        # Additional information
        st.markdown("---")
        st.subheader("ℹ️ About AirScan Lite")
        st.markdown("""
        **AirScan Lite** is a simplified air quality monitoring application that:
        - Uses simulated weather and AOD data for demonstration
        - Predicts PM2.5 levels using a simple mathematical model
        - Provides health advisories based on air quality categories
        - Visualizes data on interactive maps and charts
        - **NEW:** Validates predictions against CPCB data for accuracy assessment
        
        **Note:** This is a demonstration app using simulated data. For real-time air quality data, 
        please refer to official government sources.
        """)
        
    # Footer
    st.markdown("---")
    st.markdown("*Built with Streamlit • Data is simulated for demonstration purposes*")

if __name__ == "__main__":
    main() 