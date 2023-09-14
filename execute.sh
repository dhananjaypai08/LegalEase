#!/bin/bash

echo "Starting Your Project"
ls
#read NAME
. env/Scripts/activate
echo "Virutal environment Activated"
ls

DJANGO_SETTINGS_MODULE="core.settings"
DJANGO_WSGI_MODULE="core.wsgi"
echo "Config set"

python3 -m pip install --upgrade pip
echo "Pip upgraded"

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
#pip install -r requirements.txt
#echo "Requirements are installed" 

cd diversifynow
echo "Directory changed" 
ls

echo "Installing dependencies.."
pip install -r "requirements.txt"
echo "Requirements installed"

echo "Installing remaining dependencies"
pip install python-dotenv

#python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver
