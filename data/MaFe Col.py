import pandas as pd

# Load the CSV data
csv_file = 'data/top_100_with_fixed_ratio.csv'  # Replace with the actual file path
data = pd.read_csv(csv_file)

# Define a function to calculate the number of male and female students and round to the nearest whole integer
def calculate_gender_students(row):
    male_ratio, female_ratio = map(int, row['FemaleMaleRatio'].split(' : '))
    total_students = row['Nostudent']
    male_students = round((male_ratio / (male_ratio + female_ratio)) * total_students)
    female_students = round((female_ratio / (male_ratio + female_ratio)) * total_students)
    return pd.Series({'Male_Students': male_students, 'Female_Students': female_students})

# Apply the function to each row and create new columns
data[['Male_Students', 'Female_Students']] = data.apply(calculate_gender_students, axis=1)

# Save the updated DataFrame to a new CSV file
output_csv = 'data/top_100_with_gender_students_rounded.csv'  # Replace with the desired output file path
data.to_csv(output_csv, index=False)

print("Processing complete. Data saved to", output_csv)
