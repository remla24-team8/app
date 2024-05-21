from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)
model_service_url = os.getenv('MODEL_SERVICE_URL', 'http://localhost:5000')

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.json
    response = requests.post(f'{model_service_url}/predict', json=input_data)
    return jsonify(response.json())

@app.route('/version', methods=['GET'])
def version():
    return jsonify({"version": 'dummy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
