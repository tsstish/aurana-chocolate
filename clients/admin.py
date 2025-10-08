from django.contrib import admin
from .models import VIPClient

@admin.register(VIPClient)
class VIPClientAdmin(admin.ModelAdmin):  
    list_display = ['name', 'phone', 'email', 'bonus_points', 'registration_date']
    search_fields = ['name', 'phone', 'email']

from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['client__name', 'client__phone']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']