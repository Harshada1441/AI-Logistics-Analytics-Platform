from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load Model
model = joblib.load("models/delay_prediction_model.pkl")

# Load Encoders
encoders = joblib.load("models/label_encoders.pkl")

print("Country Classes:")
print(encoders["Country"].classes_)

print("\nShipment Mode Classes:")
print(encoders["Shipment Mode"].classes_)

print("\nProduct Group Classes:")
print(encoders["Product Group"].classes_)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():

    prediction = None

    if request.method == "POST":

        try:

            country = request.form["country"].strip()
            shipment_mode = request.form["shipment_mode"].strip()
            product_group = request.form["product_group"].strip()

            quantity = float(request.form["quantity"])
            line_value = float(request.form["line_value"])
            pack_price = float(request.form["pack_price"])
            unit_price = float(request.form["unit_price"])
            weight = float(request.form["weight"])
            freight_cost = float(request.form["freight_cost"])

            # Encode categorical variables

            country_encoded = encoders["Country"].transform(
                [country]
            )[0]

            shipment_encoded = encoders["Shipment Mode"].transform(
                [shipment_mode]
            )[0]

            product_encoded = encoders["Product Group"].transform(
                [product_group]
            )[0]

            # Create DataFrame

            input_data = pd.DataFrame(
                [[
                    country_encoded,
                    shipment_encoded,
                    product_encoded,
                    quantity,
                    line_value,
                    pack_price,
                    unit_price,
                    weight,
                    freight_cost
                ]],
                columns=[
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
            )

            # Prediction

            result = model.predict(input_data)

            if result[0] == 1:
                prediction = "🚨 Shipment Likely Delayed"
            else:
                prediction = "✅ Shipment Likely On Time"

        except Exception as e:

            prediction = f"ERROR: {str(e)}"

            print("\n====================")
            print("PREDICTION ERROR")
            print("====================")
            print(e)

    return render_template(
        "predict.html",
        prediction=prediction
    )


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


@app.route("/riskscore", methods=["GET", "POST"])
def riskscore():

    risk_score = None
    risk_category = None

    if request.method == "POST":

        shipment_mode = request.form["shipment_mode"]

        weight = float(
            request.form["weight"]
        )

        freight_cost = float(
            request.form["freight_cost"]
        )

        # Freight Score

        if freight_cost > 50000:
            freight_score = 10
        elif freight_cost > 20000:
            freight_score = 7
        elif freight_cost > 10000:
            freight_score = 5
        elif freight_cost > 5000:
            freight_score = 3
        else:
            freight_score = 1

        # Weight Score

        if weight > 10000:
            weight_score = 10
        elif weight > 5000:
            weight_score = 7
        elif weight > 2000:
            weight_score = 5
        elif weight > 500:
            weight_score = 3
        else:
            weight_score = 1

        # Shipment Mode Score

        shipment_scores = {
            "Air": 3,
            "Truck": 5,
            "Ocean": 8,
            "Air Charter": 6
        }

        shipment_score = shipment_scores.get(
            shipment_mode,
            5
        )

        risk_score = round(
            (
                freight_score +
                weight_score +
                shipment_score
            ) / 3,
            2
        )

        if risk_score >= 7:
            risk_category = "🔴 High Risk"

        elif risk_score >= 4:
            risk_category = "🟡 Medium Risk"

        else:
            risk_category = "🟢 Low Risk"

    return render_template(
        "riskscore.html",
        risk_score=risk_score,
        risk_category=risk_category
    )


if __name__ == "__main__":
    app.run(debug=True)