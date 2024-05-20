from flask import Flask, jsonify, request, send_from_directory
from lib_version.versioning import Version_Util
import os
import requests
app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
model_service_url = os.getenv('MODEL_SERVICE_URL', 'http://localhost:5000')

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/version', methods=['GET'])
def version():
    util = Version_Util()
    return jsonify({"version": util.get_version_from_setup()})

@app.route('/api/predict', methods=['POST'])
def predict():
    input_data = request.json
    # Replace this with your prediction logic
    response = requests.post(f'{model_service_url}/predict', json=input_data)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
