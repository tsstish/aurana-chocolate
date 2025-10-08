from django.urls import path
from . import views

urlpatterns = [
    path('vip/register/<uuid:client_id>/', views.vip_register, name='vip_register'),
]