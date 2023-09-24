import pandas as pd
import math  # Import math module to check for NaN

# Read the CSV file
df = pd.read_csv("data/World University Rankings 2023_coords.csv")

# Function to calculate the average of overall scores
def calculate_average(scores):
    # Check if the value is a string (contains '-')
    if isinstance(scores, str) and '-' in scores:
        score_list = scores.split('-')
        return (float(score_list[0]) + float(score_list[1])) / 2
    else:
        # Check if the converted float value is NaN
        if math.isnan(float(scores)):
            return 0.1
        else:
            return float(scores)

# Apply the calculate_average function to the 'OverAll Score' column
df['OverAll Score'] = df['OverAll Score'].apply(calculate_average)

# Create a new DataFrame to store the average scores by location
average_scores_df = df.groupby('Location')['OverAll Score'].mean().reset_index()

# Save the new DataFrame to a new CSV file
average_scores_df.to_csv("Average_Scores_By_Location.csv", index=False)
