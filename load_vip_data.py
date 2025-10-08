import os
import django
import sys

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurana.settings')

try:
    django.setup()
    
    from django.core.management import execute_from_command_line
    from django.db import transaction
    
    print("Loading VIP clients data...")
    
    # Загружаем данные VIP-клиентов
    with transaction.atomic():
        execute_from_command_line(['manage.py', 'loaddata', 'vip_clients.json'])
    
    print("VIP clients data loaded successfully!")
    
except Exception as e:
    print(f"Error loading VIP data: {e}")