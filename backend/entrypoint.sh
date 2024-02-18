#!/bin/sh

sed -ri 's/\r\n|\r/\n/g' entrypoint.sh

python manage.py makemigrations
until python manage.py migrate --noinput
do
    echo "Waiting for db to be ready..."
    sleep 2
done
python manage.py loaddata data.json
python manage.py collectstatic --no-input

gunicorn Tiskistore.wsgi:application --bind 0.0.0.0:8000