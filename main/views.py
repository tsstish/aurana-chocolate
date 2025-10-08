from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
from .models import Product
from clients.models import VIPClient, Order, OrderItem

def get_cart_total(cart):
    """Подсчитывает общее количество товаров в корзине"""
    total = 0
    if cart:
        for item in cart.values():
            total += item['quantity']
    return total

def index(request):
    cart = request.session.get('cart', {})
    cart_total = get_cart_total(cart)
    
    # Проверяем, авторизован ли клиент
    client_id = request.session.get('client_id')
    client = None
    if client_id:
        try:
            client = VIPClient.objects.get(id=client_id)
        except VIPClient.DoesNotExist:
            pass
    
    # ДОБАВИЛ ЭТУ СТРОКУ - берем 8 товаров для главной страницы
    featured_products = Product.objects.filter(is_available=True)[:8]
    
    return render(request, 'index.html', {
        'cart_total': cart_total,
        'client': client,
        'featured_products': featured_products  # ДОБАВИЛ ЭТУ СТРОКУ
    })

def catalog(request):
    # Очищаем сообщение после показа
    cart_message = request.session.pop('cart_message', None)
    
    # Получаем все товары
    products = Product.objects.filter(is_available=True)
    
    # Получаем категории для фильтрации
    categories = Product.CATEGORY_CHOICES
    
    # Обрабатываем фильтр по категории
    category_filter = request.GET.get('category', '')
    if category_filter:
        products = products.filter(category=category_filter)
    
    cart = request.session.get('cart', {})
    cart_total = get_cart_total(cart)
    
    # Проверяем авторизацию
    client_id = request.session.get('client_id')
    client = None
    if client_id:
        try:
            client = VIPClient.objects.get(id=client_id)
        except VIPClient.DoesNotExist:
            pass
    
    return render(request, 'catalog.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_filter,
        'cart_message': cart_message,
        'cart_total': cart_total,
        'client': client
    })

def add_to_cart(request, product_id):
    """Добавление товара в корзину"""
    product = get_object_or_404(Product, id=product_id)
    
    # Получаем или создаем корзину в сессии
    cart = request.session.get('cart', {})
    
    # Добавляем товар в корзину
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:  
        cart[str(product_id)] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': 1,
            'image': product.image.name if product.image else None  # Сохраняем путь к изображению
        }
    
    request.session['cart'] = cart
    # Сохраняем сообщение об успехе
    request.session['cart_message'] = f"{product.name} добавлен в корзину!"
    return redirect('catalog')
    
    request.session['cart'] = cart
    # Сохраняем сообщение об успехе
    request.session['cart_message'] = f"{product.name} добавлен в корзину!"
    return redirect('catalog')

def cart_view(request):
    """Страница корзины"""
    cart = request.session.get('cart', {})
    
    # Подсчет общей суммы
    total = 0
    for item in cart.values():
        total += float(item['price']) * item['quantity']

    # Расчет бонусов (5% от суммы)
    bonus_points = int(total * 0.05)
    
    cart_total = get_cart_total(cart)
    
    # Проверяем авторизацию
    client_id = request.session.get('client_id')
    client = None
    if client_id:
        try:
            client = VIPClient.objects.get(id=client_id)
        except VIPClient.DoesNotExist:
            pass
    
    return render(request, 'cart.html', {
        'cart': cart,
        'total': total,
        'cart_total': cart_total,
        'client': client,
        'bonus_points': bonus_points
    })

def remove_from_cart(request, product_id):
    """Удаление товара из корзины"""
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    
    return redirect('cart_view')

def checkout(request):
    """Страница оформления заказа"""
    cart = request.session.get('cart', {})
    
    if not cart:
        return redirect('cart_view')
    
    # Подсчет общей суммы
    total = 0
    for item in cart.values():
        total += float(item['price']) * item['quantity']
    
    # Расчет бонусов (5% от суммы)
    bonus_points = int(total * 0.05)
    
    cart_total = get_cart_total(cart)
    
    return render(request, 'checkout.html', {
        'cart': cart,
        'total': total,
        'cart_total': cart_total,
        'bonus_points': bonus_points  
    })

