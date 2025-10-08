import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurana.settings')

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    # Удаляем старого если есть
    User.objects.filter(username='admin').delete()
    
    # Создаем нового
    user = User.objects.create_superuser(
        username='admin',
        email='admin@aurana.ru', 
        password='admin123'
    )
    print("✅ Superuser created successfully!")
    print("Username: admin")
    print("Password: admin123")
    
except Exception as e:
    print(f"Error: {e}")
    # Пробуем другой username
    try:
        user = User.objects.create_superuser(
            username='auranaadmin',
            email='admin@aurana.ru',
            password='admin123'
        )
        print("✅ Superuser created with username: auranaadmin")
    except:
        print("❌ Could not create superuser")