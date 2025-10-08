import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurana.settings')

try:
    django.setup()
    
    from django.core.management import execute_from_command_line
    from django.db import transaction
    
    print("Loading all data...")
    
    # Загружаем ВСЕ данные
    with transaction.atomic():
        execute_from_command_line(['manage.py', 'loaddata', 'all_data.json'])
    
    print("All data loaded successfully!")
    
except Exception as e:
    print(f"Error loading data: {e}")
    import traceback
    traceback.print_exc()