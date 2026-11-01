import streamlit as st
import pandas as pd
import numpy as np

# Set up page configuration and custom color theme
st.set_page_config(page_title="Real Estate Investment Advisor", layout="wide")

# Custom CSS for a professional color schema
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #2980b9;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #3498db;
        color: white;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏡 Real Estate Investment Advisor & Future Value Predictor")
st.markdown("Evaluate property investment viability and forecast 3-Year & 5-Year valuations based on location, connectivity, and civic amenities.")
st.markdown("---")

# Move inputs to the main window using columns for better layout
col_prop, col_amenities = st.columns([1, 1], gap="large")

with col_prop:
    st.header("1. Basic Property Details")
    city = st.selectbox("City", ["Noida", "Delhi", "Mumbai", "Bangalore", "Pune", "Chennai", "Hyderabad", "Kolkata", "Jaipur"])
    prop_type = st.selectbox("Property Type", ["Apartment / Flat", "Independent House", "Villa"])
    
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        bhk = st.slider("BHK Configuration", 1, 5, 4)
    with sub_col2:
        size_sqft = st.number_input("Size (Sq.Ft)", min_value=500, max_value=10000, value=2000, step=100)
        
    current_price = st.number_input("Current Asking Price (in Lakhs)", min_value=10.0, max_value=1000.0, value=50.0, step=5.0)

with col_amenities:
    st.header("2. Connectivity & Civic Amenities")
    transport_dist = st.selectbox("Metro / Bus / Airport Connectivity", ["High (Under 1.5 - 2 km)", "Medium (2 - 5 km)", "Low (> 5 km)"])
    water_drainage = st.selectbox("Water & Drainage Connection", ["24x7 Municipal Supply & Proper Drainage", "Standard / Borewell"])
    
    st.markdown("**Nearby Essentials & Entertainment**")
    # Changed from multiselect to individual checkboxes for better visibility
    check_col1, check_col2 = st.columns(2)
    with check_col1:
        has_groceries = st.checkbox("Groceries & Supermarket", value=True)
        has_schools = st.checkbox("Schools & Colleges", value=True)
    with check_col2:
        has_hospitals = st.checkbox("Hospitals & Clinics", value=True)
        has_malls = st.checkbox("Shopping Mall & Cinema Hall", value=True)
    
    sub_col3, sub_col4, sub_col5 = st.columns(3)
    with sub_col3:
        furnished = st.selectbox("Furnished Status", ["Furnished", "Semi", "Unfurnished"])
    with sub_col4:
        society_sec = st.radio("Gated Security", ["Yes", "No"], horizontal=True)
    with sub_col5:
        parking = st.radio("Parking Space", ["Yes", "No"], horizontal=True)

st.markdown("---")

# Center the predict button
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    predict_clicked = st.button("Predict Investment & Future Value", use_container_width=True)

if predict_clicked:
    # Base annual appreciation rate (8%) adjusted by connectivity and infrastructure
    growth_rate = 0.08
    if "High" in transport_dist:
        growth_rate += 0.015
    if "24x7" in water_drainage:
        growth_rate += 0.01
    
    # Add growth for each checked essential
    essentials_count = sum([has_groceries, has_schools, has_hospitals, has_malls])
    growth_rate += 0.0025 * essentials_count
    
    # Calculate 3-Year and 5-Year forecasted prices
    price_3yr = current_price * ((1 + growth_rate) ** 3)
    price_5yr = current_price * ((1 + growth_rate) ** 5)
    
    # Classification logic: Price per SqFt and infrastructure score vs city benchmark
    price_per_sqft_inr = (current_price * 100000) / size_sqft
    is_good_investment = (price_per_sqft_inr <= 8500) and ("24x7" in water_drainage)
    
    st.header("📊 Investment Advisory Report")
    
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("### Classification Verdict")
        if is_good_investment:
            st.success("✅ **Good Investment**")
            st.write(f"At ₹{price_per_sqft_inr:,.0f}/Sq.Ft with strong civic connectivity, this property is competitively priced.")
        else:
            st.error("❌ **High Risk / Overpriced**")
            st.write(f"At ₹{price_per_sqft_inr:,.0f}/Sq.Ft, this property exceeds the recommended local median or lacks utilities.")
        st.markdown("</div>", unsafe_allow_html=True)
            
    with res_col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("### 3-Year Forecast")
        st.metric(
            label="Estimated Value",
            value=f"₹{price_3yr:.2f} L",
            delta=f"+₹{(price_3yr - current_price):.2f} L ({growth_rate*100:.1f}%/yr)"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    with res_col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("### 5-Year Forecast")
        st.metric(
            label="Estimated Value",
            value=f"₹{price_5yr:.2f} L",
            delta=f"+₹{(price_5yr - current_price):.2f} L ({growth_rate*100:.1f}%/yr)"
        )
        st.markdown("</div>", unsafe_allow_html=True)
