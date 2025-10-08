from django.core.management.base import BaseCommand
from clients.models import VIPClient
import uuid

class Command(BaseCommand):
    help = 'Генерирует указанное количество VIP-карт для печати на визитках'
    
    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Количество VIP-карт для генерации')
    
    def handle(self, *args, **options):
        count = options['count']
        
        for i in range(count):
            client = VIPClient.objects.create()
            self.stdout.write(
                self.style.SUCCESS(f'Карта {i+1}: {client.id} - http://127.0.0.1:8000/vip/register/{client.id}/')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Успешно создано {count} VIP-карт!')
        )