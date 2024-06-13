#!/bin/sh

source .env

echo ">>>> Waiting for MySQL... <<<<"
while ! nc -z $MYSQL_HOST $MYSQL_PORT
do
    echo echo ">>>> Waiting ... <<<<"
    sleep 1
done
echo ">>>> MySQL started <<<"


echo ">>>> Ensure superuser <<<<"
python manage.py ensure_superuser


echo ">>>> Updating database <<<<"
python manage.py migrate


echo ">>>> Runing server <<<<"
python manage.py runserver 0.0.0.0:8000