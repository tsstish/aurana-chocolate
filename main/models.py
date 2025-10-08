from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('milk', 'Молочный шоколад'),
        ('dark', 'Тёмный шоколад'),
        ('white', 'Белый шоколад'),
        ('gifts', 'Подарочные наборы'),
        ('special', 'Специальные предложения'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Категория")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение", blank=True)
    is_available = models.BooleanField(default=True, verbose_name="В наличии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"