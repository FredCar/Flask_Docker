FROM mariadb:latest

ENV MYSQL_ROOT_PASSWORD root
ENV MYSQL_DATABASE docker_test

ADD script.sql docker-entrypoint-initdb.d
