import os
import sys
from flask import Flask, jsonify
from flasgger import Swagger, swag_from
from flask_restful import Api
import config
import requests, json
parent = os.path.abspath(os.path.join(os.path.dirname(__file__),'..')) #this should give you absolute location of my_project folder.
sys.path.append(parent)
from db.db_manager import DatabaseManager

app = Flask(__name__)

template = {
    "swagger": "2.0",
    "info": {
    "title": "ALERT-ME",
    "description": "Sistema de gestión de alertas",
    "version": "5.0.0",
    "contact": {
        "name": "Jose Padial",
        "mail": "josepadial@correo.ugr.es",
    }
    },
    "securityDefinitions": {
        "APIKeyHeader": {"type": "apiKey", "name": "x-access-token", "in": "header"}
    },
    "security": [
        {
          "APIKeyHeader": ["x-access-token"]
        }
    ],
    "response": {
        200: {
            "description": "Success"
        }
    }
}

app.config['SWAGGER'] = {
    'title': 'ALERT-ME',
    'uiversion': 3,
    "specs_route": "/swagger/"
}

swagger = Swagger(app, template=template)
app.config.from_object(config.Config)
api = Api(app)

url_incidencias = "https://api.status.salesforce.com/v1/incidents?instance=EU48&locale=es"
url_cambios = "https://api.status.salesforce.com/v1/maintenances?instance=EU48"
filepath = "../data/"

database = DatabaseManager()

@swag_from(f"swagger/instance.yml", validation=True)
@app.route('/instance', methods=['GET'])
def get_instance():
    return jsonify({
        "Instancia": url_cambios[-4:]
    })

@swag_from(f"swagger/incidents.yml", validation=True)
@app.route("/incidents/<id_inc>", methods=['GET'])
def get_incident_id(id_inc):
    return jsonify({
        "Incident": database.search_incident_id(id_inc)
    })

@swag_from(f"swagger/add_incident.yml", validation=True)
@app.route("/addIncident/<id_inc>/<externalId>/<message>/<additionalInformation>/<isCore>/<affecteAll>/<createdAt>/<updatedAt>/<IncidentImpacts>/<IncidentEvents>/<instanceKeys>/<serviceKeys>", methods=['POST'])
def post_incident(id_inc, externalId, message, additionalInformation, isCore, affecteAll, createdAt, updatedAt, IncidentImpacts, IncidentEvents, instanceKeys, serviceKeys):
    return jsonify({
        "Add incident": database.add_incident_post(id_inc, externalId, message, additionalInformation, isCore, affecteAll, createdAt, updatedAt, IncidentImpacts, IncidentEvents, instanceKeys, serviceKeys)
    })

@swag_from(f"swagger/maintenances.yml", validation=True)
@app.route("/maintenances/<id_ch>", methods=['GET'])
def get_maintenance_id(id_ch):
    return jsonify({
        "Maintenance": database.search_maintenance_id(id_ch)
    })

@swag_from(f"swagger/add_maintenance.yml", validation=True)
@app.route("/addMaintenance/<id_ch>/<externalId>/<message>/<additionalInformation>/<name_ch>/<plannedStartTime>/<plannedEndTime>/<isCore>/<affectsAll>/<createdAt>/<updatedAt>/<MaintenanceImpacts>/<MaintenanceEvents>/<instanceKeys>/<serviceKeys>", methods=['POST'])
def post_maintenance(id_ch, externalId, message, additionalInformation, name_ch, plannedStartTime, plannedEndTime, isCore, affectsAll, createdAt, updatedAt, MaintenanceImpacts, MaintenanceEvents, instanceKeys, serviceKeys):
    return jsonify({
        "Add maintenance": database.add_maintenance_post(id_ch, externalId, message, additionalInformation, name_ch, plannedStartTime, plannedEndTime, isCore, affectsAll, createdAt, updatedAt, MaintenanceImpacts, MaintenanceEvents, instanceKeys, serviceKeys)
    })

@swag_from(f"swagger/delete.yml", validation=True)
@app.route("/delete/<tipo>/<id>", methods=['DELETE'])
def post_delete_maintenances_id(tipo, id):
    if tipo == "Incidencias":
        result = database.delete_incident_id(id)
    else:
        result = database.delete_maintenances_id(id)
    return jsonify({
        "Delete": result
    })
@swag_from(f"swagger/delete_all.yml", validation=True)
@app.route("/deleteAll/<tipo>/<confirmacion>", methods=['DELETE'])
def post_delete_all(tipo, confirmacion):
    if tipo == "Incidencias" and confirmacion == "Si":
        result = database.delete_all_incident_id()
    elif tipo == "Cambios" and confirmacion == "Si":
        result = database.delete_all_maintenances_id()
    else:
        result = f"Para confirmar hay que introducir Si, y se ha introducido {confirmacion}"
    return jsonify({
        "Delete all": result
    })

@swag_from(f"swagger/update.yml", validation=True)
@app.route("/update/<tipo>", methods=['PUT'])
def get_update(tipo):
    return jsonify({
        "Update": update_data_database(tipo)
    })

@swag_from(f"swagger/list_of_ids.yml", validation=True)
@app.route("/listOfIds/<tipo>", methods=['Get'])
def get_list_of_ids(tipo):
    if tipo == "Incidencias":
        result = database.get_ids_incidents()
    else:
        result = database.get_ids_maintenances()
    return jsonify({
        "List of ids": result
    })

@swag_from(f"swagger/test_bbdd.yml", validation=True)
@app.route("/connectDatabaseTest", methods=["GET"])
def connect_database():
    try:
        database = DatabaseManager()
        database.cursor.execute("SHOW TABLES")
        result = "La connexion con la base de datos es correcta"
    except Exception as e:
        result = f"La connexion con la base de datos ha fallado por {e}"
    return jsonify({
        "Estado de la base de datos": result
    })

def update_data_json(tipo):
    try:
        if tipo == "Incidencias":
            request_incidencias = requests.get(url_incidencias)
            with open(f"{filepath}incidencias.json", "w+") as json_file:
                json.dump(json.loads(request_incidencias.text), json_file, indent=4)
                json_file.close()
        else:
            request_cambios = requests.get(url_cambios)
            with open(f"{filepath}cambios.json", "w+") as json_file:
                json.dump(json.loads(request_cambios.text), json_file, indent=4)
                json_file.close()
        return f"Se ha actualizado correctamente el Json de {tipo} en el directorio {filepath}"
    except Exception as e:
        return  f"No se ha actualizado correctamente el Json de {tipo} en el directorio {filepath} por el fallo {e}"

def update_data_database(tipo):
    try:
        result = update_data_json(tipo) + "   "
        if tipo == "Incidencias":
            result += database.add_incidencias()
        else:
            result += database.add_cambios()
        return result
    except Exception as e:
        return  f"No se ha actualizado correctamente la BBDD  de {tipo} por el fallo {e}"

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8082))
    app.run(host="0.0.0.0", port=port, debug=True)