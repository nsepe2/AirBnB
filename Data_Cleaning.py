# %%
#Importing our dataset into VS code
import pandas as pd
import openpyxl
import ast
file_path = '/Users/nasase/Documents/GitHub/ADS_Projects/Airbnb Dataset_FINAL.xlsx'

df = pd.read_excel(file_path)

print(df.head())

# %%


# %%
#Check column header names
print(df.columns)

# %%
#Checking for Duplicates 
duplicates = df[df.duplicated(subset=['ID', 'NAME', 'Host Location', 'Host Neighbourhood'], keep=False)]
#Used these four columns to ensure there are no duplicate entries. 

if not duplicates.empty: 
    print(f"Found {duplicates.shape[0]} duplicates")
    print(duplicates)
else:
    print("No duplicates found")

# %%
print(df.dtypes)
#We can see that each column is set to a proper data type so no issues will occur later in the project. 

# %%
print(df['Amenities'].sample(10))

# %%
#Convert Amenities into usable list
import ast
df['Amenities'] = df['Amenities'].apply(lambda x: ast.literal_eval(x) if isinstance (x, str) else [])

print(df['Amenities'].head())



# %%
#Getting Amenity counts
all_amenities = [amenity for sublist in df['Amenities'] if isinstance(sublist, list) for amenity in sublist]
amenities_count = pd.Series(all_amenities).value_counts().reset_index()
amenities_count.columns = ['Neighborhood', 'Count']

pd.set_option('display.max_rows', None)
print(amenities_count)


# %%
#Getting Neighborhood Counts
neighborhood_count= df['Host Neighbourhood'].value_counts().reset_index()
neighborhood_count.columns = ['Host Neighourhood', 'Count']

print(neighborhood_count)


