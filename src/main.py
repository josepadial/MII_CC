import os
from flask import Flask
import requests, json

app = Flask(__name__)
url_incidencias = "https://api.status.salesforce.com/v1/incidents?instance=EU48&locale=es"
url_cambios = "https://api.status.salesforce.com/v1/maintenances?instance=EU48"
filepath = "../data/"

@app.route("/update_data", methods=['POST'])
def update_data():
    request_incidencias = requests.get(url_incidencias)
    request_cambios = requests.get(url_cambios)
    try:
        with open(f"{filepath}incidencias.json", "w") as json_file:
            json.dump(json.loads(request_incidencias.text), json_file, indent=2, separators=(',',': '))
            json_file.close()
        with open(f"{filepath}cambios.json", "w") as json_file:
            json.dump(json.loads(request_cambios.text), json_file, indent=2, separators=(',',': '))
            json_file.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "failed", "message": str(e)}

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8080))
    app.run(host="0.0.0.0", port=port)