from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import ProfileUpdateForm, ProfileImageForm
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db import transaction
from django.core.exceptions import PermissionDenied
from io import BytesIO
import base64
import qrcode
from datetime import timedelta
from ..models import PrepaidCard, UserCourse, UserCourseProgress, UserProfile  # تم التأكد من استيراد النماذج الصحيحة

class ProgrammaticLesson:
    def __init__(self, id, title, module_title, video_url, content, arcgis_map_url):
        self.id = id
        self.title = title
        self.module = type('Module', (object,), {'title': module_title})
        self.video_url = video_url
        self.content = content
        self.arcgis_map_url = arcgis_map_url

HARDCODED_LESSONS = {
    '1': ProgrammaticLesson(1, "الجزائر: مهد الحضارات الإنسانية", "تاريخ الجزائر", "https://www.youtube.com/embed/8kS1s8QJ43U", "محتوى التاريخ...", "#"),
    '2': ProgrammaticLesson(2, "الموقع الجغرافي: بوابة القارات", "جغرافيا الجزائر", "https://www.youtube.com/embed/yQ8Q8wV02_s", "محتوى الجغرافيا...", "#")
}


def _require_student_account(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    if profile.user_type != 'student':
        raise PermissionDenied("هذه المساحة مخصصة لحسابات منصة التعليم.")
    return profile

@login_required
def student_dashboard(request):
    _require_student_account(request.user)
    # 1. جلب المتغيرات من رابط الـ GET
    lesson_id = request.GET.get('lesson')
    subject_filter = request.GET.get('subject')
    level_filter = request.GET.get('level')
    show_profile = request.GET.get('profile') == 'true'
    
    lesson = HARDCODED_LESSONS.get(str(lesson_id))

    # 2. تصفية الدروس البرمجية حسب المادة
    filtered_lessons = []
    if subject_filter:
        for l_id, l_obj in HARDCODED_LESSONS.items():
            if subject_filter == 'history' and 'تاريخ' in l_obj.module.title:
                filtered_lessons.append(l_obj)
            elif subject_filter == 'geography' and 'جغرافيا' in l_obj.module.title:
                filtered_lessons.append(l_obj)

    # 3. جلب أو إنتاج ملف التعريف الشخصي
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # تهيئة النماذج بالبيانات الحالية
    user_form = ProfileUpdateForm(instance=user_profile)
    profile_form = ProfileImageForm(instance=user_profile)
    
    # 4. معالجة تحديث البيانات عند الإرسال (POST) فقط إذا كان الطلب لإعدادات الحساب
    if request.method == 'POST' and show_profile:
        user_form = ProfileUpdateForm(request.POST, instance=user_profile)
        profile_form = ProfileImageForm(request.POST, request.FILES, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "تم تحديث وتصحيح بيانات الحساب بنجاح!")
            return redirect(reverse('student:student_dashboard') + '?profile=true')
        else:
            messages.error(request, "حدث خطأ في تحديث البيانات، يرجى مراجعة الحقول المدخلة.")

    return render(request, 'dashboard.html', {
        'lesson': lesson,
        'filtered_lessons': filtered_lessons,
        'subject_filter': subject_filter,
        'level_filter': level_filter,
        'show_profile': show_profile,
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': user_profile,
    })
    
@login_required
def lesson_detail(request, lesson_id):
    _require_student_account(request.user)
    return redirect(f'/student/dashboard/?lesson={lesson_id}')

@login_required
@require_POST
def mark_lesson_complete(request, lesson_id):
    from ..models import Lesson, StudentLessonProgress
    _require_student_account(request.user)
    lesson = get_object_or_404(Lesson, id=lesson_id, platform_type='learning')
    course = lesson.module.course
    if not course.is_free and not (
        UserCourse.objects.filter(user=request.user, course=course).exists()
        or UserCourseProgress.objects.filter(user=request.user, course=course, is_enrolled=True).exists()
    ):
        raise PermissionDenied("يلزم التسجيل في الدورة قبل حفظ تقدمك فيها.")
    StudentLessonProgress.objects.update_or_create(
        student=request.user,
        lesson=lesson,
        defaults={'is_completed': True},
    )
    messages.success(request, "تم تسجيل إتمام الدرس بنجاح!")
    return redirect(f'/student/dashboard/?lesson={lesson_id}')

@login_required
def student_certificate(request):
    _require_student_account(request.user)
    profile = get_object_or_404(UserProfile, user=request.user)
    certificate = Certificate.objects.filter(user=request.user).select_related('course').order_by('-issue_date').first()
    if not certificate:
        return render(request, 'student/certificate_unavailable.html')
    verify_url = request.build_absolute_uri(reverse(
        'verify_certificate', kwargs={'certificate_id': certificate.certificate_id}
    ))
    qr_image = qrcode.make(verify_url)
    qr_buffer = BytesIO()
    qr_image.save(qr_buffer, format='PNG')
    qr_data_uri = 'data:image/png;base64,' + base64.b64encode(qr_buffer.getvalue()).decode('ascii')
    context = {
        'profile': profile,
        'certificate': certificate,
        'qr_data_uri': qr_data_uri,
    }
    return render(request, 'student/certificate.html', context)

@login_required
def activate_subscription(request):
    _require_student_account(request.user)
    if request.method == 'POST':
        card_pin = request.POST.get('card_pin', '').strip()
        
        try:
            with transaction.atomic():
                card = PrepaidCard.objects.select_for_update().get(pin_code=card_pin, is_used=False)
                profile, created = UserProfile.objects.get_or_create(user=request.user)
                if card.target_cycle and profile.educational_cycle != card.target_cycle:
                    messages.error(request, 'هذه البطاقة مخصصة لطور تعليمي آخر.')
                    return redirect(reverse('student:student_dashboard') + '?profile=true')
                if card.target_year and profile.academic_year != card.target_year:
                    messages.error(request, 'هذه البطاقة مخصصة لسنة دراسية أخرى.')
                    return redirect(reverse('student:student_dashboard') + '?profile=true')
                claimed = PrepaidCard.objects.filter(pk=card.pk, is_used=False).update(is_used=True, used_by=request.user)
                if not claimed:
                    raise PrepaidCard.DoesNotExist
                now = timezone.now()
                start_date = profile.subscription_end_date if profile.subscription_end_date and profile.subscription_end_date > now else now
                profile.subscription_end_date = start_date + timedelta(days=card.duration_days)
                profile.is_active_subscription = True
                profile.save()
            
            messages.success(request, f'تم تفعيل الاشتراك بنجاح لمدة {card.duration_days} يوم!')
            
        except PrepaidCard.DoesNotExist:
            messages.error(request, 'رقم البطاقة غير صالح، أو أنه تم استخدامه مسبقاً.')
            
    return redirect(reverse('student:student_dashboard') + '?profile=true')
