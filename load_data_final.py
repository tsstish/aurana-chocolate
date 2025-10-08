import os
import django
import sys
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurana.settings')

try:
    django.setup()
    
    from django.core.management import execute_from_command_line
    from django.db import transaction
    
    print("=== STARTING DATA LOAD ===")
    
    # Загружаем пользователей
    if os.path.exists('users.json') and os.path.getsize('users.json') > 100:
        print("Loading users...")
        execute_from_command_line(['manage.py', 'loaddata', 'users.json'])
        print("✓ Users loaded")
    else:
        print("✗ Users file missing or too small")
    
    # Загружаем VIP-клиентов
    if os.path.exists('vip_clients.json') and os.path.getsize('vip_clients.json') > 1000:
        print("Loading VIP clients...")
        execute_from_command_line(['manage.py', 'loaddata', 'vip_clients.json'])
        print("✓ VIP clients loaded")
    else:
        print("✗ VIP clients file missing or too small")
    
    # Пробуем загрузить товары если файл нормальный
    if os.path.exists('products.json') and os.path.getsize('products.json') > 1000:
        print("Loading products...")
        execute_from_command_line(['manage.py', 'loaddata', 'products.json'])
        print("✓ Products loaded")
    else:
        print("✗ Products file missing or too small - will add manually")
    
    print("=== DATA LOAD COMPLETED ===")
    
except Exception as e:
    print(f"!!! ERROR: {e}")
    import traceback
    traceback.print_exc()