import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# الحصول على نموذج المستخدم النشط في بيئة دجانغو
User = get_user_model()


# 1. ملف التعريف الشخصي للمستخدم
class UserProfile(models.Model):
    USER_TYPES = [
        ('student', 'طالب تعليمي'),
        ('gis_trainee', 'متدرب نظم معلومات جغرافية GIS'),
    ]
    
    CYCLE_CHOICES = [
        ('primary', 'التعليم الابتدائي'),
        ('middle', 'التعليم المتوسط'),
        ('secondary', 'التعليم الثانوي'),
        ('university', 'التعليم الجامعي'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='userprofile',
        verbose_name="المستخدم المرتبط"
    )
    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPES, 
        default='student',
        db_index=True,
        verbose_name="نوع الحساب"
    )
    educational_cycle = models.CharField(
        max_length=50, 
        choices=CYCLE_CHOICES, 
        blank=True, 
        null=True,
        verbose_name="الطور التعليمي"
    )
    academic_year = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name="السنة الدراسية",
        help_text="مثال: السنة الأولى ثانوي، السنة الثالثة جامعي..."
    )
    # الاحتفاظ بالحقل القديم توافقياً مع أي استدعاءات سابقة
    level = models.CharField(
        max_length=20, 
        choices=[('primary', 'المرحلة الابتدائية'), ('middle', 'المرحلة المتوسطة'), ('high', 'المرحلة الثانوية'), ('university', 'المرحلة الجامعية / أكاديمي')], 
        default='primary',
        verbose_name="المستوى الدراسي (قديم)"
    ) 
    points = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="النقاط المكتسبة"
    )
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True, 
        verbose_name="رقم الهاتف"
    )
    profile_image = models.ImageField(
        upload_to='profiles/avatars/', 
        null=True, 
        blank=True, 
        verbose_name="الصورة الشخصية"
    )
    bio = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="نبذة شخصية"
    )
    
    first_name_ar = models.CharField(max_length=50, blank=True, null=True, verbose_name="الاسم الأول (بالعربية)")
    last_name_ar = models.CharField(max_length=50, blank=True, null=True, verbose_name="اللقب (بالعربية)")
    first_name_en = models.CharField(max_length=50, blank=True, null=True, verbose_name="الاسم الأول (بالإنجليزية)")
    last_name_en = models.CharField(max_length=50, blank=True, null=True, verbose_name="اللقب (بالإنجليزية)")
    
    is_active_subscription = models.BooleanField(default=False, verbose_name="هل الاشتراك نشط؟")
    subscription_end_date = models.DateTimeField(null=True, blank=True, verbose_name="تاريخ انتهاء الاشتراك")
    
    class Meta:
        verbose_name = "ملف تعريف المستخدم"
        verbose_name_plural = "ملفات تعريف المستخدمين"

    def __str__(self):
        return f"ملف: {self.user.get_full_name() or self.user.username}"


# إشارة آمنة لإنشاء ملف التعريف تلقائياً وتفادي أخطاء تكرار السجلات
@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    

