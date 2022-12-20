import os
import sys
from flask import Flask
import requests, json
parent = os.path.abspath(os.path.join(os.path.dirname(__file__),'..')) #this should give you absolute location of my_project folder.
sys.path.append(parent)
from db.db_manager import DatabaseManager

app = Flask(__name__)
url_incidencias = "https://api.status.salesforce.com/v1/incidents?instance=EU48&locale=es"
url_cambios = "https://api.status.salesforce.com/v1/maintenances?instance=EU48"
filepath = "../data/"

@app.route("/update_data_json", methods=['POST'])
def update_data_json():
    try:
        request_incidencias = requests.get(url_incidencias)
        request_cambios = requests.get(url_cambios)
        with open(f"{filepath}incidencias.json", "w+") as json_file:
            json.dump(json.loads(request_incidencias.text), json_file, indent=4)
            json_file.close()
        with open(f"{filepath}cambios.json", "w+") as json_file:
            json.dump(json.loads(request_cambios.text), json_file, indent=4)
            json_file.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "failed", "message": str(e)}

@app.route("/connect_database_test", methods=["POST"])
def connect_database():
    try:
        database = DatabaseManager()
        database.cursor.execute("SHOW TABLES")
        for table_name in database.cursor:
            print(table_name)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failed", "message": str(e)}

@app.route("/update_data_database", methods=['POST'])
def update_data_database():
    try:
        database = DatabaseManager()
        update_data_json()
        database.add_incidencias()
        database.add_cambios()
        return {"status": "success"}
    except Exception as e:
        return {"status": "failed", "message": str(e)}

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8082))
    app.run(host="0.0.0.0", port=port)