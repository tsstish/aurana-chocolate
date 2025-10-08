from django.db import models
import uuid
from django.contrib.auth.hashers import make_password, check_password

class VIPClient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Поля, которые заполняет клиент при регистрации
    name = models.CharField(max_length=100, verbose_name="Имя", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)
    telegram = models.CharField(max_length=50, verbose_name="Telegram", blank=True)
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    
    # Пароль для входа в ЛК
    password = models.CharField(max_length=128, verbose_name="Пароль", blank=True)
    
    # Служебные поля
    is_registered = models.BooleanField(default=False, verbose_name="Зарегистрирован")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    bonus_points = models.IntegerField(default=0, verbose_name="Бонусные баллы")
    
    def __str__(self):
        if self.is_registered:
            return f"{self.name} ({self.phone})"
        else:
            return f"Незарегистрированная карта ({self.id})"
    
    def set_password(self, raw_password):
        """Установка хешированного пароля"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Проверка пароля"""
        return check_password(raw_password, self.password)
    
    def get_qr_code_url(self):
        return f"/vip/register/{self.id}/"

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    ]
    
    client = models.ForeignKey(VIPClient, on_delete=models.CASCADE, verbose_name="Клиент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма", default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    bonus_earned = models.IntegerField(default=0, verbose_name="Начислено бонусов")
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.client.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey('main.Product', on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.IntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"