#!/usr/bin/env bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Loading data..."
python load_data_final.py

echo "Creating superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'your-email@gmail.com', 'admin123')" | python manage.py shell || echo "Superuser already exists or error"

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Build completed!"