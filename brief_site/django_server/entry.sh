#!/bin/sh

# Compress sass and js
python manage.py collectstatic --noinput
# Migrate database
python manage.py makemigrations
python manage.py migrate
# Init server
uwsgi --ini django_server/uwsgi.ini
