from django.db import models
from django.utils.text import slugify

class Flag(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="اسم العلم")
    biography = models.TextField(verbose_name="السيرة الذاتية")
    birth_date = models.DateField(null=True, blank=True, verbose_name="تاريخ الميلاد")
    latitude = models.FloatField(verbose_name="خط العرض")
    longitude = models.FloatField(verbose_name="خط الطول")
    
    # تم تغيير الحقل هنا ليصبح ImageField بدلاً من CharField
    image = models.ImageField(
        upload_to='flags/', 
        null=True, 
        blank=True, 
        verbose_name="صورة العلم", 
        help_text="قم برفع صورة الشخصية هنا"
    )
    
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True, verbose_name="الرابط")
    
    # حقل التحكم في ظهور الشخصية
    is_ready = models.BooleanField(default=False, verbose_name="هل البيانات جاهزة للعرض؟")

    def save(self, *args, **kwargs):
        if not self.slug:
            # إضافة allow_unicode=True ضرورية جداً لدعم الأسماء باللغة العربية في الرابط
            self.slug = slugify(self.full_name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "علم/شخصية"
        verbose_name_plural = "الأعلام والسير"


class PathStep(models.Model):
    flag = models.ForeignKey(Flag, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=200, verbose_name="اسم المحطة")
    description = models.TextField(verbose_name="وصف الحدث")
    latitude = models.FloatField(verbose_name="خط العرض")
    longitude = models.FloatField(verbose_name="خط الطول")
    
    # هذا الحقل سليم وجاهز لرفع الصور
    image = models.ImageField(upload_to='steps/', null=True, blank=True, verbose_name="صورة المحطة")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتيب الظهور")

    class Meta:
        ordering = ['order']
        verbose_name = "محطة في المسار"
        verbose_name_plural = "محطات المسار"
        