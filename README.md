# app
The application has a frontend and a service, which can, but do not have to, be implemented separately. The application uses the model service in a sensible use case.

• Depends on the lib-version through a package manager (e.g., Maven). The version is visible in the frontend.

• Queries the model-service through REST requests.

• The URL of the model-service is configurable as an environment variable.


# Usage
In order to start the app only without docker, one must first launch a virtual environment and install dependencies.
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

Afterwards one must launch the backend:
```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
Then the frontend:

```
cd ./frontend
npm run dev

```
