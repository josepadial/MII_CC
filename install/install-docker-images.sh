#!/bin/bash
docker pull mysql:latest
mysqlpass="1234"
docker run --name mysql -e MYSQL_ROOT_PASSWORD=$mysqlpass -p 3306:3306 -d mysql
docker pull phpmyadmin/phpmyadmin:latest
docker run --name phpmyadmin -d --link mysql:db -p 8081:80 phpmyadmin/phpmyadmin
docker-compose up -d
docker update --restart always $(docker ps -q)