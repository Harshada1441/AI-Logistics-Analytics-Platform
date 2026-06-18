import pandas as pd

# Load Clean Dataset
df = pd.read_csv("data/processed/logistics_cleaned.csv")

print("=" * 50)
print("DATASET OVERVIEW")
print("=" * 50)

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# -----------------------------------
# Top Countries
# -----------------------------------

print("\nTOP 10 COUNTRIES")
print(df["Country"].value_counts().head(10))

# -----------------------------------
# Shipment Mode
# -----------------------------------

print("\nSHIPMENT MODE ANALYSIS")
print(df["Shipment Mode"].value_counts())

# -----------------------------------
# Top Product Groups
# -----------------------------------

print("\nTOP PRODUCT GROUPS")
print(df["Product Group"].value_counts().head(10))

# -----------------------------------
# Top Vendors
# -----------------------------------

print("\nTOP 10 VENDORS")
print(df["Vendor"].value_counts().head(10))

# -----------------------------------
# Cost Analysis
# -----------------------------------

print("\nFREIGHT COST ANALYSIS")

print("Average Cost:",
      round(df["Freight Cost (USD)"].mean(), 2))

print("Maximum Cost:",
      round(df["Freight Cost (USD)"].max(), 2))

print("Minimum Cost:",
      round(df["Freight Cost (USD)"].min(), 2))

# -----------------------------------
# Weight Analysis
# -----------------------------------

print("\nWEIGHT ANALYSIS")

print("Average Weight:",
      round(df["Weight (Kilograms)"].mean(), 2))

print("Maximum Weight:",
      round(df["Weight (Kilograms)"].max(), 2))

print("Minimum Weight:",
      round(df["Weight (Kilograms)"].min(), 2))