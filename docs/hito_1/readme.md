# Hito 1: Concretando y planificando el proyecto
Índice:
<!-- TOC -->
* [User Stories](#user-stories)
* [cc.yaml](#ccyaml)
* [Código](#cdigo)
* [JSON de ejemplo](#json-de-ejemplo)
* [Manual de ejecución](#manual-de-ejecucin)
<!-- TOC -->

## User Stories
- [[US1] Como usuario del sistema, quiero que ALERT-ME guarde todas las alertas obtenidas desde la API (sin filtrado) en un JSON](https://github.com/josepadial/MII_CC/issues/2)
- [[US2] Como usuario del sistema, quiero que ALERT-ME guarde todas las alertas obtenidas desde la API (sin filtrado) en una BBDD](https://github.com/josepadial/MII_CC/issues/3)
- [[US3] Como usuario del sistema, quiero que ALERT-ME genere un correo con cada alerta recibida](https://github.com/josepadial/MII_CC/issues/4)
- [[US4] Como usuario del sistema, quiero poder realizar un consulta filtrando alertas por diferentes filtros](https://github.com/josepadial/MII_CC/issues/5)

## cc.yaml
Para crédito adicional, la clase o clases que se hayan comenzado a implementar (sin código)
correspondientes a las historias de usuario. Para indicar qué clases son estas, se usará un
fichero cc.yaml, y, en la clave entidad, el fichero donde se haya programado la entidad en
forma de una clase, módulo o paquete que es el objeto de este hito, con el camino correcto.

Enlace al fichero [cc.yaml](../../cc.yaml)

## Código
- Ficheros principales:
  - Clase principal [main.py](../../src/main.py).
  - Variables de entorno [envfile.env](../../src/envfile.env).
  - Requirements [requirements.txt](../../src/requirements.txt).
  - Set up del entorno virtual de Python [venv-setup.sh](../../install/venv-setup.sh).
- Carpetas principales:
  - Para almacenar toda la información [data](../../data).
  - Código [source](../../src).
  - Librería para el proyecto [vendor](../../src/vendor).

## JSON de ejemplo
En la carpeta DATA se tiene dos ficheros JSON con datos reales de las incidencias y cambios de
la instancia EU48 de Salesforce. Con la [US1](https://github.com/josepadial/MII_CC/issues/2) se va
a conseguir actualizar esos ficheros en cada ejecución de forma automática.
- [Incidencias](../../data/incidencias.json)
- [Cambios](../../data/cambios.json)

## Manual de ejecución
Para ejecutar el proyecto previamente debemos de tener Python 3.8 instalado en nuestro sistema.
Después, procedemos a ejecutar el fichero [venv-setup.sh](../../install/venv-setup.sh); el cual procederá
a crearnos un entorno virtual de Python exclusivo para este proyecto en cuál ya estarán instalados
todos los requirments y librerías. Una vez configurado seleccionamos el intérprete de Python y 
ejecutamos el fichero [main.py](../../src/main.py). 

Los pasos anteriores nos van a crear un servidor Flsk que escucha en "localhost:8080". En el fichero
[main.py](../../src/main.py) se pueden encontrar las diferentes acciones que se han implementado.
Para este hito 1 solo se ha implementado un POST, obtener los datos de la API y guardarlos en un JSON.
Al realizar un POST a "http://127.0.0.1:8080/update_data" podemos obtener:
- "SUCCESS": en el caso de que no haya habido ningún fallo de ejecución.
- "FAILED": en el caso de que suceda cuando si hay un fallo de ejecución, el cual viene acompañado de un mensaje de error.