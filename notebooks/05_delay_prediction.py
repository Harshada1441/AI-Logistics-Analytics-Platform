import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# ==========================
# Load Dataset
# ==========================

df = pd.read_csv("data/processed/logistics_featured.csv")

# ==========================
# Select Features
# ==========================

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

target = "Delayed"

data = df[features + [target]].copy()

# ==========================
# Encode Categorical Columns
# ==========================

le_dict = {}

for col in data.select_dtypes(include="object").columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col].astype(str))
    le_dict[col] = le

# ==========================
# Train Test Split
# ==========================

X = data[features]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================
# Train Model
# ==========================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ==========================
# Prediction
# ==========================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("=" * 50)
print("MODEL ACCURACY")
print("=" * 50)
print(round(accuracy * 100, 2), "%")

print("\nClassification Report")
print(classification_report(y_test, y_pred))

# ==========================
# Save Model
# ==========================

joblib.dump(
    model,
    "models/delay_prediction_model.pkl"
)

print("\n Model Saved Successfully!")