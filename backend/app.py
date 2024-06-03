from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import os
import time
from prometheus_client import start_http_server, Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from remla24_team8_lib_version import versioning


# Flask app setup
app = Flask(__name__)
CORS(app)

# Environment variables
model_service_url = os.getenv('MODEL_SERVICE_URL', 'http://localhost:5000')

# Metrics definitions
REQUEST_COUNT = Counter('page_requests_total', 'Total number of requests to the page')
TOTAL_PREDICTIONS = Counter('prediction_requests_total', 'Total number of prediction requests')
PREDICTION_LATENCY = Histogram('prediction_latency_seconds', 'Latency of prediction requests in seconds')
SCAM_PREDICTIONS = Counter('scam_predictions', 'Number of scam predictions')
SCAM_PERCENTAGE = Gauge('scam_percentage', 'Percentage of predictions that are classified as scams')

@app.route('/predict', methods=['POST'])
def predict():
    REQUEST_COUNT.inc()
    TOTAL_PREDICTIONS.inc()
    start_time = time.time()

    # Get JSON data from request
    input_data = request.json
    
    try:
        # Send data to model service and get response
        response = requests.post(f'{model_service_url}/predict', json=input_data)
        response.raise_for_status()  # Raises HTTPError for bad requests (4XX or 5XX)
        result = response.json()

        
        # Record latency
        PREDICTION_LATENCY.observe(time.time() - start_time)
        
        score = result.get('score', 0)[0]
        # Check if the prediction is classified as a scam
        if score > 0.5:
            SCAM_PREDICTIONS.inc()

        # Update scam percentage gauge
        total_predictions = TOTAL_PREDICTIONS._value.get()  # Use internal method to get the count
        scam_predictions = SCAM_PREDICTIONS._value.get()
        if total_predictions > 0:  # Avoid division by zero
            scam_rate = 100 * scam_predictions / total_predictions
            SCAM_PERCENTAGE.set(scam_rate)


        return jsonify(result)
    
    except requests.exceptions.RequestException as e:
        # Handle errors in connecting to the model service or processing the request
        return jsonify({'error': str(e)}), 500

@app.route('/version', methods=['GET'])
def version():
    util = versioning.VersionUtil()
    received_version = util.version
    return jsonify({"version": received_version})

@app.route('/metrics', methods=['GET'])
def metrics():
    # Serve the metrics page
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    # Optionally start a Prometheus metrics server on a different port if needed
    # start_http_server(8000)
    app.run(host='0.0.0.0', port=5001)
