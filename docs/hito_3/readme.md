# Hito 3: Creación de un contenedor para pruebas
Índice:
<!-- TOC -->
* [Elección de la imagen para el contenedor](#eleccin-de-la-imagen-para-el-contenedor)
  * [Hardware](#hardware)
  * [Seguridad](#seguridad)
  * [Rendimiento](#rendimiento)
  * [Soporte](#soporte)
  * [Pruebas de tiempo](#pruebas-de-tiempo)
    * [Alpine Linux](#alpine-linux)
    * [Ubuntu Linux](#ubuntu-linux)
  * [Pruebas de tamaño](#pruebas-de-tamao)
    * [Imagen base](#imagen-base)
    * [Imagen Wordpress](#imagen-wordpress)
  * [Conclusion](#conclusion)
<!-- TOC -->

## Elección de la imagen para el contenedor
Se va a realizar una estudio previo para decidir si se va a utilizar Alpine Linux o si se va a utiliz
utilizar Ubuntu Linux. En este estudio todas las pruebas se han realizado sin GUI.

### Hardware
Alpine Linux requiere al menos 100 MB de RAM y entre 0 y 700 MB de espacio de almacenamiento. En comparación,
Ubuntu requiere al menos 512 MB de RAM y al menos 1 GB de almacenamiento. La necesidad mínima de hardware de 
Alpine Linux lo hace ideal para ejecutarse en dispositivos pequeños.

### Seguridad
Dado que Alpine Linux es pequeño, tiene una superficie de ataque mínima. Menos código conduce a menos errores
y vulnerabilidades, pero no lo hace más seguro. Ubuntu también ha implementado PIE por defecto a partir de 17.10 
para todas las arquitecturas en el archivo de Ubuntu. Además, Ubuntu tiene habilitada la protección de pila en el Kernel.
Adicionalmente, Ubuntu se incluye con un conjunto completo de bibliotecas C de GNU y herramientas estándar.

### Rendimiento
Alpine Linux requiere menos código. Una base de código más pequeña permite la creación, empuje y extracción de imágenes 
más rápidas. Los tiempos de inicio se reducen y el escaneo no lleva mucho tiempo.

### Soporte
Alpine Linux lanza una nueva versión principal cada mayo y noviembre. El repositorio principal suele recibir soporte 
durante dos años. Por el contrario, el repositorio de la comunidad es compatible hasta la próxima versión estable.

Ubuntu se lanza cada seis meses. Y una versión de soporte a largo plazo (LTS) se lanza en abril cada dos años. 
Las versiones LTS son de "nivel empresarial" y tienen soporte durante cinco años.

### Pruebas de tiempo
Se va a realizar pruebas con la imagen de Wordpress.
#### Alpine Linux
Resultado: Inicio promedio 0.49 segundos.
````shell
root@jpadial:/home/alpine# time docker run --rm -d wordpress
92a19eed723cdb6ef073fd58b0fed45ba02320986c8d2dc4b964bf21c89b255c
real 0m 0.47s
user 0m 0.02s
sys 0m 0.02s

root@jpadial:/home/alpine# time docker run --rm -d wordpress
26c80fb4ad321ab79fae5148fdab2406b288e0efdc1af211bda680836d5563e9
real 0m 0.51s
user 0m 0.02s
sys 0m 0.01s

root@jpadial:/home/alpine# time docker run --rm -d wordpress
e4bfc492ba28c77c0b18c4ece1bd27201e00f0e2193f133d5a251f39566f835c
real 0m 0.49s
user 0m 0.02s
sys 0m 0.02s
````

#### Ubuntu Linux
Resultado: Inicio promedio 0.587 segundos.
````shell
root@jpadial:/home/ubuntu# time docker run --rm -d wordpress
1709d25e62778342503175a65b29fe625d022565587763f5c82d3efdddf4fcf8
real 0m0.507s
user 0m0.028s
sys 0m0.020s

root@jpadial:/home/ubuntu# time docker run --rm -d wordpress
b46cbff58939db2c3b9eeff6e565b6e943db218463b30df0f1681405b1ab3a76
real 0m0.703s
user 0m0.022s
sys 0m0.026s

root@jpadial:/home/ubuntu# time docker run --rm -d wordpress
6aa712fb5b333b23b77ed056354d06dc5ace92d804ef6032f20bb36511244174
real 0m0.551s
user 0m0.028s
sys 0m0.019s
````

### Pruebas de tamaño
#### Imagen base
La imagen de Alpine Linux es de 5,61 MB, que es considerablemente más pequeña que Debian o Ubuntu.
````shell
root@jpadial:/home/alpine# docker image ls

REPOSITORY TAG IMAGE ID CREATED SIZE
alpine latest 6dbb9cc54074 2 days ago 5.61MB
debian latest 0d587dfbc4f4 7 days ago 114MB
ubuntu latest 26b77e58432b 2 weeks ago 72.9MB
````

#### Imagen Wordpress
Resultado: La versión de imagen Alpine Linux deWordPresses 351 MB más pequeña.
````shell
root@jpadial:/home/ubuntu # docker image ls

REPOSITORY TAG IMAGE ID CREATED SIZE
wordpress php8.0-fpm-alpine 6b5f99037a83 38 hours ago 199MB
wordpress latest c01290f258b3 38 hours ago 550MB
````

### Conclusion
Es mejor usar Alpine Linux si tiene restricciones de procesamiento, memoria, red o almacenamiento. Afortunadamente, 
el almacenamiento y las redes son asequibles en la mayoría de los casos. Alpine Linux también es un claro ganador 
si le preocupa la superficie de ataque. En nuestro caso vamos a darle más importancia al soporte comercial,
soporte de paquetes y la complejidad del sistema y quitarle importancia a las restrinciones hardware. Con lo cual
se va a utilizar UBUNTU.

## Dockerfile y docker-compose.yaml
Se va a generar un Dockerfile para la creación del docker con las funcionalidades del código principal. Pero como
se depende de dos dockers más (MySQL y MailDev) se va a crear un docker-compose para automatizar el despliegue de todos los requisitos.

El Dockerfile se puede encontrar en el siguiente [enlace](../../Dockerfile)

El docker-compose.yaml se puede encontrar en el siguiente [enlace](../../docker-compose.yaml)

## Docker Hub
Para que se suba automáticamente a Docker Hub todas las actualizaciones que hagamos sobre el Dockerfile se va a utilizar
los webhooks de GitHub.