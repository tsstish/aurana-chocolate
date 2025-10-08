from django.shortcuts import render, get_object_or_404, redirect
from .models import VIPClient

def vip_register(request, client_id):
    # Находим клиента по ID из QR-кода
    client = get_object_or_404(VIPClient, id=client_id)
    
    # Если клиент УЖЕ зарегистрирован - показываем приветствие
    if client.is_registered:
        return render(request, 'clients/welcome_back.html', {'client': client})
    
    # Если форма отправлена - сохраняем данные и начисляем бонусы
    if request.method == 'POST':
        client.name = request.POST.get('name')
        client.phone = request.POST.get('phone')
        client.email = request.POST.get('email')
        client.telegram = request.POST.get('telegram')
        client.birth_date = request.POST.get('birth_date')
        
        # Устанавливаем пароль, если указан
        password = request.POST.get('password')
        if password:
            client.set_password(password)
        
        client.is_registered = True
        # Начисляем приветственные бонусы
        client.bonus_points = 100  # 100 баллов за регистрацию
        client.save()
        
        # Авторизуем клиента
        request.session['client_id'] = str(client.id)
        
        return render(request, 'clients/vip_profile.html', {'client': client})
    
    # Показываем форму регистрации
    return render(request, 'clients/vip_register.html', {'client': client})