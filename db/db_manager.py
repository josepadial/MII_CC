import pymysql
import os
import json
from datetime import datetime
from dateutil import tz


def format_date(date, op=True, zone="UTC"):
    from_zone = tz.gettz(zone)
    to_zone = tz.gettz("Europe/Paris")
    utc_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    utc_date = utc_date.replace(tzinfo=from_zone)
    local_date = utc_date.astimezone(to_zone)
    local_date_str = datetime.strftime(local_date, "%Y-%m-%d %H:%M:%S")
    if op:
        return local_date
    else:
        return local_date_str


class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.filepath = "../data/"

        self.connect()

    def connect(self):
        try:
            self.connection = pymysql.connect(host=os.getenv('HOST_DB', 'localhost'), user=os.getenv('USER_DB', 'root'),
                                              passwd=os.getenv('PASSWORD_DB', '1234'), database="ALERT-ME")
            self.cursor = self.connection.cursor()
        except pymysql.OperationalError as e:
            print(e)

    def add_incidencias(self):
        try:
            with open(f"{self.filepath}incidencias.json", "r") as json_file:
                incidencias = json.load(json_file)
                json_file.close()
            sql_statement = "SELECT id FROM incidencias"
            self.cursor.execute(sql_statement)
            primary_keys = self.cursor.fetchall()
            primary_keys = [item for t in primary_keys for item in t]
            for incidencia in incidencias:
                if incidencia['id'] not in primary_keys:
                    id_inc = incidencia["id"]
                    external_id = incidencia["externalId"]
                    message = json.dumps(incidencia["message"]).replace("'", "")
                    if incidencia["additionalInformation"] != "" and incidencia["additionalInformation"] is not None:
                        additional_information = incidencia["additionalInformation"].replace("'", "")
                    else:
                        additional_information = None
                    is_core = incidencia["isCore"]
                    affects_all = incidencia["affectsAll"]
                    created_at = format_date(incidencia["createdAt"], False)
                    updated_at = format_date(incidencia["updatedAt"], False)
                    if incidencia["IncidentImpacts"]:
                        incidencia["IncidentImpacts"][0]["id"] = str(incidencia["IncidentImpacts"][0]["id"])
                        incident_impacts = json.dumps(incidencia["IncidentImpacts"][0]).replace("'", "")
                    else:
                        incident_impacts = None
                    if incidencia["IncidentEvents"]:
                        incidencia["IncidentEvents"][0]["id"] = str(incidencia["IncidentEvents"][0]["id"])
                        incident_events = json.dumps(incidencia["IncidentEvents"][0]).replace("'", "")
                    else:
                        incident_events = None
                    instance_keys = ""
                    if incidencia["instanceKeys"]:
                        instance_keys = instance_keys.join(incidencia["instanceKeys"]).replace("'", "")
                    else:
                        instance_keys = None
                    service_keys = ""
                    if incidencia["serviceKeys"]:
                        service_keys = service_keys.join(incidencia["serviceKeys"]).replace("'", "")
                    else:
                        service_keys = None

                    self.cursor.execute(f"INSERT INTO incidencias (id, externalId, message, additionalInformation,"
                                        f"isCore, affectsAll, createdAt, updatedAt, IncidentImpacts,"
                                        f"IncidentEvents, instanceKeys, serviceKeys) VALUES ('{id_inc}', '{external_id}', "
                                        f"'{message}', '{additional_information}', {is_core},"
                                        f"{affects_all}, '{created_at}', '{updated_at}',"
                                        f"'{incident_impacts}', '{incident_events}', '{instance_keys}', '{service_keys}')")
            self.connection.commit()
        except pymysql.OperationalError as e:
            print(e)

    def add_cambios(self):
        try:
            with open(f"{self.filepath}cambios.json", "r") as json_file:
                cambios = json.load(json_file)
                json_file.close()
            sql_statement = "SELECT id FROM cambios"
            self.cursor.execute(sql_statement)
            primary_keys = self.cursor.fetchall()
            primary_keys = [item for t in primary_keys for item in t]
            for cambio in cambios:
                if cambio['id'] not in primary_keys:
                    id_ch = cambio["id"]
                    message = json.dumps(cambio["message"]).replace("'", "")
                    external_id = cambio["externalId"].replace("'", "")
                    name = cambio["name"].replace("'", "")
                    planned_start_time = format_date(cambio["plannedStartTime"], False)
                    planned_end_time = format_date(cambio["plannedEndTime"], False)
                    if cambio["additionalInformation"] != "" and cambio["additionalInformation"] is not None:
                        additional_information = cambio["additionalInformation"].replace("'", "")
                    else:
                        additional_information = None
                    is_core = cambio["isCore"]
                    affects_all = cambio["affectsAll"]
                    created_at = format_date(cambio["createdAt"], False)
                    updated_at = format_date(cambio["updatedAt"], False)
                    if cambio["MaintenanceImpacts"]:
                        cambio["MaintenanceImpacts"][0]["id"] = str(cambio["MaintenanceImpacts"][0]["id"])
                        maintenance_impacts = json.dumps(cambio["MaintenanceImpacts"][0]).replace("'", "")
                    else:
                        maintenance_impacts = None
                    if cambio["MaintenanceEvents"]:
                        cambio["MaintenanceEvents"][0]["id"] = str(cambio["MaintenanceEvents"][0]["id"])
                        maintenance_events = json.dumps(cambio["MaintenanceEvents"][0]).replace("'", "")
                    else:
                        maintenance_events = None
                    instance_keys = ""
                    if cambio["instanceKeys"]:
                        instance_keys = instance_keys.join(cambio["instanceKeys"]).replace("'", "")
                    else:
                        instance_keys = None
                    service_keys = ""
                    if cambio["serviceKeys"]:
                        service_keys = service_keys.join(cambio["serviceKeys"]).replace("'", "")
                    else:
                        service_keys = None
                    self.cursor.execute(f"INSERT INTO cambios (id, message, externalId, name_ch, plannedStartTime,"
                                        f"plannedEndTime, additionalInformation, isCore, affectsAll, createdAt,"
                                        f"updatedAt, MaintenanceImpacts, MaintenanceEvents, instanceKeys, serviceKeys)"
                                        f"VALUES ('{id_ch}', '{message}', '{external_id}', '{name}', '{planned_start_time}',"
                                        f"'{planned_end_time}', '{additional_information}', {is_core}, {affects_all},"
                                        f"'{created_at}', '{updated_at}', '{maintenance_impacts}', '{maintenance_events}',"
                                        f"'{instance_keys}', '{service_keys}')")
            self.connection.commit()
        except pymysql.OperationalError as e:
            print(e)
