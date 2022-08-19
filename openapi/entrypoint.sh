#! /bin/bash

echo started
# apt update
if [ "$1" = "run_django" ]; then
  python manage.py makemigrations mailing --no-input
  python manage.py migrate --no-input
  exec gunicorn openapi.wsgi:application -b 0.0.0.0:8000 --reload
fi

if [ "$1" = "run_huey" ]; then
  python manage.py run_huey
fi
