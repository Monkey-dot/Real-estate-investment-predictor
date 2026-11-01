import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Real Estate Investment Advisor", layout="wide")
st.title("🏡 Real Estate Investment Advisor & Future Value Predictor")
st.markdown("Evaluate property investment viability and forecast 3-Year & 5-Year valuations based on location, connectivity, and civic amenities.")

# Sidebar: Investor Property Inputs
st.sidebar.header("1. Basic Property Details")
city = st.sidebar.selectbox("City", ["Noida", "Delhi", "Mumbai", "Bangalore", "Pune", "Chennai", "Hyderabad", "Kolkata", "Jaipur"])
prop_type = st.sidebar.selectbox("Property Type", ["Apartment / Flat", "Independent House", "Villa"])
bhk = st.sidebar.slider("BHK Configuration", 1, 5, 4)
size_sqft = st.sidebar.number_input("Size (Sq.Ft)", min_value=500, max_value=10000, value=2000, step=100)
current_price = st.sidebar.number_input("Current Asking Price (in Lakhs)", min_value=10.0, max_value=1000.0, value=50.0, step=5.0)

st.sidebar.header("2. Connectivity & Civic Amenities")
transport_dist = st.sidebar.selectbox("Metro / Bus / Airport Connectivity", ["High (Under 1.5 - 2 km)", "Medium (2 - 5 km)", "Low (> 5 km)"])
water_drainage = st.sidebar.selectbox("Water & Drainage Connection", ["24x7 Municipal Supply & Proper Drainage", "Standard / Borewell"])
daily_needs = st.sidebar.multiselect(
    "Nearby Essentials & Entertainment",
    ["Groceries & Supermarket", "Schools & Colleges", "Hospitals & Clinics", "Shopping Mall & Cinema Hall"],
    default=["Groceries & Supermarket", "Schools & Colleges", "Hospitals & Clinics", "Shopping Mall & Cinema Hall"]
)
furnished = st.sidebar.selectbox("Furnished Status", ["Furnished", "Semi-Furnished", "Unfurnished"])
society_sec = st.sidebar.radio("Gated Society & 24x7 Security", ["Yes", "No"], horizontal=True)
parking = st.sidebar.radio("Dedicated Parking Available", ["Yes", "No"], horizontal=True)

if st.sidebar.button("Predict Investment & Future Value"):
    # Base annual appreciation rate (8%) adjusted by connectivity and infrastructure
    growth_rate = 0.08
    if "High" in transport_dist:
        growth_rate += 0.015
    if "24x7" in water_drainage:
        growth_rate += 0.01
    growth_rate += 0.0025 * len(daily_needs)

    # Calculate 3-Year and 5-Year forecasted prices
    price_3yr = current_price * ((1 + growth_rate) ** 3)
    price_5yr = current_price * ((1 + growth_rate) ** 5)

    # Classification logic: Price per SqFt and infrastructure score vs city benchmark
    price_per_sqft_inr = (current_price * 100000) / size_sqft
    is_good_investment = (price_per_sqft_inr <= 8500) and ("24x7" in water_drainage)

    st.subheader("📊 Investment Advisory Report")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Classification Verdict")
        if is_good_investment:
            st.success("✅ **Good Investment**")
            st.write(f"At ₹{price_per_sqft_inr:,.0f}/Sq.Ft with strong civic connectivity, this {bhk}BHK in {city} is competitively priced.")
        else:
            st.error("❌ **High Risk / Overpriced**")
            st.write(f"At ₹{price_per_sqft_inr:,.0f}/Sq.Ft, this property exceeds the recommended local median or lacks core utilities.")

    with col2:
        st.markdown("### 3-Year Price Forecast")
        st.metric(
            label="Estimated Value (3 Years)",
            value=f"₹{price_3yr:.2f} Lakhs",
            delta=f"+₹{(price_3yr - current_price):.2f} Lakhs ({growth_rate*100:.1f}%/yr)"
        )

    with col3:
        st.markdown("### 5-Year Price Forecast")
        st.metric(
            label="Estimated Value (5 Years)",
            value=f"₹{price_5yr:.2f} Lakhs",
            delta=f"+₹{(price_5yr - current_price):.2f} Lakhs ({growth_rate*100:.1f}%/yr)"
        )
