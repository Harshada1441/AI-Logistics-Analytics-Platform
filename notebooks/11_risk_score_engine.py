import pandas as pd

print("=" * 50)
print("RISK SCORE ENGINE")
print("=" * 50)

# ==========================
# Load Dataset
# ==========================

df = pd.read_csv(
    "data/processed/logistics_featured.csv"
)

# ==========================
# Freight Cost Score
# ==========================

df["Freight_Score"] = pd.cut(
    df["Freight Cost (USD)"],
    bins=[0, 5000, 10000, 20000, 50000, float("inf")],
    labels=[1, 3, 5, 7, 10]
)

# ==========================
# Weight Score
# ==========================

df["Weight_Score"] = pd.cut(
    df["Weight (Kilograms)"],
    bins=[-1, 500, 2000, 5000, 10000, float("inf")],
    labels=[1, 3, 5, 7, 10]
)

# Convert to float

df["Freight_Score"] = (
    df["Freight_Score"]
    .astype(float)
)

df["Weight_Score"] = (
    df["Weight_Score"]
    .astype(float)
)

# ==========================
# Shipment Mode Score
# ==========================

shipment_risk = {
    "Air": 3,
    "Truck": 5,
    "Ocean": 8,
    "Air Charter": 6
}

df["Shipment_Score"] = (
    df["Shipment Mode"]
    .map(shipment_risk)
)

# Fill Missing Values

df["Shipment_Score"] = (
    df["Shipment_Score"]
    .fillna(5)
)

# ==========================
# Final Risk Score
# ==========================

df["Risk_Score"] = (
    df["Freight_Score"]
    + df["Weight_Score"]
    + df["Shipment_Score"]
) / 3

# ==========================
# Risk Category
# ==========================

def risk_category(score):

    if score >= 7:
        return "High Risk"

    elif score >= 4:
        return "Medium Risk"

    else:
        return "Low Risk"


df["Risk_Category"] = (
    df["Risk_Score"]
    .apply(risk_category)
)

# ==========================
# Output
# ==========================

print("\nRisk Distribution")
print(
    df["Risk_Category"]
    .value_counts()
)

print("\nAverage Risk Score")
print(
    round(
        df["Risk_Score"].mean(),
        2
    )
)

# ==========================
# Save Dataset
# ==========================

df.to_csv(
    "data/processed/logistics_risk_scored.csv",
    index=False
)

print("\nRisk Score Dataset Saved Successfully!")
print(
    "Saved:",
    "data/processed/logistics_risk_scored.csv"
)