import json
from flask import Flask, Response, render_template, request, jsonify
# from flask_cors import CORS
from backend.helpers import bigquery
app = Flask(__name__)
# CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/", methods=['GET'])
@app.route("/static/dashboard", methods=['GET'])
@app.route("/static/support", methods=['GET'])
@app.route("/dashboard", methods=['GET'])
@app.route("/support", methods=['GET'])
def main():
    model = {"title": "Maintenance & Service Department."}
    return render_template('index.html', model=model)


@app.get("/clients")
def get_client():
    """
        Returns a list of all clients
        GET: /clients
        Returns: (JSON, Array)
        - clientId
        - name
        - location
    """
    return jsonify(bigquery.get_clients())


@app.get("/types")
def get_task_types():
    """
        Returns a list of all task types
        GET: /types
        Returns: (JSON, String Array)
    """
    return jsonify(bigquery.get_task_types())


@app.post("/predict")
def predict():
    """
        Returns the most fitting team for a task
        POST: /predict
        Payload: (JSON)
        - taskType
        - clientId
        - quantity
        - limit (optional) - max teams that will be returned (defaults to 10)

        Returns: (JSON) [Time data is provided in seconds]
        - teamId
        - location
        - prediction (TimeSpentNorm prediction [in seconds])
        - predictedWorkingTime (TimeSpentNorm prediction multiplied by quantity [in seconds])
        - travelDuration (Time it takes to get to the clients location by driving [in seconds])
        - total (predictedWorkingTime + travelDuration [in seconds])
    """
    content = request.json

    # Check if every required parameter is defined
    if not 'clientId' in content:
        return Response(status=400, content_type='application/json', response=json.dumps({"message": "clientId is missing."}))

    if not 'taskType' in content:
        return Response(status=400, content_type='application/json', response=json.dumps({"message": "taskType is missing."}))

    if not 'quantity' in content:
        return Response(status=400, content_type='application/json', response=json.dumps({"message": "quantity is missing."}))

    # Check if the clientId is valid
    client_id = content['clientId']
    clients = bigquery.get_clients()
    client_found = False
    for client in clients:
        if client['clientId'] == client_id:
            client_found = True

    if not client_found:
        return Response(status=400, content_type='application/json', response=json.dumps({"message": f"Unknown clientId provided."}))

    # Check if the taskType is valid
    task_type = content['taskType']
    task_types = bigquery.get_task_types()
    if not task_type in task_types:
        return Response(status=400, content_type='application/json', response=json.dumps({"message": f"Unknown taskType provided. Allowed: {', '.join(task_types)}"}))

    # Get data from BigQuery
    return jsonify(bigquery.get_time_spent_norm_prediction(
        client_id, task_type, content['quantity'], content['limit'] if 'limit' in content else 10))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
