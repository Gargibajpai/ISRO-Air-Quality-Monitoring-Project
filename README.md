# 🌤️ AirScan Lite

A Streamlit web application for real-time air quality monitoring and prediction using simulated data.

## Features

- **City Selection**: Choose from 8 major Indian cities (Delhi, Mumbai, Bangalore, Lucknow, Chennai, Kolkata, Hyderabad, Pune)
- **Weather Simulation**: Generates realistic weather data including temperature, humidity, wind speed, and AOD
- **PM2.5 Prediction**: Uses a simple ML model to predict PM2.5 levels based on AOD and temperature
- **AQI Classification**: Converts PM2.5 to Air Quality Index categories with health advisories
- **Interactive Map**: Visualizes the selected location with AQI information using Folium
- **Data Visualization**: Pie chart showing PM2.5 levels across different cities
- **Offline Operation**: Works completely offline with no external API keys required

  ## 🚀 Live Demo
  https://gargibajpai-isro-air-quality-monitoring-project-app-xqkraq.streamlit.app/

  
## Installation

1. **Clone or download the project files**
   ```bash
   # If using git
   git clone <repository-url>
   cd airscan-lite
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, manually navigate to the URL

## Usage

1. **Select a City**: Use the dropdown in the sidebar to choose a city
2. **View Weather Data**: See simulated temperature, humidity, wind speed, and AOD values
3. **Check Air Quality**: View the predicted PM2.5 level and AQI category
4. **Health Advisory**: Read the health recommendations based on air quality
5. **Explore Map**: Click on the map marker to see detailed information
6. **Compare Cities**: View the pie chart showing PM2.5 levels across different cities
7. **Update Data**: Click the "Update Data" button to refresh the simulation

## Technical Details

### Data Simulation
- **Weather Data**: Random values within realistic ranges
- **AOD (Aerosol Optical Depth)**: Simulated values between 0.1-1.5
- **PM2.5 Prediction**: Formula: `PM2.5 = AOD × 50 + Temperature × 2 + random variation`

### AQI Categories (Indian Standards)
- **Good** (0-30): Enjoy outdoor activities
- **Satisfactory** (31-60): Minor breathing discomfort for sensitive people
- **Moderate** (61-90): Reduce outdoor activities for people with heart/lung disease
- **Poor** (91-120): Everyone should reduce outdoor activities
- **Very Poor** (121-250): Avoid outdoor activities, use masks
- **Severe** (251+): Stay indoors, avoid all outdoor activities

### Dependencies
- `streamlit`: Web application framework
- `geopy`: Geocoding (with fallback to predefined coordinates)
- `folium`: Interactive maps
- `pandas`: Data manipulation
- `numpy`: Numerical computations
- `plotly`: Data visualization
- `streamlit-folium`: Streamlit integration for Folium maps

## Customization

### Adding New Cities
To add more cities, update the `CITY_DATA` dictionary in `app.py`:

```python
CITY_DATA = {
    "Your City": {"lat": latitude, "lon": longitude, "state": "State Name"},
    # ... existing cities
}
```

### Modifying the ML Model
The PM2.5 prediction formula can be adjusted in the `predict_pm25()` function:

```python
def predict_pm25(weather_data):
    # Modify this formula as needed
    base_pm25 = aod * 50 + temperature * 2
    # ... rest of the function
```

### Changing AQI Standards
Update the `calculate_aqi_category()` function to use different AQI standards or thresholds.

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   streamlit run app.py --server.port 8502
   ```

2. **Missing dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Geocoding errors**
   - The app uses predefined coordinates for major cities
   - Geopy is only used as a fallback for unknown cities

### System Requirements
- Python 3.7 or higher
- Internet connection (for initial package installation)
- 4GB RAM recommended
- Modern web browser

 ## Team Members:
- Gargi Bajpai
- Ashmita Goyal
- LipikaTomar

## License

This project is for educational and demonstration purposes. The simulated data should not be used for real-world air quality monitoring.


##Screnshots 
![WhatsApp Image 2025-07-09 at 17 53 22_81885931](https://github.com/user-attachments/assets/5b49ae59-5784-4def-8678-85b991a4a9e8)
![WhatsApp Image 2025-07-09 at 17 54 15_6e07ae64](https://github.com/user-attachments/assets/58c67cfa-c245-4ede-a18f-9db3553d7d3c)
![WhatsApp Image 2025-07-09 at 17 54 57_a6f6c066](https://github.com/user-attachments/assets/bc4db520-6218-4894-b030-071b74086fd3)
![WhatsApp Image 2025-07-09 at 17 55 25_d9117950](https://github.com/user-attachments/assets/a432980c-4593-4a92-a606-6dec7d8bed32)
![WhatsApp Image 2025-07-09 at 17 55 54_ca07b829](https://github.com/user-attachments/assets/cc3c3130-92d0-4b27-9dc1-d4a47b4740a5)
![WhatsApp Image 2025-07-09 at 17 56 14_8e088155](https://github.com/user-attachments/assets/ea5830b8-adcb-45ef-a3b8-0aae86a87118)







**Note**: This application uses simulated data for demonstration purposes. For real-time air quality monitoring, please refer to official government sources like the Central Pollution Control Board (CPCB) in India. 
