"""
CPCB Data Validation Utilities for AirScan Lite
"""

import pandas as pd
from datetime import datetime, date
import streamlit as st

def load_cpcb_data():
    """
    Load CPCB data from the real CSV file (Real_Time_Air_Quality.csv)
    Returns:
        pandas.DataFrame: Filtered CPCB data with city, date, PM2.5 columns
    """
    try:
        df = pd.read_csv('Real_Time_Air_Quality.csv')
        # Only keep PM2.5 rows with valid average values
        df = df[(df['pollutant_id'] == 'PM2.5') & (df['pollutant_avg'].notna())]
        # Parse date
        df['Date'] = pd.to_datetime(df['last_update'], format='%d-%m-%Y %H:%M:%S').dt.date
        # Standardize city names (strip whitespace)
        df['City'] = df['city'].str.strip()
        # Convert PM2.5 to numeric (coerce errors to NaN, then drop)
        df['PM2.5'] = pd.to_numeric(df['pollutant_avg'], errors='coerce')
        df = df.dropna(subset=['PM2.5'])
        return df[['City', 'Date', 'PM2.5']]
    except FileNotFoundError:
        st.error("CPCB data file not found. Please ensure 'Real_Time_Air_Quality.csv' exists.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading CPCB data: {e}")
        return pd.DataFrame()

def get_cpcb_data_for_city_date(city_name, selected_date):
    """
    Get CPCB PM2.5 data for a specific city and date from the real dataset
    Args:
        city_name (str): Name of the city
        selected_date (datetime.date): Selected date
    Returns:
        float or None: PM2.5 value if found, None otherwise
    """
    df = load_cpcb_data()
    if df.empty:
        return None
    filtered_data = df[(df['City'].str.lower() == city_name.lower()) & (df['Date'] == selected_date)]
    if not filtered_data.empty:
        return filtered_data.iloc[0]['PM2.5']
    return None

def calculate_accuracy(predicted_pm25, actual_pm25):
    """
    Calculate prediction accuracy and provide feedback
    
    Args:
        predicted_pm25 (float): Predicted PM2.5 value
        actual_pm25 (float): Actual PM2.5 value from CPCB
        
    Returns:
        dict: Dictionary containing accuracy metrics and feedback
    """
    if actual_pm25 is None:
        return {
            'absolute_error': None,
            'percentage_error': None,
            'accuracy_level': 'No Data',
            'feedback': 'No CPCB data available for comparison'
        }
    
    absolute_error = abs(predicted_pm25 - actual_pm25)
    percentage_error = (absolute_error / actual_pm25) * 100
    
    # Determine accuracy level
    if absolute_error <= 5:
        accuracy_level = "Excellent"
        feedback = "Prediction is very accurate (within 5 µg/m³)"
    elif absolute_error <= 10:
        accuracy_level = "Good"
        feedback = "Prediction is accurate (within 10 µg/m³)"
    elif absolute_error <= 20:
        accuracy_level = "Fair"
        feedback = "Prediction is reasonably accurate (within 20 µg/m³)"
    elif absolute_error <= 30:
        accuracy_level = "Poor"
        feedback = "Prediction needs improvement (within 30 µg/m³)"
    else:
        accuracy_level = "Very Poor"
        feedback = "Prediction has significant error (over 30 µg/m³)"
    
    return {
        'absolute_error': absolute_error,
        'percentage_error': percentage_error,
        'accuracy_level': accuracy_level,
        'feedback': feedback
    }

def get_accuracy_color(accuracy_level):
    """
    Get color for accuracy level display
    
    Args:
        accuracy_level (str): Accuracy level string
        
    Returns:
        str: Color name for display
    """
    color_map = {
        'Excellent': 'green',
        'Good': 'lightgreen',
        'Fair': 'gold',
        'Poor': 'orange',
        'Very Poor': 'red',
        'No Data': 'gray'
    }
    return color_map.get(accuracy_level, 'gray')

