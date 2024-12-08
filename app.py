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
        data = pd.read_csv(obj)

        # Preprocess the data
        if 'price' in data.columns:
            data['price'] = data['price'].replace('[\$,]', '', regex=True).astype(float)
        return data
    except Exception as e:
        st.error(f"Error fetching data from Backblaze: {e}")
        return None

# Main application function
def main():
    # Set the page config for a wide layout
    st.set_page_config(page_title="Airbnb Data Viewer", layout="wide", initial_sidebar_state="expanded")

    # Custom CSS for styling
    st.markdown("""
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f9;
            }
            .title {
                font-size: 3rem;
                font-weight: bold;
                color: #F0000B;
                text-align: center;
                margin-top: 40px;
            }
            .sub-title {
                font-size: 2rem;
                color: #333;
            }
            .markdown-text {
                font-size: 1.1rem;
                line-height: 1.6;
                color: #555;
            }
            .stButton>button {
                background-color: #007BFF;
                color: white;
                font-weight: bold;
                border-radius: 12px;
                padding: 10px 20px;
            }
            .stButton>button:hover {
                background-color: #006FCE;
            }
            .sidebar .sidebar-content {
                background-color: #2F4F4F;
                color: white;
            }
            .stSidebar .sidebar-content .element-container {
                color: white;
            }
            .footer {
                background-color: #007BFF;
                padding: 10px;
                color: white;
                text-align: center;
                font-size: 14px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Title Section with custom color
    st.markdown('<h1 class="title">Airbnb Explorer</h1>', unsafe_allow_html=True)

    # Navigation
    navigation = st.sidebar.selectbox("Navigate", ["Main", "Buyer Page", "Seller Page"])

    # Fetch data
    data = fetch_data()

    # Main Page Content with Tabs
    if navigation == "Main":
        st.header("Welcome to the Airbnb Data Explorer")

        # Tab system
        tab = st.selectbox("Select a section", ["Introduction", "Goals and Approach", "Data Preview"])

        if tab == "Introduction":
            st.markdown('<p class="sub-title">Introduction</p>', unsafe_allow_html=True)
            st.markdown("""
            <p class="markdown-text">Using this data, we aim to uncover insights into what makes an Airbnb listing successful.</p>
            """, unsafe_allow_html=True)

        elif tab == "Goals and Approach":
            st.markdown('<p class="sub-title">Our Goals and Approach</p>', unsafe_allow_html=True)
            st.markdown("""
            <p class="markdown-text">
            Our Goals:
            - Understand the factors that lead to higher ratings and greater foot traffic.
            - Explore the influence of location and neighborhoods on reviews and ratings.
            - Identify specific amenities that contribute to higher reviews.
            - Evaluate if pricing strategies impact success.

            Our Approach:
            - Compare locations and neighborhoods to identify "hotspots" that are favored by users.
            - Assess the role of amenities in improving customer satisfaction.
            - Analyze price ranges to find the "sweet spot" that attracts the most guests.
            </p>
            """, unsafe_allow_html=True)

        elif tab == "Data Preview":
            if data is not None and 'id' in data.columns:
                # Convert 'id' to integer, then keep only the first five digits
                data['id'] = data['id'].apply(lambda x: str(int(float(x)))[:5])

            # Display data on the main page
            if data is not None:
                st.write("Data loaded successfully.")
                st.dataframe(data.head())
            else:
                st.write("Failed to load data.")

    elif navigation == "Buyer Page" and data is not None:
        st.header("Buyer Page")

        # Inputs with better styling
        rating_input = st.number_input("Minimum Review Rating", min_value=0.0, max_value=5.0, value=3.0, step=0.1)
        price_input = st.number_input("Maximum Price ($)", min_value=0, value=500)

        unique_property_types = (
            ["Any"] + sorted(data['property_type'].dropna().unique().tolist()) 
            if 'property_type' in data.columns else ["Any"]
        )
        selected_property_type = st.selectbox("Property Type", options=unique_property_types)

        unique_bedrooms = (
            sorted(data['bedrooms'].dropna().unique()) 
            if 'bedrooms' in data.columns else []
        )
        selected_bedrooms = st.selectbox("Number of Bedrooms", options=unique_bedrooms)

        search_button = st.button("Search")

        if search_button:
            filtered_data = data.copy()

            # Filter by rating
            if 'review_scores_rating' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['review_scores_rating'] >= rating_input]

            # Filter by property type
            if selected_property_type != "Any" and 'property_type' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['property_type'] == selected_property_type]

            # Filter by price
            if 'price' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['price'] <= price_input]

            # Filter by bedrooms
            if 'bedrooms' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['bedrooms'] == selected_bedrooms]

            # Display filtered data
            if len(filtered_data) > 0:
                st.write(f"Found {len(filtered_data)} properties based on your search criteria.")
                st.dataframe(filtered_data[['review_scores_rating', 'name', 'listing_url', 'price', 'bedrooms']])

                # Render map
                if 'latitude' in filtered_data.columns and 'longitude' in filtered_data.columns:
                    filtered_data = filtered_data.dropna(subset=['latitude', 'longitude'])
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
                    st.error("Latitude and longitude columns are missing or invalid.")
            else:
                st.write("No properties match your search criteria.")

    elif navigation == "Seller Page":
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
            st.markdown(f"##  **Predicted Score: {random_score}** ")

    # Footer
    st.markdown("""
        <div class="footer">
            <p>Made by Nathan, Parth, Diya & Arsh | 2024</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
