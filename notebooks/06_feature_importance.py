import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load Model
model = joblib.load(
    "models/delay_prediction_model.pkl"
)

features = [
    "Country",
    "Shipment Mode",
    "Product Group",
    "Line Item Quantity",
    "Line Item Value",
    "Pack Price",
    "Unit Price",
    "Weight (Kilograms)",
    "Freight Cost (USD)"
]

importance = model.feature_importances_

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": importance
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print(importance_df)

plt.figure(figsize=(10,5))
plt.barh(
    importance_df["Feature"],
    importance_df["Importance"]
)

plt.title("Feature Importance")
plt.tight_layout()

plt.savefig(
    "reports/feature_importance.png"
)

plt.show()