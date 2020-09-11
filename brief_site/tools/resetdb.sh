#!/bin/bash
set -e # fail on any error

echo -n "Do you really reset the database?[yes]"
read CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "Aborted"
    exit;
fi

PWD=`pwd`
cd `dirname $0`/..

# Re-create database
docker-compose exec mysql mysql -u passonate -ppassonate -e "DROP DATABASE passonate;"
echo "Drop Database";
docker-compose exec mysql mysql -u passonate -ppassonate -e "CREATE DATABASE passonate DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
echo "Create Database";

# Migrate
DJANGO_CONTAINER=`docker-compose ps | awk '/django/{ print $1; }'`
docker exec -it $DJANGO_CONTAINER python manage.py migrate

cd $PWD
