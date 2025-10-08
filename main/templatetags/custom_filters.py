from django import template

register = template.Library()

@register.filter
def total_quantity(cart):
    """Подсчитывает общее количество товаров в корзине"""
    total = 0
    for item in cart.values():
        total += item['quantity']
    return total

@register.filter
def get_item(dictionary, key):
    """Получает значение из словаря по ключу"""
    return dictionary.get(str(key))