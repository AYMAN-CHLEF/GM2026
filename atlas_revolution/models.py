from django.db import models

class HistoricalEvent(models.Model):
    TYPE_CHOICES = [('battle', 'معركة'), ('center', 'مركز استراتيجي')]
    
    name = models.CharField(max_length=200, verbose_name="الاسم")
    event_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="النوع")
    wilaya = models.CharField(max_length=100, verbose_name="الولاية")
    date = models.DateField(verbose_name="التاريخ")
    leader = models.CharField(max_length=100, verbose_name="القائد")
    description = models.TextField(verbose_name="الوصف")
    outcome = models.TextField(verbose_name="النتيجة/الأهمية")
    lat = models.FloatField(verbose_name="خط العرض")
    lng = models.FloatField(verbose_name="خط الطول")

    def __str__(self):
        return self.name