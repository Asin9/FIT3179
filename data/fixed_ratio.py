import pandas as pd

# Load the CSV file
input_file = "data/top_100.csv_with_continent__fix.csv"
output_file = "data/top_100_with_fixed_ratio.csv"

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)

# Function to format the FemaleMaleRatio column
def format_ratio(ratio):
    try:
        parts = ratio.split(':')
        if len(parts) == 3 and all(part.isdigit() for part in parts):
            formatted_ratio = f"{parts[0].strip()} : {parts[1].strip()}"
            return formatted_ratio
        else:
            return None  # Return None for values not in the expected format
    except AttributeError:
        return None  # Handle non-string or missing values gracefully

# Apply the format_ratio function to the FemaleMaleRatio column
df['FemaleMaleRatio'] = df['FemaleMaleRatio'].apply(format_ratio)

# Drop rows with None (i.e., data not in the specified format)
df = df.dropna(subset=['FemaleMaleRatio'])

# Save the updated DataFrame to a new CSV file
df.to_csv(output_file, index=False)

print("FemaleMaleRatio column formatted and saved to", output_file)
