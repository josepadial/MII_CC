import pymysql
import os, sys
import json
from datetime import datetime
from dateutil import tz
parent = os.path.abspath(os.path.join(os.path.dirname(__file__),'..')) #this should give you absolute location of my_project folder.
sys.path.append(parent)
from emails.email import EmailManager


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
        self.email = EmailManager()
        self.connect()

    def connect(self):
        try:
            self.connection = pymysql.connect(host=os.getenv('HOST_DB', '10.5.0.5'), user=os.getenv('USER_DB', 'root'),
                                              passwd=os.getenv('PASSWORD_DB', '1234'), database="ALERT-ME")
            self.cursor = self.connection.cursor()
        except pymysql.OperationalError as e:
            print(e)

    def ulify(self, elements):
        if elements is None:
            string = "No hay servicios afectados"
        else:
            string = "<ul>\n"
            for s in elements:
                string += "<li>" + str(s) + "</li>\n"
            string += "</ul>"
        return string

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
                    incident_html = {"info_relevante": {}, "info_adicional": {}, "info_relevante_url": {},
                                     "info_adicional_url": {}, "titulo": ""}
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

                    incident_html["titulo"] = message
                    incident_html["info_relevante"]["Creación de la incidencia"] = created_at
                    incident_html["info_relevante"]["Actualización de la incidencia"] = updated_at
                    incident_html["info_relevante"]["Severity"] = is_core
                    incident_html["info_adicional"]["ID"] = id_inc
                    incident_html["info_adicional"]["Información"] = additional_information
                    incident_html["info_adicional"]["Servicios afectados"] = self.ulify(incidencia["serviceKeys"])
                    incident_html["info_adicional"]["Instancias afectados"] = self.ulify(incidencia["instanceKeys"])

                    self.email.send_email(data=incident_html, subject=f"Resumen de la incidencia {id_inc}", incidencias=True)

                    self.cursor.execute(f"INSERT INTO incidencias (id, externalId, message, additionalInformation,"
                                        f"isCore, affectsAll, createdAt, updatedAt, IncidentImpacts,"
                                        f"IncidentEvents, instanceKeys, serviceKeys) VALUES ('{id_inc}', '{external_id}', "
                                        f"'{message}', '{additional_information}', {is_core},"
                                        f"{affects_all}, '{created_at}', '{updated_at}',"
                                        f"'{incident_impacts}', '{incident_events}', '{instance_keys}', '{service_keys}')")
            self.connection.commit()
            return f"Se ha actualizado correctamente la BBDD de incidencias"
        except pymysql.OperationalError as e:
            return f"Se ha producido el siguiente fallo {e}"

    def add_incident_post(self, id_inc, external_id, message, additional_information, is_core, affects_all, created_at, updated_at, incident_impacts, incident_events, instance_keys, service_keys):
        try:
            self.cursor.execute(f"INSERT INTO incidencias (id, externalId, message, additionalInformation,"
                                f"isCore, affectsAll, createdAt, updatedAt, IncidentImpacts,"
                                f"IncidentEvents, instanceKeys, serviceKeys) VALUES ('{id_inc}', '{external_id}', "
                                f"'{message}', '{additional_information}', {is_core},"
                                f"{affects_all}, '{created_at}', '{updated_at}',"
                                f"'{incident_impacts}', '{incident_events}', '{instance_keys}', '{service_keys}')")
            self.connection.commit()
            return f"Se ha añadido correctamente la incidencia a la BBDD"
        except pymysql.OperationalError as e:
            return f"Se ha producido el siguiente fallo {e}"

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
                    change_html = {"info_relevante": {}, "info_adicional": {}, "info_relevante_url": {},
                                   "info_adicional_url": {}, "titulo": ""}
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

                    change_html["titulo"] = name
                    change_html["info_relevante"]["Creación de la incidencia"] = created_at
                    change_html["info_relevante"]["Actualización de la incidencia"] = updated_at
                    change_html["info_relevante"]["Severity"] = is_core
                    change_html["info_adicional"]["ID"] = id_ch
                    change_html["info_adicional"]["Información"] = additional_information
                    change_html["info_adicional"]["Servicios afectados"] = self.ulify(cambio["serviceKeys"])
                    change_html["info_adicional"]["Instancias afectados"] = self.ulify(cambio["instanceKeys"])

                    self.email.send_email(change_html, f"Resumen del cambio {id_ch}", False)

                    self.cursor.execute(f"INSERT INTO cambios (id, message, externalId, name_ch, plannedStartTime,"
                                        f"plannedEndTime, additionalInformation, isCore, affectsAll, createdAt,"
                                        f"updatedAt, MaintenanceImpacts, MaintenanceEvents, instanceKeys, serviceKeys)"
                                        f"VALUES ('{id_ch}', '{message}', '{external_id}', '{name}', '{planned_start_time}',"
                                        f"'{planned_end_time}', '{additional_information}', {is_core}, {affects_all},"
                                        f"'{created_at}', '{updated_at}', '{maintenance_impacts}', '{maintenance_events}',"
                                        f"'{instance_keys}', '{service_keys}')")
            self.connection.commit()
            return f"Se ha actualizado correctamente la BBDD de cambios"
        except pymysql.OperationalError as e:
            print(e)

    def add_maintenance_post(self, id_ch, external_id, message, additional_information, name, planned_start_time, planned_end_time, is_core, affects_all, created_at, updated_at, maintenance_impacts, maintenance_events, instance_keys, service_keys):
        try:
            self.cursor.execute(f"INSERT INTO cambios (id, message, externalId, name_ch, plannedStartTime,"
                                f"plannedEndTime, additionalInformation, isCore, affectsAll, createdAt,"
                                f"updatedAt, MaintenanceImpacts, MaintenanceEvents, instanceKeys, serviceKeys)"
                                f"VALUES ('{id_ch}', '{message}', '{external_id}', '{name}', '{planned_start_time}',"
                                f"'{planned_end_time}', '{additional_information}', {is_core}, {affects_all},"
                                f"'{created_at}', '{updated_at}', '{maintenance_impacts}', '{maintenance_events}',"
                                f"'{instance_keys}', '{service_keys}')")
            self.connection.commit()
            return f"Se ha añadido correctamente cambio a la BBDD"
        except pymysql.OperationalError as e:
            return f"Se ha producido el siguiente fallo {e}"
    def search_incident_id(self, id_inc):
        try:
            sql_statement = f"SELECT * FROM incidencias WHERE id='{id_inc}'"
            self.cursor.execute(sql_statement)
            result = self.cursor.fetchall()
            if len(result) == 1:
                return result[0]
            else:
                return "Ese ID no se encuentra"
        except pymysql.OperationalError as e:
            return f"Se ha producido el siguiente fallo {e}"

    def delete_incident_id(self, id_inc):
        try:
            sql_statement = f"DELETE FROM incidencias WHERE id='{id_inc}'"
            self.cursor.execute(sql_statement)
            self.connection.commit()
            return "Se ha borrado correctamente la incidencia"
        except pymysql.OperationalError as e:
            return f"Se ha producido el siguiente fallo {e}"

    def delete_all_incident_id(self):
        try:
            sql_statement = f"DELETE FROM incidencias"
            self.cursor.execute(sql_statement)
            self.connection.commit()
            return "Se ha borrado correctamente las incidencias"
        except pymysql.OperationalError as e:
            return f"Se ha producido el siguiente fallo {e}"

    def get_ids_incidents(self):
        try:
            sql_statement = "SELECT id FROM incidencias"
            self.cursor.execute(sql_statement)
            primary_keys = self.cursor.fetchall()
            primary_keys = [item for t in primary_keys for item in t]
            if len(primary_keys) >= 1:
                return primary_keys
            else:
                return ["No se encuentran"]
        except pymysql.OperationalError as e:
            return [f"Se ha producido el siguiente fallo {e}"]

    def search_maintenance_id(self, id_ch):
        try:
            sql_statement = f"SELECT * FROM cambios WHERE id='{id_ch}'"
            self.cursor.execute(sql_statement)
            result = self.cursor.fetchall()
            if len(result) == 1:
                return result[0]
            else:
                return "Ese ID no se encuentra"
        except pymysql.OperationalError as e:
            return f"Se ha producido el siguiente fallo {e}"

    def delete_maintenances_id(self, id_ch):
        try:
            sql_statement = f"DELETE FROM cambios WHERE id='{id_ch}'"
            self.cursor.execute(sql_statement)
            self.connection.commit()
            return "Se ha borrado correctamente el cambio"
        except pymysql.OperationalError as e:
            return f"Se ha producido el siguiente fallo {e}"

    def delete_all_maintenances_id(self):
        try:
            sql_statement = f"DELETE FROM cambios"
            self.cursor.execute(sql_statement)
            self.connection.commit()
            return "Se ha borrado correctamente los cambios"
        except pymysql.OperationalError as e:
            return f"Se ha producido el siguiente fallo {e}"

    def get_ids_maintenances(self):
        try:
            sql_statement = "SELECT id FROM cambios"
            self.cursor.execute(sql_statement)
            primary_keys = self.cursor.fetchall()
            primary_keys = [item for t in primary_keys for item in t]
            if len(primary_keys) >= 1:
                return primary_keys
            else:
                return ["No se encuentran"]
        except pymysql.OperationalError as e:
            return [f"Se ha producido el siguiente fallo {e}"]