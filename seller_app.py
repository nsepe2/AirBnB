
### lets just write the script without worrying about the running the code. We don't have all the modules installed.

import streamlit as st
import pandas as pd
import random

# Sample data for dropdown options (replace with your actual data if needed)
property_types = ["House", "Apartment", "Condo", "Townhouse"]
price_ranges = ["$10 - $500", "$500 - $1,000", "$1,000 - $5,000", "$5,000 - $10,000", "$10,000 - $50,000"]

# Sidebar for Seller Input Form
st.sidebar.title("Seller's Property Details")

# Dropdown for Property Type
property_type = st.sidebar.selectbox("Property Type", property_types)

# Dropdown for Price Range
price_range = st.sidebar.selectbox("Price Range", price_ranges)

# Number inputs for Bedrooms, Bathrooms, Beds, etc.
bedrooms = st.sidebar.number_input("Number of Bedrooms", min_value=1, max_value=10, value=1)
bathrooms = st.sidebar.number_input("Number of Bathrooms", min_value=1, max_value=10, value=1)
beds = st.sidebar.number_input("Number of Beds", min_value=1, max_value=10, value=1)

# Flag to check if the submit button has been clicked
submitted = st.sidebar.button("Submit Property")

# Main Page Content
if not submitted:
    # Display introductory text only if not submitted
    st.title("Seller's Property Submission")
    st.write("Fill in the property details on the sidebar to submit your listing.")
else:
    # Display submitted property details
    st.markdown("### Property Details Submitted")
    st.write(f"**Property Type:** {property_type}")
    st.write(f"**Price Range:** {price_range}")
    st.write(f"**Bedrooms:** {bedrooms}")
    st.write(f"**Bathrooms:** {bathrooms}")
    st.write(f"**Beds:** {beds}")
    
    # Generate and display a prominent random score
    random_score = random.randint(1, 5)
    st.markdown(f"## 🔥 **Predicted Score: {random_score}** 🔥")

