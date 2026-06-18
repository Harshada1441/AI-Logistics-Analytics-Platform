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



if __name__ == "__main__":
    app.run(debug=True)