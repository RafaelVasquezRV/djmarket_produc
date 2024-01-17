#!/bin/bash

NAME="djmarket_produc" # Nombre de la aplicación
DJANGODIR=/home/croanca/production/djmarket_produc/ #Ruta de la carpeta de la aplicación
SOCKFILE=/home/croanca/production/run/gunicorn.sock #Ruta donde se creará el archivo de socket unix para comunicarnos
LOGDIR=${DJANGODIR}logs/gunicorn.log #Carpeta donde estara los logs del gunicorn
USER=croanca #Usuario con el que vamos a correr el sitio web
GROUP=croanca #Grupo con el que vamos a correr el sitio web
NUM_WORKERS=3 #Número de procesos que se van a utilizar para correr la aplicación
DJANGO_SETTINGS_MODULE=setting_djmarket.settings.prod #Ruta de los settings
DJANGO_WSGI_MODULE=setting_djmarket.wsgi #Nombre del módulo wsgi

# Activar el entorno virtual
cd $DJANGODIR
source ../env/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Crear la carpeta run si no existe para guardar el socket linux
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Iniciar la aplicación django por medio de gunicorn
exec ../env/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--user=$USER --group=$GROUP \
--bind=unix:$SOCKFILE \
--log-level=debug \
--log-file=-
