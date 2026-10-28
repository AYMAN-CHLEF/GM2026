from django.db import models
from django.contrib.auth.models import User

class HeritageAsset(models.Model):
    """نموذج لتخزين بيانات المواقع التراثية"""
    name = models.CharField(max_length=255, verbose_name="اسم الموقع")
    description = models.TextField(verbose_name="الوصف التراثي")
    latitude = models.FloatField(verbose_name="خط العرض", null=True, blank=True)
    longitude = models.FloatField(verbose_name="خط الطول", null=True, blank=True)
    category = models.CharField(max_length=100, verbose_name="نوع التراث")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Location(models.Model):
    """نموذج المواقع الجغرافية العام"""
    name = models.CharField(max_length=255, verbose_name="اسم المكان")
    coordinates = models.JSONField(default=dict, verbose_name="الإحداثيات") 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TouristService(models.Model):
    """نموذج الخدمات السياحية، الإقامات، والحرفيين التراثيين مع الصور والأسعار والمدة"""
    CATEGORY_CHOICES = [
        ('restaurant', 'مطعم ووجبات تقليدية'),
        ('hotel', 'فندق / منزل للكراء والمبيت'),
        ('guide', 'مرشد سياحي محلي'),
        ('artisan', 'حرفي / بائع تحف وهدايا تذكارية'),
    ]

    name = models.CharField(max_length=255, verbose_name="اسم المزود / المكان / الحرفي")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="التصنيف")
    description = models.TextField(blank=True, verbose_name="وصف الخدمة أو المنتجات والتحف المعروضة")
    
    # الإحداثيات الجغرافية
    latitude = models.FloatField(verbose_name="خط العرض (Latitude)")
    longitude = models.FloatField(verbose_name="خط الطول (Longitude)")
    
    # المعلومات الشخصية والاتصال
    contact_person = models.CharField(max_length=150, blank=True, verbose_name="اسم المسؤول أو الحرفي")
    phone = models.CharField(max_length=30, blank=True, verbose_name="رقم الهاتف / واتساب")
    
    # الأسعار والوسائط (صور، تحف، سعر الليلة أو المنتج)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="السعر (لكل ليلة / أو سعر المنتج والخدمة)")
    image = models.ImageField(upload_to='services_images/', null=True, blank=True, verbose_name="صورة المكان أو المنتج / التحفة")
    
    # خيارات المبيت والمدة (أيام، أسابيع، أشهر)
    supports_duration_booking = models.BooleanField(default=False, verbose_name="يدعم تحديد مدة الإقامة (أيام/أسابيع/أشهر)")
    
    # الربط بالمعلم التراثي القريب
    related_asset = models.ForeignKey(
        HeritageAsset, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="nearby_services",
        verbose_name="المعلم التراثي القريب"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    def __str__(self):
        return f"[{self.get_category_display()}] - {self.name}"

class BookingRequest(models.Model):
    """نموذج طلبات حجز المبيت (أيام، أسابيع، أشهر) أو التواصل"""
    service = models.ForeignKey(TouristService, on_delete=models.CASCADE, related_name='bookings', verbose_name="الخدمة أو مكان المبيت")
    visitor_name = models.CharField(max_length=150, verbose_name="اسم السائح / الزائر")
    phone = models.CharField(max_length=30, verbose_name="رقم الهاتف للتواصل")
    
    duration_type = models.CharField(
        max_length=20, 
        choices=[('days', 'أيام'), ('weeks', 'أسابيع'), ('months', 'أشهر')],
        default='days',
        verbose_name="نوع وحدة المدة"
    )
    duration_value = models.IntegerField(verbose_name="العدد (مثال: 3 أيام، أسبوعين...)")
    notes = models.TextField(blank=True, verbose_name="ملاحظات إضافية للطلب")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")

    def __str__(self):
        return f"طلب حجز لـ {self.service.name} بواسطة {self.visitor_name}"

class VisitorFlow(models.Model):
    """نموذج لتتبع تدفق الزوار"""
    asset = models.ForeignKey(HeritageAsset, on_delete=models.CASCADE, related_name="visitor_data")
    timestamp = models.DateTimeField(auto_now_add=True)
    visitor_count = models.IntegerField(verbose_name="عدد الزوار")
    
    def __str__(self):
        return f"{self.asset.name} - {self.timestamp}"

class FieldReport(models.Model):
    asset = models.ForeignKey(HeritageAsset, on_delete=models.CASCADE, related_name='field_reports', verbose_name="الأصل التراثي")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="المستخدم الميداني")
    latitude = models.FloatField(verbose_name="خط العرض (Latitude)")
    longitude = models.FloatField(verbose_name="خط الطول (Longitude)")
    topographic_status = models.CharField(max_length=255, verbose_name="تحديث الحالة الطبوغرافية")
    condition_rating = models.IntegerField(verbose_name="تقييم الحالة (من 1 إلى 5)")
    field_image = models.ImageField(upload_to='field_reports/', null=True, blank=True, verbose_name="صورة الميدان")
    notes = models.TextField(blank=True, verbose_name="ملاحظات الميدان التوثيقية")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإرسال")

    def __str__(self):
        return f"تقرير ميداني #{self.id} - {self.asset.name if self.asset else 'معلم غير محدد'}"