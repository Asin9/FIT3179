import pandas as pd

# Read the CSV file
df = pd.read_csv('data/top_100.csv_with_continent__fix.csv')

# Function to calculate FemaleScore and MaleScore based on FemaleMaleRatio and OverAllScore
def calculate_scores(row):
    ratio_str = str(row['FemaleMaleRatio'])
    ratio = [int(part.strip()) for part in ratio_str.replace(':', '').split() if part.isdigit()]
    
    if len(ratio) == 2:
        female_ratio = ratio[0] / (ratio[0] + ratio[1])
        male_ratio = ratio[1] / (ratio[0] + ratio[1])
    else:
        return pd.Series({'FemaleScore': None, 'MaleScore': None})

    female_score = female_ratio * row['OverAllScore']
    male_score = male_ratio * row['OverAllScore']
    
    return pd.Series({'FemaleScore': female_score, 'MaleScore': male_score})

# Apply the function to each row
df[['FemaleScore', 'MaleScore']] = df.apply(calculate_scores, axis=1)

# Save the modified DataFrame to a new CSV file
df.to_csv('top_100_with_scores.csv', index=False)

# Print the first few rows of the modified DataFrame
print(df.head())
