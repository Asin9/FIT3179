import pandas as pd
import pycountry

# Load the CSV file into a DataFrame
df = pd.read_csv("data/top_100.csv")

# Function to get continent from country name
def get_continent(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        if country:
            return pycountry.countries.get(name=country_name).continent.name
        else:
            return "Unknown"
    except AttributeError:
        return "Unknown"

# Apply the get_continent function to the "Location" column and create the "Continent" column
df["Continent"] = df["Location"].apply(get_continent)

# Save the updated DataFrame to a new CSV file
df.to_csv("data/top_100_with_continent.csv", index=False)
