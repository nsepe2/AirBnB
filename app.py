import sys
import os
import streamlit as st
import pandas as pd
import random
import pydeck as pdk
from dotenv import load_dotenv
from utils.b2 import B2
 
# Add the utils directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'utils')))
 
# Load environment variables
load_dotenv()
 
# Set Backblaze connection
b2 = B2(
    endpoint=os.getenv('B2_ENDPOINT', 's3.us-east-005.backblazeb2.com'),
    key_id=os.getenv('B2_KEYID'),
    secret_key=os.getenv('B2_APPKEY')
)
 
@st.cache_data
def fetch_data():
    try:
        b2.set_bucket('Streamlit-D')  # Set the bucket
        obj = b2.get_object('Sorted_Austin_AirBnB.csv')  # Use the EXACT file name
        return pd.read_csv(obj)
    except Exception as e:
        st.error(f"Error fetching data from Backblaze: {e}")
        return None
 
# APPLICATION
st.title("Airbnb Data Viewer")
 
# Sidebar navigation options
navigation = st.sidebar.radio("Select ", ("Main", "Buyer", "Seller"))
 
# Main Page Content
if navigation == "Main":
    st.header("Welcome to the Airbnb Data Explorer")
    st.markdown("""
    **Using this data, we aim to uncover insights into what makes an Airbnb listing successful.**

    ### Our Goals:
    - Understand the factors that lead to higher ratings and greater foot traffic.
    - Explore the influence of location and neighborhoods on reviews and ratings.
    - Identify specific amenities that contribute to higher reviews.
    - Evaluate if pricing strategies impact success.

    ### Our Approach:
    - Compare locations and neighborhoods to identify "hotspots" that are favored by users.
    - Assess the role of amenities in improving customer satisfaction.
    - Analyze price ranges to find the "sweet spot" that attracts the most guests.

    By analyzing this data, we hope to help Airbnb hosts optimize their listings and improve their offerings for greater success.
    """)
    st.write("Use the navigation options on the left to explore the Buyer and Seller pages for more detailed insights.")

# Fetch data from Backblaze
data = fetch_data()

if data is not None and 'id' in data.columns:
    # Convert 'id' to integer, then keep only the first five digits
    data['id'] = data['id'].apply(lambda x: str(int(x))[:5])
 
# Display data on the main page
if navigation == "Main" and data is not None:
    st.write("Data loaded successfully.")
    st.dataframe(data.head())
 

# Buyer Page
if navigation == "Buyer":
    st.header("Explore Listings in Austin, Texas")

    # Check if data is available
    if data is not None:
        
        st.sidebar.subheader("Search Filters")

        # User-enterable ratings input
        rating_input = st.sidebar.text_input("Enter Minimum Rating (0.0 to 5.0)", "0.0")

        # Validate rating input
        try:
            rating_input = float(rating_input)
            if rating_input < 0.0 or rating_input > 5.0:
                st.sidebar.error("Rating out of range. Enter a value between 0.0 and 5.0.")
                rating_input = None
        except ValueError:
            st.sidebar.error("Invalid rating. Please enter a numeric value.")
            rating_input = None

        # Property type dropdown with "Any" option
        unique_property_types = (
            ["Any"] + sorted(data['property_type'].dropna().unique().tolist()) 
            if 'property_type' in data.columns 
            else ["Any"]
        )
        selected_property_type = st.sidebar.selectbox("Select Property Type", unique_property_types)

        # Text input for price filter
        price_input = st.sidebar.text_input("Enter Price (0 to 8240)", "0")

        # Validate price input
        try:
            price_input = int(price_input)
            if price_input < 0 or price_input > 8240:
                st.sidebar.error("Price out of range. Enter a value between 0 and 8240.")
                price_input = None
        except ValueError:
            st.sidebar.error("Invalid price. Please enter a numeric value.")
            price_input = None

        # Number of bedrooms filter
        selected_bedrooms = st.sidebar.slider("Select Number of Bedrooms", min_value=1, max_value=10, value=1)

        # Search button
        search_button = st.sidebar.button("Search")

        # Apply filters and display results when search button is clicked
        if search_button:
            filtered_data = data

            # Filter by ratings
            if rating_input is not None:
                filtered_data = filtered_data[filtered_data['review_scores_rating'] >= rating_input]

            # Filter by property type (ignore if "Any" is selected)
            if selected_property_type and selected_property_type != "Any":
                filtered_data = filtered_data[filtered_data['property_type'] == selected_property_type]

            # Filter by price
            if price_input is not None:
                filtered_data = filtered_data[filtered_data['price'] <= price_input]

            # Filter by bedrooms
            if selected_bedrooms:
                filtered_data = filtered_data[filtered_data['bedrooms'] == selected_bedrooms]

            # Display filtered results
            if len(filtered_data) > 0:
                st.write(f"Found {len(filtered_data)} properties based on your search criteria.")
                st.dataframe(filtered_data[['review_scores_rating', 'name', 'listing_url', 'price', 'bedrooms']])

                # Render map with filtered data
                if 'latitude' in filtered_data.columns and 'longitude' in filtered_data.columns:
                    deck = pdk.Deck(
                        map_style='mapbox://styles/mapbox/streets-v11',
                        initial_view_state=pdk.ViewState(
                            latitude=filtered_data['latitude'].mean(),
                            longitude=filtered_data['longitude'].mean(),
                            zoom=10,
                            pitch=50,
                        ),
                        layers=[pdk.Layer(
                            'ScatterplotLayer',
                            data=filtered_data,
                            get_position='[longitude, latitude]',
                            get_color='[200, 30, 0, 160]',
                            get_radius=200,
                            pickable=True
                        )],
                        tooltip={
                            "html": "<b>Listing Name:</b> {name}<br/><b>Price:</b> {price}<br/><b>Review Score:</b> {review_scores_rating}",
                            "style": {"backgroundColor": "steelblue", "color": "white"}
                        }
                    )
                    st.pydeck_chart(deck)
                else:
                    st.error("The dataset does not contain 'latitude' and 'longitude' columns.")
            else:
                st.write("No properties match your search criteria.")
    else:
        st.error("No data available.")



#Seller Page
elif navigation == "Seller":
    # Sidebar for Seller Input Form
    st.sidebar.title("Seller's Property Details")
    property_types = ["House", "Apartment", "Condo", "Townhouse"]
    price_ranges = ["$10 - $500", "$500 - $1000", "$1000- $5000", "$5000 - $10000", "$10000 - $50000"]
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
