# AirBnB Explorer

__Introduction to the App__

The Airbnb Data Viewer serves as an interactive tool for users to explore insights into Airbnb listings. It is particularly focused on helping two main audiences: buyers seeking suitable properties and sellers (hosts) aiming to optimize their listings for better customer satisfaction and ratings.

__The app offers the following features:__

__Data Exploration:__
Users can explore Airbnb data to identify trends in ratings, prices, locations, and property types.
It includes visualization features, such as interactive maps, to highlight the geographic distribution of properties.

__Buyer-Focused Insights:__
Buyers can filter properties based on criteria such as minimum review ratings, price limits, property type, and the number of bedrooms.
Results are presented in an easy-to-understand table format and plotted on an interactive map.

__Seller-Focused Predictions:__
Hosts can input property details, such as accommodations, amenities, and neighborhood descriptions, to predict a potential review score for their listings.
The prediction leverages a trained linear regression model that uses features such as the sentiment of the neighborhood overview and property details to estimate the likely review score.


__Tools Used:__

**1. Streamlit:** For building an interactive web application with UI elements and navigation.

**2. Pandas:** For data manipulation and analysis, including loading CSV data.

**3. Pydeck:** For creating interactive map visualizations.

**4. VADER Sentiment Analysis:** To analyze textual sentiments for review-related features.

**5. Scikit-learn:** For machine learning, including Linear Regression modeling and feature scaling.

**6. Pickle:** To load pre-trained models and scalers.

**7. Backblaze B2 SDK:** For fetching data stored in a cloud bucket.

**8. Dotenv:** For securely managing environment variables like API keys.

**9. OS and Sys Modules:** For handling file paths and modifying the Python path.

**10. Streamlit Cache:** For optimizing performance by caching fetched data.
