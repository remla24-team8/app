# app-backend
This is the app backend, implemented using Flask. It communicates directly with the [model-service](https://github.com/remla24-team8/model-service).

## Running in development

Install `uv`.

Go into the backend folder.

If the dependencies are not up to date, run first `uv pip compile requirements.in -o requirements.txt`.

Install dependencies and the project using `uv pip sync requirements.txt`.

Enter the venv using `. .venv/bin/activate` (or similar for your platform/shell).

Run the service using `flask --app app run`. By default it will run on port 5001.

To connect to the model service, it requires the environment variable MODEL_SERVICE_URL (by default set to localhost:5000).
