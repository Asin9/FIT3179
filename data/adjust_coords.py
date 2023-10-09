import pandas as pd
import random

# Define the file path for the input CSV
input_csv_file = 'data/top_100.csv_with_continent__fix.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(input_csv_file)

# Function to apply latitude and longitude adjustments
def adjust_coordinates(row):
    random_lat_adjustment = (random.random() - 0.5) * 2
    random_lon_adjustment = (random.random() - 0.5) * 2
    row['Latitude'] += random_lat_adjustment
    row['Longitude'] += random_lon_adjustment
    return row

# Apply the adjustments to each row in the DataFrame
df = df.apply(adjust_coordinates, axis=1)

# Save the modified DataFrame back to a new CSV file
output_csv_file = 'top_100_with_adjusted_coordinates.csv'
df.to_csv(output_csv_file, index=False)

print(f"Adjusted coordinates and saved to {output_csv_file}")
