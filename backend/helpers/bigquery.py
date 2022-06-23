from google.cloud import bigquery
from google.oauth2 import service_account
from backend.helpers.configuration import BIGQUERY_CONFIG

PROJECT_NAME = BIGQUERY_CONFIG['project_name']

credentials = service_account.Credentials.from_service_account_file(
    BIGQUERY_CONFIG['credentials_path'])
client = bigquery.Client(credentials=credentials)


def get_teams():
    rows = client.query(
        f"SELECT TeamId, Location FROM `{PROJECT_NAME}.Teams`").result()
    teams = []
    for row in rows:
        teams.append({"teamId": row.TeamId, "location": row.Location})

    return teams


def get_clients():
    rows = client.query(
        f"SELECT ClientId, ClientName, CONCAT(PostalCode, '-', City) as Location FROM `{PROJECT_NAME}.Clients`").result()
    teams = []
    for row in rows:
        teams.append({"clientId": row.ClientId,
                     "name": row.ClientName, "location": row.Location})

    return teams
