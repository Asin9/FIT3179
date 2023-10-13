import pandas as pd

# Load the CSV data into a Pandas DataFrame
df = pd.read_csv('data/top_100_with_gender_students_decimal.csv')
# Select only numeric columns for correlation calculation
numeric_columns = df.select_dtypes(include=['number'])

# Calculate the correlation matrix for numeric columns
correlation_matrix = numeric_columns.corr()

# Print the correlation matrix
print(correlation_matrix)