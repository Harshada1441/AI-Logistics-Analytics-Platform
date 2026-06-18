import pandas as pd
import numpy as np

# ==========================
# Load Dataset
# ==========================

df = pd.read_csv("data/raw/SCMS_Delivery_History_Dataset.csv")

print("=" * 50)
print("ORIGINAL DATASET SHAPE")
print("=" * 50)
print(df.shape)

# ==========================
# Handle Missing Values
# ==========================

# Insurance Column
df["Line Item Insurance (USD)"] = df["Line Item Insurance (USD)"].fillna(
    df["Line Item Insurance (USD)"].median()
)

# Shipment Mode
df["Shipment Mode"] = df["Shipment Mode"].fillna(
    df["Shipment Mode"].mode()[0]
)

# Dosage
df["Dosage"] = df["Dosage"].fillna(
    "Unknown"
)

# ==========================
# Convert Numeric Columns
# ==========================

df["Weight (Kilograms)"] = pd.to_numeric(
    df["Weight (Kilograms)"],
    errors="coerce"
)

df["Freight Cost (USD)"] = pd.to_numeric(
    df["Freight Cost (USD)"],
    errors="coerce"
)

# ==========================
# Fill Numeric Missing Values
# ==========================

df["Weight (Kilograms)"] = df["Weight (Kilograms)"].fillna(
    df["Weight (Kilograms)"].median()
)

df["Freight Cost (USD)"] = df["Freight Cost (USD)"].fillna(
    df["Freight Cost (USD)"].median()
)

# ==========================
# Remove Duplicates
# ==========================

before_rows = df.shape[0]

df = df.drop_duplicates()

after_rows = df.shape[0]

print("\nDuplicates Removed:", before_rows - after_rows)

# ==========================
# Final Validation
# ==========================

print("\n" + "=" * 50)
print("FINAL DATASET SHAPE")
print("=" * 50)
print(df.shape)

print("\n" + "=" * 50)
print("TOTAL MISSING VALUES")
print("=" * 50)
print(df.isnull().sum().sum())

print("\n" + "=" * 50)
print("COLUMN DATA TYPES")
print("=" * 50)
print(df.dtypes)

# ==========================
# Save Clean Dataset
# ==========================

df.to_csv(
    "data/processed/logistics_cleaned.csv",
    index=False
)

print("\n Cleaned Dataset Saved Successfully!")
print("Location: data/processed/logistics_cleaned.csv")