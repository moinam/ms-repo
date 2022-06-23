from flask import Flask, render_template, request, jsonify
from backend.helpers import bigquery
app = Flask(__name__)


@app.route("/")
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


@app.post("/team")
def get_team():
    """
        Returns the most fitting team for a task
        POST: /team
        Payload: (JSON)
        - taskType
        - clientId
        - quantity

        Returns: (JSON)
        - servicePoint
        - teamId
        - teamMembers
    """
    # TODO: return best fitting team from bigquery
    # Test: returns all teams
    return jsonify(bigquery.get_teams())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
