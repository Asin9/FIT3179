import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv("data/top_100_with_adjusted_coordinates_6 - Copy.csv")

# Convert the "InternationalStudent" column to decimal format
df["InternationalStudent"] = df["InternationalStudent"].str.rstrip('%').astype('float') / 100

# Save the DataFrame back to a new CSV file
df.to_csv("top_100_with_gender_students_decimal_    .csv", index=False)