# 2. نموذج الدورات التدريبية والتعليمية
class Course(models.Model):
    COURSE_TYPE_CHOICES = [
        ('coding', 'برمجة'),
        ('specialized', 'نظم معلومات جغرافية GIS'),
    ]
    title = models.CharField(max_length=200, verbose_name="عنوان الدورة")
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES, default='specialized', db_index=True, verbose_name="نوع الدورة")
    description = models.TextField(verbose_name="وصف الدورة الشامل", default="")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        validators=[MinValueValidator(0.00)],
        verbose_name="سعر الدورة (دج)"
    )
    is_free = models.BooleanField(
        default=False, 
        db_index=True,
        verbose_name="هل الدورة مجانية؟"
    )
    image = models.ImageField(
        upload_to='courses/covers/', 
        null=True, 
        blank=True, 
        verbose_name="غلاف الدورة"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "الدورة التدريبية"
        verbose_name_plural = "الدورات التدريبية"
        ordering = ['-created_at']

    @property
    def is_locked(self):
        """تحديد ما إذا كانت الدورة تتطلب اشتراكاً مدفوعاً"""
        return not self.is_free

    def __str__(self):
        return self.title

    def is_purchased_by(self, user):
        """التحقق السريع مما إذا كان المستخدم يمتلك حق الوصول لهذه الدورة"""
        if not user.is_authenticated:
            return False
        if self.is_free:
            return True
        return self.enrollments.filter(user=user).exists()


# 3. نموذج الاشتراكات الفعلية للمستخدمين في الدورات
class UserCourse(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='purchased_courses',
        verbose_name="المشترك"
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='enrollments',
        verbose_name="الدورة المسجل بها"
    )
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الاشتراك")

    class Meta:
        verbose_name = "اشتراك مستخدم"
        verbose_name_plural = "اشتراكات المستخدمين"
        unique_together = ('user', 'course')

    def __str__(self):
        return f"اشتراك {self.user.username} في دورة: {self.course.title}"


# 4. نموذج الوحدات التعليمية (تقسيم الدورات إلى فصول)
class Module(models.Model):
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='modules',
        verbose_name="الدورة التابعة لها"
    )
    title = models.CharField(max_length=200, verbose_name="عنوان الوحدة")
    order = models.PositiveIntegerField(verbose_name="ترتيب الوحدة في الدورة")

    class Meta:
        verbose_name = "الوحدة التعليمية"
        verbose_name_plural = "الوحدات التعليمية"
        ordering = ['order']
        unique_together = ('course', 'order')

    def __str__(self):
        return f"{self.course.title} - الوحدة: {self.title}"


# 5. نموذج الدروس التفصيلية (محدث للتمييز بين منصة التعلم ومنصة التدريب)
class Lesson(models.Model):
    PLATFORM_CHOICES = [
        ('learning', 'منصة التعلم'),
        ('training', 'منصة التدريب'),
    ]
    SUBJECT_CHOICES = [
        ('history', 'تاريخ الجزائر'),
        ('geography', 'جغرافيا الجزائر'),
    ]
    LEVEL_CHOICES = [
        ('primary', 'التعليم الابتدائي'),
        ('middle', 'التعليم المتوسط'),
        ('secondary', 'التعليم الثانوي'),
        ('university', 'التعليم الجامعي'),
    ]

    platform_type = models.CharField(
        max_length=20, 
        choices=PLATFORM_CHOICES, 
        default='learning', 
        db_index=True,
        verbose_name="المنصة التابع لها الدرس"
    )
    module = models.ForeignKey(
        Module, 
        on_delete=models.CASCADE, 
        related_name='lessons',
        verbose_name="الوحدة التعليمية"
    )
    subject = models.CharField(
        max_length=20, 
        choices=SUBJECT_CHOICES, 
        default='history',
        verbose_name="المادة الدراسية"
    )
    level = models.CharField(
        max_length=20, 
        choices=LEVEL_CHOICES, 
        default='primary',
        verbose_name="المستوى الدراسي المستهدف"
    )
    title = models.CharField(max_length=200, verbose_name="عنوان الدرس")
    content = models.TextField(verbose_name="المحتوى النصي والشرح العلمي")
    video_url = models.URLField(blank=True, null=True, verbose_name="رابط فيديو الشرح (إن وجد)")
    arcgis_map_url = models.URLField(blank=True, null=True, default='#', verbose_name="رابط خريطة ArcGIS التفاعلية")
    duration_minutes = models.PositiveIntegerField(default=10, verbose_name="المدة المتوقعة (دقائق)")
    order = models.PositiveIntegerField(verbose_name="ترتيب الدرس ضمن الوحدة")

    class Meta: 
        verbose_name = "الدرس"
        verbose_name_plural = "الدروس التعليمية"
        ordering = ['order']

    def __str__(self):
        return f"[{self.get_platform_type_display()}] {self.module.title} - درس: {self.title}"


# نموذج تتبع إتمام الدروس للطلاب
class StudentLessonProgress(models.Model):
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='lesson_progress',
        verbose_name="الطالب"
    )
    lesson = models.ForeignKey(
        Lesson, 
        on_delete=models.CASCADE, 
        related_name='student_progress',
        verbose_name="الدرس"
    )
    is_completed = models.BooleanField(default=False, verbose_name="تم إتمام الدرس؟")
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإتمام")

    class Meta:
        verbose_name = "تقدم الطالب في الدرس"
        verbose_name_plural = "تقدم الطلاب في الدروس"
        unique_together = ('student', 'lesson')

    def __str__(self):
        status = "مكتمل ✅" if self.is_completed else "قيد الدراسة ⏳"
        return f"الطالب {self.student.username} - درس {self.lesson.title} ({status})"


