""" Main application file for the backend service. """
import os
import time
import requests
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from remla24_team8_lib_version import versioning


app = Flask(__name__)
CORS(app)

model_service_url = os.getenv("MODEL_SERVICE_URL", "http://localhost:5000")

REQUEST_COUNT = Counter("page_requests_total", "Total number of requests to the page")
TOTAL_PREDICTIONS = Counter(
    "prediction_requests_total", "Total number of prediction requests"
)
PREDICTION_LATENCY = Histogram(
    "prediction_latency_seconds", "Latency of prediction requests in seconds"
)
SCAM_PREDICTIONS = Counter("scam_predictions", "Number of scam predictions")
SCAM_PERCENTAGE = Gauge(
    "scam_percentage", "Percentage of predictions that are classified as scams"
)


@app.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint for making predictions.

    Increments the request counters, records the prediction latency,
    checks if the prediction is classified as a scam, and updates the scam percentage gauge.

    Returns:
        JSON response containing the prediction result.
    """
    REQUEST_COUNT.inc()
    TOTAL_PREDICTIONS.inc()
    start_time = time.time()

    input_data = request.json

    try:
        response = requests.post(f"{model_service_url}/predict", json=input_data)
        response.raise_for_status()
        result = response.json()

        PREDICTION_LATENCY.observe(time.time() - start_time)

        score = result.get("score", 0)[0]
        if score > 0.5:
            SCAM_PREDICTIONS.inc()

        total_predictions = TOTAL_PREDICTIONS._value.get()
        scam_predictions = SCAM_PREDICTIONS._value.get()
        if total_predictions > 0:
            scam_rate = 100 * scam_predictions / total_predictions
            SCAM_PERCENTAGE.set(scam_rate)

        return jsonify(result)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route("/version", methods=["GET"])
def version():
    """
    Endpoint for retrieving the version of the application.

    Returns:
        JSON response containing the version number.
    """
    util = versioning.VersionUtil()
    received_version = util.version
    return jsonify({"version": received_version})


@app.route("/metrics", methods=["GET"])
def metrics():
    """
    Endpoint for serving the metrics page.

    Returns:
        Prometheus metrics in the latest format.
    """
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
