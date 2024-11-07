import streamlit as st

st.title("Property Search")

## Location Input
st.header("Enter Location")
location = st.text_input("City or Neighborhood")

## Amenities Selection
st.header("Select Amenities")

amenities = [
    "Swimming Pool",
    "Gym",
    "Parking",
    "Pet-friendly",
    "Balcony",
    "Furnished",
    "Air Conditioning",
    "Elevator",
    "Laundry Facilities",
    "Security System"
]

selected_amenities = st.multiselect("Choose desired amenities", amenities)

## Property Type
st.header("Property Type")
property_type = st.selectbox("Select property type", ["Apartment", "House", "Condo", "Townhouse"])

## Price Range
st.header("Price Range")
min_price, max_price = st.slider("Select price range ($)", 0, 10000, (500, 5000), step=100)

## Number of Bedrooms
st.header("Bedrooms")
bedrooms = st.number_input("Number of bedrooms", min_value=0, max_value=10, value=1, step=1)

## Search Button
if st.button("Search Properties"):
    st.success("Searching for properties...")
    st.write(f"Location: {location}")
    st.write(f"Amenities: {', '.join(selected_amenities)}")
    st.write(f"Property Type: {property_type}")
    st.write(f"Price Range: ${min_price} - ${max_price}")
    st.write(f"Bedrooms: {bedrooms}")
    # Here you would typically call a function to search for properties based on the input
    # and display the results