def display_validation_metrics(predicted_pm25, actual_pm25, city_name, selected_date):
    """
    Display validation metrics comparing predicted vs actual PM2.5
    
    Args:
        predicted_pm25 (float): Predicted PM2.5 value
        actual_pm25 (float): Actual PM2.5 value from CPCB
        city_name (str): Name of the city
        selected_date (datetime.date): Selected date
    """
    st.markdown("---")
    st.subheader("🔍 CPCB Data Validation")
    
    # Check if CPCB data is available
    if actual_pm25 is None:
        st.warning(f"⚠️ No CPCB data available for {city_name} on {selected_date.strftime('%Y-%m-%d')}")
        st.info("💡 This could be due to: data not being collected, holidays, or technical issues.")
        return
    
    # Calculate accuracy
    accuracy_data = calculate_accuracy(predicted_pm25, actual_pm25)
    accuracy_color = get_accuracy_color(accuracy_data['accuracy_level'])
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📊 Predicted PM2.5",
            value=f"{predicted_pm25} µg/m³",
            delta=None
        )
    
    with col2:
        st.metric(
            label="📈 Actual PM2.5 (CPCB)",
            value=f"{actual_pm25} µg/m³",
            delta=None
        )
    
    with col3:
        if accuracy_data['absolute_error'] is not None:
            st.metric(
                label="🎯 Absolute Error",
                value=f"{accuracy_data['absolute_error']:.1f} µg/m³",
                delta=f"{accuracy_data['percentage_error']:.1f}%"
            )
    
    # Display accuracy assessment
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background-color: {accuracy_color}; color: white; border-radius: 0.5rem;">
            <h4>Accuracy Level</h4>
            <h3>{accuracy_data['accuracy_level']}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="padding: 1.5rem; background-color: #2c3e50; color: white; border-radius: 0.5rem; border-left: 6px solid {accuracy_color}; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <h4 style="color: white; margin-bottom: 1rem; font-size: 1.3rem;">📋 Validation Summary</h4>
            <p style="color: #ecf0f1; font-size: 1.1rem; margin: 0.5rem 0;"><strong style="color: white;">City:</strong> {city_name}</p>
            <p style="color: #ecf0f1; font-size: 1.1rem; margin: 0.5rem 0;"><strong style="color: white;">Date:</strong> {selected_date.strftime('%Y-%m-%d')}</p>
            <p style="color: #ecf0f1; font-size: 1.1rem; margin: 0.5rem 0; line-height: 1.4;"><strong style="color: white;">Feedback:</strong> {accuracy_data['feedback']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional insights
    if accuracy_data['absolute_error'] is not None:
        st.markdown("---")
        st.subheader("📊 Model Performance Insights")
        
        if accuracy_data['accuracy_level'] in ['Excellent', 'Good']:
            st.success("✅ The model is performing well for this city and date combination.")
        elif accuracy_data['accuracy_level'] == 'Fair':
            st.info("ℹ️ The model shows reasonable accuracy but could be improved with more training data.")
        else:
            st.warning("⚠️ The model prediction differs significantly from actual data. This could indicate:")
            st.markdown("""
            - Seasonal variations not captured in the model
            - Local events affecting air quality
            - Need for model retraining with recent data
            - Different measurement methodologies
            """)
        
        # Health Advisory for Very Poor accuracy
        if accuracy_data['accuracy_level'] == 'Very Poor':
            st.markdown("---")
            st.markdown(f"""
            <div style="padding: 1.5rem; background-color: #ffebee; border-radius: 0.5rem; border-left: 6px solid #f44336; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                <h4 style="color: #c62828; margin-bottom: 1rem; font-size: 1.3rem;">⚠️ Health Advisory</h4>
                <p style="color: #d32f2f; font-size: 1.1rem; margin: 0.5rem 0; line-height: 1.4;">
                    <strong>Model Accuracy Alert:</strong> The prediction model is showing very poor accuracy for this location and date. 
                    Please exercise caution when interpreting the air quality predictions and consider using official CPCB data sources for critical decisions.
                </p>
                <p style="color: #d32f2f; font-size: 1.1rem; margin: 0.5rem 0; line-height: 1.4;">
                    <strong>Recommendation:</strong> Verify air quality information through official government sources before making health-related decisions.
                </p>
            </div>
            """, unsafe_allow_html=True)

def get_available_cpcb_cities():
    """
    Get list of cities available in the real CPCB data
    Returns:
        list: List of city names available in CPCB data
    """
    df = load_cpcb_data()
    if df.empty:
        return []
    return sorted(df['City'].unique().tolist())

def get_available_cpcb_dates():
    """
    Get list of dates available in the real CPCB data
    Returns:
        list: List of available dates
    """
    df = load_cpcb_data()
    if df.empty:
        return []
    return sorted(df['Date'].unique().tolist()) 