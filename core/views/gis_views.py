from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Course, UserCourseProgress, Certificate, UserProfile, Lesson
from django.contrib import messages  # تأكد من استيرادها أعلى الملف
from django.core.exceptions import PermissionDenied
from core.forms import GISRegisterForm, UserUpdateForm, UserProfileUpdateForm
from core.views.auth_views import get_user_context

@login_required
def course_detail_view(request, course_id):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if profile.user_type != 'gis_trainee':
        raise PermissionDenied("هذه الصفحة مخصصة لحسابات المتدربين التقنيين.")
    course = get_object_or_404(Course, id=course_id)
    has_enrollment = UserCourseProgress.objects.filter(user=request.user, course=course, is_enrolled=True).exists()
    has_purchase = course.enrollments.filter(user=request.user).exists()
    if not course.is_free and not (has_enrollment or has_purchase):
        raise PermissionDenied("يلزم الاشتراك في الدورة للوصول إلى محتواها.")
    
    # التعامل مع الفلترة أو المعلمات الاختيارية للدرس (إذا كانت ممررة عبر الـ GET)
    selected_lesson_id = request.GET.get('lesson')
    current_lesson = None
    if selected_lesson_id:
        current_lesson = get_object_or_404(
            Lesson, id=selected_lesson_id, module__course=course, platform_type='training'
        )
    
    # 1. جلب بيانات السياق الأساسية للمستخدم
    context = get_user_context(request.user) if request.user.is_authenticated else {}
    
    # 2. حساب الإحصائيات الحقيقية للمستخدم (لضمان ظهورها في الهيدر أو الشريط الجانبي إن وجدت)
    enrolled_courses_count = UserCourseProgress.objects.filter(user=request.user, is_enrolled=True).count()
    
    all_progresses = UserCourseProgress.objects.filter(user=request.user, is_enrolled=True)
    if all_progresses.exists():
        total_progress = sum([p.progress_percentage for p in all_progresses])
        overall_progress = round(total_progress / all_progresses.count())
    else:
        overall_progress = 0
        
    certificates_count = Certificate.objects.filter(user=request.user).count()

    # 3. جلب محاور الدورة الحالية (تأكد من مطابقة اسم العقدة/Related name مثل modules أو course_modules)
    course_modules = course.modules.all() if hasattr(course, 'modules') else []

    # 4. دمج كافة البيانات في الـ Context لتفعيل الشريط الجانبي الديناميكي والدرس الحالي
    context.update({
        'course': course,
        'active_course': course,  # لتفعيل عرض محاور الدورة في الشريط الجانبي تلقائياً
        'course_modules': course_modules,
        'lesson': current_lesson,  # تمرير الدرس الحالي المختار إن وجد ليتوافق مع القالب الخاص بك
        'enrolled_courses_count': enrolled_courses_count,
        'overall_progress': overall_progress,
        'certificates_count': certificates_count,
    })
    
    return render(request, 'course_detail.html', context)

def register_gis(request):
    form = GISRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        # تكملة منطق التسجيل هنا...
        return redirect('login') 
    return render(request, 'register_gis.html', {'form': form})

@login_required
def gis_dashboard(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    if profile.user_type != 'gis_trainee':
        raise PermissionDenied("هذه المساحة مخصصة لحسابات المتدربين التقنيين.")
    
    # --- معالجة تحديث إعدادات الحساب والصورة الشخصية باستخدام نماذج Django لضمان مطابقة الـ HTML الجديد ---
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "تم تحديث الملف التقني وإعدادات الحساب بنجاح!")
            return redirect(request.path)
        else:
            messages.error(request, "يرجى تصحيح الأخطاء الموجودة في الحقول أدناه.")
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileUpdateForm(instance=profile)

    # دعم الفلترة الديناميكية بناءً على نوع الدورة
    course_type = request.GET.get('type', 'all')
    if course_type == 'coding':
        courses = Course.objects.filter(course_type='coding') 
    elif course_type == 'gis':
        courses = Course.objects.filter(course_type='specialized')
    else:
        courses = Course.objects.all()

    # الإحصائيات الحقيقية للمستخدم
    enrolled_courses_count = UserCourseProgress.objects.filter(user=request.user, is_enrolled=True).count()
    
    all_progresses = UserCourseProgress.objects.filter(user=request.user, is_enrolled=True)
    if all_progresses.exists():
        total_progress = sum([p.progress_percentage for p in all_progresses])
        overall_progress = round(total_progress / all_progresses.count())
    else:
        overall_progress = 0
        
    certificates_count = Certificate.objects.filter(user=request.user).count()

    context = get_user_context(request.user)
    context.update({
        'target_space': 'gis_training',
        'courses': courses,
        'profile': profile,
        'user_form': user_form,
        'profile_form': profile_form,
        'enrolled_courses_count': enrolled_courses_count,
        'overall_progress': overall_progress,
        'certificates_count': certificates_count,
        'active_course': None,
    })
    return render(request, 'gis_workspace.html', context)

@login_required
def gis_training_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if profile.user_type != 'gis_trainee':
        raise PermissionDenied("هذه المنصة مخصصة لحسابات المتدربين التقنيين.")
    
    enrolled_courses_count = UserCourseProgress.objects.filter(user=request.user, is_enrolled=True).count()
    
    all_progresses = UserCourseProgress.objects.filter(user=request.user, is_enrolled=True)
    if all_progresses.exists():
        total_progress = sum([p.progress_percentage for p in all_progresses])
        overall_progress = round(total_progress / all_progresses.count())
    else:
        overall_progress = 0
        
    certificates_count = Certificate.objects.filter(user=request.user).count()

    context = get_user_context(request.user)
    context.update({
        'profile': profile,
        'courses': Course.objects.all(),
        'enrolled_courses_count': enrolled_courses_count,
        'overall_progress': overall_progress,
        'certificates_count': certificates_count,
        'active_course': None,
    })
    return render(request, 'gis_workspace.html', context)