# 6. نموذج المحتوى التاريخي الجغرافي العام
class HistoricalGeographicContent(models.Model):
    title = models.CharField(max_length=200, verbose_name="العنوان الرئيسي للمحتوى")
    main_text = models.TextField(verbose_name="المتن العلمي والتاريخي")
    image = models.ImageField(upload_to='historical/images/', null=True, blank=True, verbose_name="صورة المحتوى")
    location_name = models.CharField(max_length=255, verbose_name="الموقع الجغرافي", default="غير محدد")
    event_date = models.DateField(null=True, blank=True, verbose_name="تاريخ الحدث التاريخي")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ النشر في الموقع")

    class Meta:
        verbose_name = "المحتوى التاريخي الجغرافي"
        verbose_name_plural = "المحتويات التاريخية الجغرافية"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# 7. نموذج طلبات تفعيل الأطالس والاشتراكات عبر الحوالات البريدية CPC
class PaymentRequest(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='payment_requests',
        verbose_name="صاحب الطلب"
    )
    atlas_name = models.CharField(max_length=255, verbose_name="اسم أو رقم الأطلس المطلوب")
    cpc_receipt = models.ImageField(
        upload_to='payments/receipts/%Y/%m/', 
        verbose_name="نسخة مصورة من وصل دفع الحوالة البريدية CPC"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ إرسال الطلب")
    is_approved = models.BooleanField(
        default=False, 
        db_index=True,
        verbose_name="حالة تفعيل الحساب وتأكيد الدفع"
    )

    class Meta:
        verbose_name = "طلب دفع أطلس"
        verbose_name_plural = "طلبات الدفع والأطالس"
        ordering = ['-created_at']

    def __str__(self):
        return f"طلب تفعيل {self.atlas_name} للمستخدم {self.user.username}"


# 8. نموذج الوثائق التاريخية المفهرسة مكانياً
class HistoricalDocument(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان الوثيقة أو الخارطة")
    description = models.TextField(verbose_name="الوصف التاريخي والأثري")
    latitude = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        verbose_name="إحداثي خط العرض (Latitude)"
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        verbose_name="إحداثي خط الطول (Longitude)"
    )
    category = models.CharField(max_length=100, db_index=True, verbose_name="تصنيف المادة التاريخية")
    is_premium = models.BooleanField(
        default=False, 
        db_index=True,
        verbose_name="هل المادة مدفوعة ومحمية؟"
    )
    file = models.FileField(
        upload_to='archives/documents/%Y/', 
        verbose_name="ملف الوثيقة المؤرشف (PDF/Zip/TIFF)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الأرشفة الرقمية")

    class Meta:
        verbose_name = "الوثيقة المؤرشفة"
        verbose_name_plural = "خزانة الوثائق التاريخية"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# 9. نموذج بطاقات تفعيل الألعاب والمسارات التعليمية المطبوعة
class Card(models.Model):
    serial_number = models.CharField(
        max_length=100, 
        unique=True, 
        blank=True, 
        verbose_name="رقم التسلسل التسويقي (Serial)"
    )
    is_used = models.BooleanField(
        default=False, 
        db_index=True,
        verbose_name="هل تم استخدام هذا الرمز من قبل؟"
    )
    session_id = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name="معرف جلسة التفعيل النشطة"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ إصدار الكود")

    class Meta:
        verbose_name = "بطاقة تفعيل فكرية"
        verbose_name_plural = "بطاقات التفعيل المطبوعة"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.serial_number:
            self.serial_number = f"GM-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        status = "مستخدمة ❌" if self.is_used else "جاهزة للتفعيل ✅"
        return f"البطاقة {self.serial_number} ({status})"


# 10. نموذج بطاقات الدفع المسبق (محدث بالقيود وفهرسة الأداء للأعداد الكبيرة)
class PrepaidCard(models.Model):
    pin_code = models.CharField(
        max_length=50, 
        unique=True, 
        db_index=True, 
        verbose_name="رقم الكود"
    )
    duration_days = models.IntegerField(
        default=30, 
        verbose_name="مدة الصلاحية باليوم"
    )
    is_used = models.BooleanField(
        default=False, 
        db_index=True, 
        verbose_name="هل تم استخدامها؟"
    )
    used_by = models.ForeignKey(
        User, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        verbose_name="استخدمت بواسطة"
    )
    
    # حقول القيود الجديدة لتخصيص البطاقات حسب الأطوار والسنوات الدراسية
    target_cycle = models.CharField(
        max_length=50, 
        choices=UserProfile.CYCLE_CHOICES, 
        blank=True, 
        null=True, 
        verbose_name="الطور التعليمي المخصص للبطاقة",
        help_text="اتركه فارغاً إذا كانت البطاقة عامة لكل الأطوار"
    )
    target_year = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name="السنة الدراسية المخصصة للبطاقة",
        help_text="اتركه فارغاً إذا كانت البطاقة عامة لكل السنوات في هذا الطور"
    )

    class Meta:
        verbose_name = "بطاقة دفع مسبق"
        verbose_name_plural = "بطاقات الدفع المسبق"

    def __str__(self):
        cycle_info = f" [{self.target_cycle}]" if self.target_cycle else " [عامة]"
        return f"بطاقة بقيمة {self.duration_days} يوم{cycle_info} - {self.pin_code}"


