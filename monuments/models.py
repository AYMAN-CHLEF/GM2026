from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.urls import reverse

class Monument(models.Model):
    # معلومات أساسية
    name_ar = models.CharField(max_length=200, verbose_name="اسم المعلم (عربي)")
    name_fr = models.CharField(max_length=200, verbose_name="اسم المعلم (فرنسي)")
    name_en = models.CharField(max_length=200, verbose_name="اسم المعلم (إنجليزي)")
    
    slug = models.SlugField(unique=True, help_text="المعرف الفريد لرابط الصفحة مثل: ksar-wakda-bechar")
    
    # الأوصاف متعددة اللغات
    description_ar = models.TextField(verbose_name="الوصف (عربي)")
    description_fr = models.TextField(verbose_name="الوصف (فرنسي)")
    description_en = models.TextField(verbose_name="الوصف (إنجليزي)")
    
    # مسارات الملفات في STATIC
    drone_video_path = models.CharField(max_length=255, blank=True, null=True, verbose_name="مسار فيديو الدرون في Static")
    image_path = models.CharField(max_length=255, blank=True, null=True, verbose_name="مسار صورة المعلم في Static")
    
    # الإحداثيات الجغرافية لتوجيه السائح (GPS)
    location_name = models.CharField(max_length=255, verbose_name="اسم الموقع / الولاية")
    google_maps_url = models.URLField(blank=True, null=True, verbose_name="رابط الخريطة (Google Maps)")

    # رمز الاستجابة السريعة الخاص بالمعلم (يخزن تلقائياً)
    qr_code = models.ImageField(upload_to='monuments/qrcodes/', blank=True, null=True, verbose_name="كود QR الميداني")

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # توليد كود QR تلقائياً إذا لم يكن موجوداً أو تم تغيير الـ slug
        if not self.qr_code and self.slug:
            # رابط صفحة المعلم (يمكنك استبدال الدومين لاحقاً أو استخدامه ديناميكياً)
            target_url = f"https://geo-memory.dz{reverse('monument_detail', args=[self.slug])}"
            qr_image = qrcode.make(target_url)
            buffer = BytesIO()
            qr_image.save(buffer, format="PNG")
            self.qr_code.save(f"qr_{self.slug}.png", File(buffer), save=False)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_ar
