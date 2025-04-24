import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('QueryResults.csv')

# Rename the columns
df.columns = ['Date', 'Tag', 'Posts']

# Drop missing values
df.dropna(inplace=True)

# Remove duplicates
clean = df.drop_duplicates()

# Convert 'Posts' to numeric (just in case)
clean['Posts'] = pd.to_numeric(clean['Posts'], errors='coerce')

# Convert 'Date' column to datetime format
clean['Date'] = pd.to_datetime(clean['Date'])

# Count unique months per language
months_per_language = clean.groupby('Tag')['Date'].nunique()
print("Months of data per language:")
print(months_per_language)

# Language with the fewest months
min_language = months_per_language.idxmin()
min_months = months_per_language.min()
print(f"\nLanguage with the fewest months of data: {min_language} ({min_months} months)")

# Count total entries per language
entries_per_language = clean['Tag'].value_counts()
print("\nEntries per language:")
print(entries_per_language)

# Filter for Java and Python
java_python = clean[clean['Tag'].isin(['java', 'python'])]

# Group and reshape the data
plot_data = java_python.groupby(['Date', 'Tag'])['Posts'].sum().unstack()

# Plot original data
plot_data.plot(figsize=(12, 6))
plt.title('Java vs Python Posts Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Posts')
plt.grid(True)
plt.legend(title='Language')
plt.tight_layout()
plt.show()

# --- Smoothing with 6-month rolling average ---
rolling_avg = plot_data.rolling(window=6).mean()

# Plot smoothed data
rolling_avg.plot(figsize=(12, 6))
plt.title('Java vs Python Posts Over Time (6-Month Rolling Average)')
plt.xlabel('Date')
plt.ylabel('Number of Posts')
plt.grid(True)
plt.legend(title='Language')
plt.tight_layout()
plt.show()
