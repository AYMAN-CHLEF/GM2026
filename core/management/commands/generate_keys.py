import uuid
from django.core.management.base import BaseCommand
from core.models import SerialKey

class Command(BaseCommand):
    help = 'توليد 100 رقم تسلسلي للمفاتيح'
    def handle(self, *args, **options):
        for _ in range(100):
            code = str(uuid.uuid4())[:8].upper()
            SerialKey.objects.get_or_create(serial_number=code)
        self.stdout.write(self.style.SUCCESS('تم توليد 100 مفتاح بنجاح!'))
