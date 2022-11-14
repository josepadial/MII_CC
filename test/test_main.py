import os, sys
parent = os.path.abspath(os.path.join(os.path.dirname(__file__),'..')) #this should give you absolute location of my_project folder.
sys.path.append(parent)
from db.db_manager import DatabaseManager
import requests, json

def test_connect_database():
    database = DatabaseManager()
    assert database.connection is not None

def test_get_tables():
    database = DatabaseManager()
    database.cursor.execute("SHOW TABLES")
    tables = database.cursor.fetchall()
    tables = [item for t in tables for item in t]
    assert len(tables) == 2

def test_api_request():
    url_incidencias = "https://api.status.salesforce.com/v1/incidents?instance=EU48&locale=es"
    url_cambios = "https://api.status.salesforce.com/v1/maintenances?instance=EU48"
    request_incidencias = requests.get(url_incidencias)
    request_cambios = requests.get(url_cambios)
    assert request_incidencias.status_code == 200
    assert request_cambios.status_code == 200

def test_read_json_file():
    with open(f"./data/cambios.json", "r") as json_file:
        cambios = json.load(json_file)
        assert type(cambios) is list
        json_file.close()
    with open(f"./data/incidencias.json", "r") as json_file:
        incidencias = json.load(json_file)
        assert type(incidencias) is list
        json_file.close()
