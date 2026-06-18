import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

print("=" * 50)
print("ETA PREDICTION MODEL")
print("=" * 50)

# Load Dataset
df = pd.read_csv(
    "data/processed/logistics_featured.csv"
)

# Features
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

target = "Delay_Days"

data = df[features + [target]].copy()

# Encode Categorical Columns

eta_encoders = {}

for col in data.select_dtypes(include="object").columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(
        data[col].astype(str)
    )
    eta_encoders[col] = le

# X and y

X = data[features]
y = data[target]

# Train Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Prediction

y_pred = model.predict(X_test)

# Evaluation

mae = mean_absolute_error(
    y_test,
    y_pred
)

r2 = r2_score(
    y_test,
    y_pred
)

print("\nMAE:", round(mae, 2))
print("R2 Score:", round(r2, 2))

# Save Model

joblib.dump(
    model,
    "models/eta_prediction_model.pkl"
)

joblib.dump(
    eta_encoders,
    "models/eta_encoders.pkl"
)
print("\nDelay Days Statistics")
print(df["Delay_Days"].describe())
print("\nETA Model Saved Successfully!")