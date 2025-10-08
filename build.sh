#!/usr/bin/env bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Loading data..."
python load_data_final.py

echo "Creating superuser..."
python create_superuser.py

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Build completed!"