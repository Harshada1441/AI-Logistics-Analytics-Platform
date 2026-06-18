import pandas as pd
import numpy as np

# ==========================
# Load Clean Dataset
# ==========================

df = pd.read_csv("data/processed/logistics_cleaned.csv")

print("=" * 50)
print("FEATURE ENGINEERING STARTED")
print("=" * 50)

# ==========================
# Date Conversion
# ==========================

date_columns = [
    "Scheduled Delivery Date",
    "Delivered to Client Date",
    "Delivery Recorded Date"
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# ==========================
# Delivery Delay Feature
# ==========================

df["Delay_Days"] = (
    df["Delivered to Client Date"]
    - df["Scheduled Delivery Date"]
).dt.days

# ==========================
# Delayed or Not
# ==========================

df["Delayed"] = np.where(
    df["Delay_Days"] > 0,
    1,
    0
)

# ==========================
# Risk Score
# ==========================

df["Risk_Score"] = (
    df["Freight Cost (USD)"]
    / df["Freight Cost (USD)"].max()
) * 10

df["Risk_Score"] = df["Risk_Score"].round(2)

# ==========================
# Order Value Category
# ==========================

df["Order_Category"] = pd.cut(
    df["Line Item Value"],
    bins=[0, 10000, 50000, 1000000],
    labels=["Low", "Medium", "High"]
)

# ==========================
# Business KPIs
# ==========================

total_orders = len(df)
delayed_orders = df["Delayed"].sum()

delay_percentage = round(
    (delayed_orders / total_orders) * 100,
    2
)

print("\nTotal Orders:", total_orders)
print("Delayed Orders:", delayed_orders)
print("Delay Percentage:", delay_percentage, "%")

# ==========================
# Save Featured Dataset
# ==========================

df.to_csv(
    "data/processed/logistics_featured.csv",
    index=False
)

print("\n Feature Engineering Completed")
print(" Saved: logistics_featured.csv")