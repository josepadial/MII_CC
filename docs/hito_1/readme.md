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

## JSON de ejemplo
En la carpeta DATA se tiene dos ficheros JSON con datos reales de las incidencias y cambios de
la instancia EU48 de Salesforce. Con la [US1](https://github.com/josepadial/MII_CC/issues/2) se va
a conseguir actualizar esos ficheros en cada ejecución de forma automática.
- [Incidencias](../../data/incidencias.json)
- [Cambios](../../data/cambios.json)

## Manual de ejecución