def create_order(request):
    """Создание заказа"""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        
        if not cart:
            return redirect('cart_view')
        
        try:
            # Создаем клиента на основе данных формы
            client_name = request.POST.get('name', 'Гость')
            client_phone = request.POST.get('phone', '')
            client_email = request.POST.get('email', '')
            client_password = request.POST.get('password', '')
            client_address = request.POST.get('address', '')
            
            if not client_phone:
                return render(request, 'checkout.html', {
                    'cart': cart,
                    'total': sum(float(item['price']) * item['quantity'] for item in cart.values()),
                    'cart_total': get_cart_total(cart),
                    'error_message': 'Пожалуйста, укажите телефон.'
                })
            
            # Ищем или создаем клиента
            client = VIPClient.objects.filter(phone=client_phone).first()
            
            if not client:
                # Создаем нового клиента (нашедшего сайт в интернете)
                client = VIPClient.objects.create(
                    phone=client_phone,
                    name=client_name,
                    email=client_email,
                    is_registered=True
                )
                
                # Устанавливаем пароль, если указан
                if client_password:
                    client.set_password(client_password)
                    client.save()
                
                print(f"Создан новый клиент: {client.name} ({client.phone})")
            else:
                # Обновляем данные существующего клиента
                client.name = client_name
                client.email = client_email
                client.is_registered = True
                
                # Обновляем пароль, если указан новый
                if client_password:
                    client.set_password(client_password)
                
                client.save()
                print(f"Обновлен существующий клиент: {client.name} ({client.phone})")
            
            # Создаем заказ
            order = Order.objects.create(
                client=client,
                total_amount=0,  # Рассчитаем ниже
                status='new'
            )
            
            # Добавляем товары в заказ
            total_amount = 0
            for product_id, item in cart.items():
                product = Product.objects.get(id=product_id)
                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=item['price']
                )
                total_amount += float(item['price']) * item['quantity']
            
            # Обновляем общую сумму заказа
            order.total_amount = total_amount
            
            # Начисляем бонусы (5% от суммы заказа)
            bonus_points = int(total_amount * 0.05)
            client.bonus_points += bonus_points
            order.bonus_earned = bonus_points
            
            order.save()
            client.save()
            
            # Авторизуем клиента
            request.session['client_id'] = str(client.id)
            
            # Очищаем корзину
            request.session['cart'] = {}
            
            # Сохраняем ID заказа для показа на странице успеха
            request.session['last_order_id'] = str(order.id)
            
            print(f"Создан заказ #{order.id} для клиента {client.name}. Начислено бонусов: {bonus_points}")
            
            # Перенаправляем на страницу успеха
            return redirect('order_success')
            
        except Exception as e:
            print(f"Ошибка создания заказа: {e}")
            # В случае ошибки показываем сообщение
            return render(request, 'checkout.html', {
                'cart': cart,
                'total': sum(float(item['price']) * item['quantity'] for item in cart.values()),
                'cart_total': get_cart_total(cart),
                'error_message': 'Произошла ошибка при оформлении заказа. Попробуйте еще раз.'
            })
    
    return redirect('checkout')

def order_success(request):
    """Страница успешного оформления заказа"""
    order_id = request.session.get('last_order_id')
    client_id = request.session.get('client_id')
    
    order = None
    client = None
    
    if order_id:
        try:
            order = Order.objects.get(id=order_id)
            client = order.client
        except Order.DoesNotExist:
            pass
    
    if client_id and not client:
        try:
            client = VIPClient.objects.get(id=client_id)
        except VIPClient.DoesNotExist:
            pass
    
    cart_total = get_cart_total(request.session.get('cart', {}))
    
    return render(request, 'order_success.html', {
        'order': order,
        'client': client,
        'cart_total': cart_total
    })

def login_view(request):
    """Страница входа в личный кабинет"""
    if request.method == 'POST':
        phone = request.POST.get('phone')
        
        if phone:
            # Ищем клиента по телефону (временно без пароля)
            client = VIPClient.objects.filter(phone=phone, is_registered=True).first()
            
            if client:
                # Успешный вход
                request.session['client_id'] = str(client.id)
                return redirect('client_profile')
            else:
                # Неверные данные
                return render(request, 'login.html', {
                    'error_message': 'Клиент с таким телефоном не найден',
                    'cart_total': get_cart_total(request.session.get('cart', {}))
                })
    
    cart_total = get_cart_total(request.session.get('cart', {}))
    return render(request, 'login.html', {'cart_total': cart_total})    

def logout_view(request):
    """Выход из личного кабинета"""
    if 'client_id' in request.session:
        del request.session['client_id']
    return redirect('index')

def client_profile(request):
    """Личный кабинет клиента"""
    client_id = request.session.get('client_id')
    
    if not client_id:
        return redirect('login_view')
    
    try:
        client = VIPClient.objects.get(id=client_id)
    except VIPClient.DoesNotExist:
        # Если клиент не найден, разлогиниваем
        if 'client_id' in request.session:
            del request.session['client_id']
        return redirect('login_view')
    
    cart_total = get_cart_total(request.session.get('cart', {}))
    
    return render(request, 'clients/vip_profile.html', {
        'client': client,
        'cart_total': cart_total
    })