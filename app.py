import os
import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template

# Optional: enable CORS if needed
try:
    from flask_cors import CORS
    cors_enabled = True
except ImportError:
    cors_enabled = False

# ---------------- Setup Flask ----------------
app = Flask(__name__)
if cors_enabled:
    CORS(app)

# ---------------- Load Model & Scaler ----------------
base_path = os.path.dirname(__file__)
regmodel = pickle.load(open(os.path.join(base_path, 'regmodel.pkl'), 'rb'))
scaler = pickle.load(open(os.path.join(base_path, 'scaler.pkl'), 'rb'))

# Explicit feature order (must match training time!)
feature_order = [
    "MedInc", "HouseAge", "AveRooms", "AveBedrms",
    "Population", "AveOccup", "Latitude", "Longitude"
]

# ---------------- Routes ----------------
@app.route('/')
def home():
    """Render homepage with input form"""
    return render_template('home.html')


@app.route('/predict_api', methods=['POST'])
def predict_api():
    """API endpoint for Postman or external apps"""
    try:
        data = request.get_json(force=True)
        print("Raw input:", data)

        if not data or "data" not in data:
            return jsonify({"error": "JSON must contain a 'data' key"}), 400

        data = data["data"]

        # Case 1: dict of features
        if isinstance(data, dict):
            try:
                features = np.array([data[feat] for feat in feature_order]).reshape(1, -1)
            except KeyError as e:
                return jsonify({"error": f"Missing feature: {e.args[0]}"}), 400

        # Case 2: list of values (order must match feature_order)
        elif isinstance(data, list):
            if len(data) != len(feature_order):
                return jsonify({
                    "error": f"Expected {len(feature_order)} features, got {len(data)}"
                }), 400
            features = np.array(data).reshape(1, -1)

        else:
            return jsonify({"error": "Invalid input format. Must be dict or list."}), 400

        # Scale + Predict
        scaled_features = scaler.transform(features)
        prediction = float(regmodel.predict(scaled_features).ravel()[0])
        prediction = round(prediction, 2)  # <-- rounding applied

        print("Prediction:", prediction)

        return jsonify({
            "input": data,
            "prediction": prediction,
            "features_used": feature_order,  # <-- added
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/predict', methods=['POST'])
def predict():
    """Form submission route for website"""
    try:
        # Extract form values → convert to float
        data = [float(x) for x in request.form.values()]
        if len(data) != len(feature_order):
            return render_template(
                "home.html",
                prediction_text=f"Error: Expected {len(feature_order)} values, got {len(data)}"
            )

        features = np.array(data).reshape(1, -1)
        scaled_features = scaler.transform(features)

        # Predict
        prediction = float(regmodel.predict(scaled_features).ravel()[0])
        prediction = round(prediction, 2)  # <-- rounding applied
        print("Prediction (form):", prediction)

        return render_template(
            "home.html",
            prediction_text=f"The House price prediction is {prediction}"
        )

    except Exception as e:
        return render_template(
            "home.html",
            prediction_text=f"Error: {str(e)}"
        )


# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(debug=True)
     # Use PORT env variable if available (CI/CD), default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


