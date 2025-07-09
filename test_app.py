#!/usr/bin/env python3
"""
Test script for AirScan Lite application
This script tests the core functions without running the Streamlit app
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import CITY_DATA, AQI_CATEGORIES, WEATHER_RANGES, ML_MODEL
import numpy as np

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import streamlit as st
        import pandas as pd
        import numpy as np
        import folium
        from geopy.geocoders import Nominatim
        import plotly.express as px
        from streamlit_folium import folium_static
        print("✅ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration file"""
    try:
        # Test city data
        assert len(CITY_DATA) > 0, "City data should not be empty"
        for city, data in CITY_DATA.items():
            assert "lat" in data, f"City {city} missing latitude"
            assert "lon" in data, f"City {city} missing longitude"
        
        # Test AQI categories
        assert len(AQI_CATEGORIES) > 0, "AQI categories should not be empty"
        for category, info in AQI_CATEGORIES.items():
            assert "min" in info, f"Category {category} missing min value"
            assert "max" in info, f"Category {category} missing max value"
            assert "color" in info, f"Category {category} missing color"
            assert "message" in info, f"Category {category} missing message"
        
        # Test weather ranges
        assert len(WEATHER_RANGES) > 0, "Weather ranges should not be empty"
        for param, ranges in WEATHER_RANGES.items():
            assert "min" in ranges, f"Parameter {param} missing min value"
            assert "max" in ranges, f"Parameter {param} missing max value"
            assert "unit" in ranges, f"Parameter {param} missing unit"
        
        # Test ML model
        assert "aod_weight" in ML_MODEL, "ML model missing AOD weight"
        assert "temperature_weight" in ML_MODEL, "ML model missing temperature weight"
        assert "variation_range" in ML_MODEL, "ML model missing variation range"
        
        print("✅ Configuration file is valid")
        return True
    except AssertionError as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_weather_simulation():
    """Test weather data simulation"""
    try:
        from app import simulate_weather_data
        
        # Test with a known city
        weather_data = simulate_weather_data("Delhi")
        
        # Check all required parameters are present
        required_params = ["temperature", "humidity", "wind_speed", "aod"]
        for param in required_params:
            assert param in weather_data, f"Missing parameter: {param}"
        
        # Check values are within expected ranges
        assert WEATHER_RANGES["temperature"]["min"] <= weather_data["temperature"] <= WEATHER_RANGES["temperature"]["max"]
        assert WEATHER_RANGES["humidity"]["min"] <= weather_data["humidity"] <= WEATHER_RANGES["humidity"]["max"]
        assert WEATHER_RANGES["wind_speed"]["min"] <= weather_data["wind_speed"] <= WEATHER_RANGES["wind_speed"]["max"]
        assert WEATHER_RANGES["aod"]["min"] <= weather_data["aod"] <= WEATHER_RANGES["aod"]["max"]
        
        # Test consistency (same city should give same results)
        weather_data2 = simulate_weather_data("Delhi")
        assert weather_data == weather_data2, "Weather data should be consistent for same city"
        
        print("✅ Weather simulation works correctly")
        return True
    except Exception as e:
        print(f"❌ Weather simulation error: {e}")
        return False

def test_pm25_prediction():
    """Test PM2.5 prediction"""
    try:
        from app import predict_pm25
        
        # Test with sample weather data
        test_weather = {
            "temperature": 25.0,
            "humidity": 60.0,
            "wind_speed": 10.0,
            "aod": 0.5
        }
        
        pm25 = predict_pm25(test_weather)
        
        # Check PM2.5 is within reasonable bounds
        assert ML_MODEL["pm25_min"] <= pm25 <= ML_MODEL["pm25_max"], f"PM2.5 value {pm25} out of bounds"
        
        # Check PM2.5 is a reasonable value
        expected_base = test_weather["aod"] * ML_MODEL["aod_weight"] + test_weather["temperature"] * ML_MODEL["temperature_weight"]
        assert abs(pm25 - expected_base) <= expected_base * ML_MODEL["variation_range"] * 2, "PM2.5 prediction seems incorrect"
        
        print("✅ PM2.5 prediction works correctly")
        return True
    except Exception as e:
        print(f"❌ PM2.5 prediction error: {e}")
        return False

def test_aqi_categorization():
    """Test AQI categorization"""
    try:
        from app import calculate_aqi_category
        
        # Test with known values
        test_cases = [
            (15, "Good"),
            (45, "Satisfactory"),
            (75, "Moderate"),
            (100, "Poor"),
            (200, "Very Poor"),
            (300, "Severe")
        ]
        
        for pm25, expected_category in test_cases:
            category, color, message = calculate_aqi_category(pm25)
            assert category == expected_category, f"Expected {expected_category} for PM2.5 {pm25}, got {category}"
            assert color in ["green", "lightgreen", "yellow", "orange", "red", "darkred"], f"Invalid color: {color}"
            assert len(message) > 0, "Health message should not be empty"
        
        print("✅ AQI categorization works correctly")
        return True
    except Exception as e:
        print(f"❌ AQI categorization error: {e}")
        return False

def test_coordinate_lookup():
    """Test coordinate lookup"""
    try:
        from app import get_city_coordinates
        
        # Test with known city
        lat, lon = get_city_coordinates("Delhi")
        assert lat == CITY_DATA["Delhi"]["lat"], f"Expected latitude {CITY_DATA['Delhi']['lat']}, got {lat}"
        assert lon == CITY_DATA["Delhi"]["lon"], f"Expected longitude {CITY_DATA['Delhi']['lon']}, got {lon}"
        
        print("✅ Coordinate lookup works correctly")
        return True
    except Exception as e:
        print(f"❌ Coordinate lookup error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing AirScan Lite Application")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_weather_simulation,
        test_pm25_prediction,
        test_aqi_categorization,
        test_coordinate_lookup
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 