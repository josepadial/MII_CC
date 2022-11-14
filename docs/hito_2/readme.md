# Hito 2: Tests
Índice:
<!-- TOC -->
* [Docker](#docker)
* [BBDD](#bbdd)
* [Gestor de tareas](#gestor-de-tareas)
* [Biblioteca de aserciones](#biblioteca-de-aserciones)
* [Marco de pruebas](#marco-de-pruebas)
  * [Base de datos](#base-de-datos)
  * [Acceso a la API del SaaS](#acceso-a-la-api-del-saas)
  * [Lectura de ficheros](#lectura-de-ficheros)
<!-- TOC -->

## Docker
Para el desarrollo de este proyecto se está utilizando Windows 11 junto WSL2(Windows Subsystem Linux 2) con Ubuntu 22.04.
Para este hito se ha instalado Docker Desktop en Windows con la sincronización con Ubuntu.
Se ha creado el script [install-docker-images.sh](../../install/install-docker-images.sh) con el cual
vamos a poder instalar todos los contenedores que requiere el proyecto.

| Docker     | Imagen            | Puerto    | User | Password |
|------------|-------------------|-----------|------|----------|
| Mysql      | mysql:latest      | 3306:3306 | root | 1234     |
| PhpMyAdmin | phpmyadmin:latest | 8081:80   |      |          |

## BBDD
Se crea una base de datos nombrada ALERT-ME. Y se crean las tablas importando el fichero [ALERT-ME.sql](../../sql/ALERT-ME.sql).

## Gestor de tareas
Se ha creado un Makefile con el cual se puede ejecutar el proyecto (make run), hacer los
test (make tests) y limpiar la cache de Python (make clean).
````makefile
VENV = ~/venv-cc
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

run: $(VENV)/bin/activate
	$(PIP) install -r ./src/requirements.txt
	$(PYTHON) ./src/main.py

tests: $(VENV)/bin/activate
	$(PIP) install -r ./src/requirements.txt
	$(PYTHON) -m pytest

clean:
	rm -rf __pycache__
````

## Biblioteca de aserciones
Para la gestión de aserciones en Python se ha utilizado el módulo [pytest](https://docs.pytest.org/en/stable/contents.html).
[pytest](https://docs.pytest.org/en/stable/contents.html) permite utilizar el Python estándar para verificar expectativas y valores en las pruebas de Python.
````python
def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 5
````
Resultado:
````shell
$ pytest
============================= test session starts =============================
collected 1 items

test_sample.py F

================================== FAILURES ===================================
_________________________________ test_answer _________________________________

    def test_answer():
>       assert inc(3) == 5
E       assert 4 == 5
E        +  where 4 = inc(3)

test_sample.py:5: AssertionError
========================== 1 failed in 0.04 seconds ===========================
````
[pytest](https://docs.pytest.org/en/stable/contents.html) tiene soporte para mostrar los valores de las subexpresiones
más comunes incluyendo llamadas, atributos, comparaciones y binarios y unarios Operadores. 
[Demo of Python failure reports with pytest](https://docs.pytest.org/en/stable/example/reportingdemo.html#tbreportdemo)
Esto le permite utilizar el Python idiomático construye sin código repetitivo sin perder Información de introspección.

Sin embargo, si especifica un mensaje con la aserción como este:
````python
assert a % 2 == 0, "value was odd, should be even"
````
Entonces no se produce ninguna introspección de afirmación en absoluto y el mensaje simplemente se mostrará en el rastreo.

## Marco de pruebas
Para las pruebas se ha utilizado el módulo de [pytest](https://docs.pytest.org/en/stable/contents.html)
Se han establecido tres tipos de pruebas:
### Base de datos
Se comprueba que haya conectividad con la base de datos. Y se comprueba que se puedan
obtener las dos tablas de la base de datos.
````python
def test_connect_database():
    database = DatabaseManager()
    assert database.connection is not None

def test_get_tables():
    database = DatabaseManager()
    database.cursor.execute("SHOW TABLES")
    tables = database.cursor.fetchall()
    tables = [item for t in tables for item in t]
    assert len(tables) == 2
````
### Acceso a la API del SaaS
Se comprueba que haya conectividad con la API del SaaS.
````python
def test_api_request():
    url_incidencias = "https://api.status.salesforce.com/v1/incidents?instance=EU48&locale=es"
    url_cambios = "https://api.status.salesforce.com/v1/maintenances?instance=EU48"
    request_incidencias = requests.get(url_incidencias)
    request_cambios = requests.get(url_cambios)
    assert request_incidencias.status_code == 200
    assert request_cambios.status_code == 200
````

### Lectura de ficheros
Se comprueba que se pueda leer los ficheros con la información que guarda la API del SaaS. 
Este test también nos permite probar que esta creada la estructura de las carpetas de los 
datos correctamente.
````python
def test_api_request():
    url_incidencias = "https://api.status.salesforce.com/v1/incidents?instance=EU48&locale=es"
    url_cambios = "https://api.status.salesforce.com/v1/maintenances?instance=EU48"
    request_incidencias = requests.get(url_incidencias)
    request_cambios = requests.get(url_cambios)
    assert request_incidencias.status_code == 200
    assert request_cambios.status_code == 200
````