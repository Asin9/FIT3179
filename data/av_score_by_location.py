import pandas as pd
import math  # Import math module to check for NaN

# Read the CSV file
df = pd.read_csv("data/top_100_with_gender_students_rounded.csv")

# Function to calculate the average score from a string in the format of "47.0-48.7"
def calculate_average(scores):
    # Check if the value is a string (contains '-')
    if isinstance(scores, str) and '-' in scores:
        score_list = scores.split('-')
        return (float(score_list[0]) + float(score_list[1])) / 2
    else:
        return float(scores)
    
# Convert the "OverAll Score" column to float
df['OverAllScore'] = df['OverAllScore'].apply(calculate_average)

# Group by 'Location' and calculate the average 'OverAll Score'
location_avg_scores = df.groupby('Location')['OverAllScore'].mean().reset_index()

# Save the result to a new CSV file
location_avg_scores.to_csv("Location_Average_Scores.csv", index=False)
