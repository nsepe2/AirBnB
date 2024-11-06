# %%
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import openpyxl
import ast
file_path = '/Users/nasase/Documents/GitHub/ADS_Projects/Airbnb Dataset_FINAL.xlsx'

data = pd.read_excel(file_path)

# %%
# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

#Process Neighborhood Overviews and Ensure that all data is in string format
data['NEIGHBOUR OVERVIEW'] = data['NEIGHBOUR OVERVIEW'].astype(str)
data['Neighbour_Description_Sentiment'] = data['NEIGHBOUR OVERVIEW'].apply(lambda x: analyzer.polarity_scores(x)['compound'])

#Process Amenities and Ensure that all data is in string/list format
def process_amenities(amenities):
    if isinstance(amenities, str):
        try:
            return ast.literal_eval(amenities)
        except (ValueError, SyntaxError):
            return []
    elif isinstance(amenities, list):
        return amenities
    else:
        return []  

data['Amenities'] = data['Amenities'].apply(process_amenities)

# Ensure all entries in 'Amenities' are now lists
data['Amenities_Sentiment'] = data['Amenities'].apply(
    lambda amenities: analyzer.polarity_scores(" ".join(amenities))['compound'] if isinstance(amenities, list) else 0
)

print(data[['NEIGHBOUR OVERVIEW', 'Neighbour_Description_Sentiment', 'Amenities', 'Amenities_Sentiment', 'Review Scores Rating']].head())


# %%
#Checking Correlation between good sentiment and High Review scores
correlation_neighbour = data['Neighbour_Description_Sentiment'].corr(data['Review Scores Rating'])
correlation_amenities = data['Amenities_Sentiment'].corr(data['Review Scores Rating'])
print(f"Correlation (Neighbour Overview Sentiment - Review Scores Rating): {correlation_neighbour}")
print(f"Correlation (Amenities Sentiment - Review Scores Rating): {correlation_amenities}")