# 11. نموذج تتبع تقدم الطالب في الدورات
class UserCourseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="الدورة")
    is_enrolled = models.BooleanField(default=False, verbose_name="مسجل مفعل")
    progress_percentage = models.PositiveIntegerField(default=0, verbose_name="نسبة الإنجاز (%)")
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")

    class Meta:
        verbose_name = "تقدم المستخدم في الدورة"
        verbose_name_plural = "تتبع تقدم المستخدمين في الدورات"

    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.progress_percentage}%)"


# 12. نموذج الشهادات المُكتسبة الموحد (يدعم منصة التعلم ومنصة التدريب)
class Certificate(models.Model):
    PLATFORM_CHOICES = (
        ('learning', 'منصة التعلم'),
        ('training', 'منصة التدريب'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, verbose_name="الدورة")
    course_name = models.CharField(max_length=255, verbose_name="اسم الدورة")
    platform_type = models.CharField(
        max_length=20, 
        choices=PLATFORM_CHOICES, 
        default='learning', 
        verbose_name="نوع المنصة"
    )
    language = models.CharField(max_length=50, default='ar', verbose_name="لغة الشهادة")
    issue_date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الاصدار")
    certificate_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name="معرف الشهادة")
    certificate_code = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="كود الشهادة")

    class Meta:
        verbose_name = "الشهادة المكتسبة"
        verbose_name_plural = "الشهادات المكتسبة"

    def save(self, *args, **kwargs):
        if not self.certificate_code:
            self.certificate_code = f"CERT-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"شهادة {self.user.username} - {self.course_name} ({self.get_platform_type_display()})"


class InteractiveMap(models.Model):
    lesson = models.OneToOneField(
        Lesson, 
        on_delete=models.CASCADE, 
        related_name='interactive_map',
        verbose_name="الدرس المرتبط بهذه الخريطة"
    )
    title = models.CharField(max_length=200, verbose_name="عنوان الخريطة التفاعلية")
    latitude = models.FloatField(default=36.7538, verbose_name="خط العرض المركزي (Latitude)")
    longitude = models.FloatField(default=3.0588, verbose_name="خط الطول المركزي (Longitude)")
    zoom_level = models.PositiveIntegerField(default=6, verbose_name="مستوى التكبير (Zoom)")
    
    # --- الصلاحيات والأذونات (تُتحكم فيها من لوحة التحكم) ---
    allow_student_drawing = models.BooleanField(default=False, verbose_name="السماح للطالب بالرسم والتلوين وتحديد المواقع؟")
    allow_student_markers = models.BooleanField(default=True, verbose_name="السماح للطالب بالنقر والتفاعل (وضع التحدي)؟")

    class Meta:
        verbose_name = "خريطة تفاعلية متقدمة"
        verbose_name_plural = "الخرائط التفاعلية المتقدمة"

    def __str__(self):
        return f"خريطة متقدمة: {self.lesson.title}"
