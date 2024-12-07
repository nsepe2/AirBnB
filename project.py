import pandas as pd
import folium
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

# Load the dataset from the CSV file (replace 'path_to_file' with the correct path to your file)
file_path = 'C:\\Users\\Raj\\OneDrive\\Documents\\diya\\projects\\DataScience_Projects\\Airbnb_Dataset_Updated.csv'

# Read the CSV file using a specific encoding
df = pd.read_csv(file_path, encoding='ISO-8859-1')

geolocator = Nominatim(user_agent="airbnb_analysis")

def get_coordinates(location):
    try:
        loc = geolocator.geocode(location)
        if loc:
            return (loc.latitude, loc.longitude)
        else:
            return None
    except (GeocoderTimedOut, GeocoderServiceError):
        time.sleep(1)  # Wait for a second before retrying
        return get_coordinates(location)

# Create a dictionary of locations and their coordinates
location_coords = {}

# Geocode all host locations
for location in df['Host Location'].dropna():
    if location not in location_coords:
        coords = get_coordinates(location)
        if coords:
            location_coords[location] = coords

# Add coordinates to the dataframe
df['Coordinates'] = df['Host Location'].map(location_coords)

# Remove rows with missing coordinates
df = df.dropna(subset=['Coordinates'])

# Create a map centered on the mean coordinates
center_lat = df['Coordinates'].apply(lambda x: x[0]).mean()
center_lon = df['Coordinates'].apply(lambda x: x[1]).mean()
map = folium.Map(location=[center_lat, center_lon], zoom_start=4)

# Create a MarkerCluster
marker_cluster = MarkerCluster().add_to(map)

# Add markers for each host location
for idx, row in df.iterrows():
    folium.Marker(
        location=row['Coordinates'],
        popup=f"ID: {row['ID']}<br>Location: {row['Host Location']}<br>Price: ${row['Price']}",
        tooltip=row['Host Location']
    ).add_to(marker_cluster)

# Save the map
map.save("airbnb_all_host_locations_map2.html")

print("Map has been saved as airbnb_all_host_locations_map.html")

def count_amenities(amenities):
    if pd.isna(amenities) or amenities == '':
        return 0
    # Split the string on commas and count the items
    return len(amenities.split(','))

# Create the 'amenity_count' column
df['amenity_count'] = df['Amenities'].apply(count_amenities)

# Display the first few rows of the new column
print(df[['Amenities', 'amenity_count']].head())

# Save the processed dataframe to a new CSV file
df.to_csv('cleaned_airbnb_data_with_amenity_count.csv', index=False)
def clean_amenities(amenities):
    if pd.isna(amenities) or amenities == '[]' or amenities == '':
        return ''
    # Remove curly braces and quotes
    cleaned = amenities.strip('{}[]').replace('"', '')
    # Convert to lowercase
    cleaned = cleaned.lower()
    # Standardize common variations
    cleaned = cleaned.replace('wifi', 'wi-fi')
    cleaned = cleaned.replace('air conditioning', 'ac')
    # Add more replacements as needed
    return cleaned.strip()

# Apply cleaning to the amenities column
df['Amenities'] = df['Amenities'].apply(clean_amenities)

# Display the first few rows of the cleaned amenities column
print(df['Amenities'].head())

df['Price'] = df['Price'].replace('[\$,]', '', regex=True).astype(float)

# Sort the listings by Price in descending order to identify the most expensive listings
most_expensive_listings = df.sort_values(by='Price', ascending=False)

# Display the top 10 most expensive listings
print(most_expensive_listings[['ID', 'Host Location', 'Price']].head(10))
# Save the processed dataframe to a new CSV file
df.to_csv('cleaned_airbnb_data222.csv', index=False)