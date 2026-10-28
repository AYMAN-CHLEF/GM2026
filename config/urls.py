from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
# تأكد من استيرادها بشكل صحيح من مكانها
# استيراد الدوال من الملفات الفرعية الجديدة
from core.views.auth_views import (
    LocalizedPasswordResetForm, LocalizedSetPasswordForm, SafePasswordResetView,
    dashboard_router, login_view, logout_view, register_gis, register_student,
    verification_pending, verify_email,
)
from django.contrib.auth import views as auth_views
from core.views.public_views import home_view, atlases_view, museum_view, library_view, activate_game, game_main, print_keys, payment_view, verify_certificate
from map_module import views as map_views 

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('favicon.ico', RedirectView.as_view(url='/static/images/Geo-Memory.jpeg', permanent=False), name='favicon'),
    path('admin/', admin.site.urls),
    
    # الروابط الرئيسية
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_student, name='register'), 
    path('register/gis/', register_gis, name='register_gis'),
    path('register/pending/', verification_pending, name='verification_pending'),
    path('register/verify/<str:token>/', verify_email, name='verify_email'),
    path('certificates/verify/<uuid:certificate_id>/', verify_certificate, name='verify_certificate'),
    path('password-reset/', SafePasswordResetView.as_view(
        form_class=LocalizedPasswordResetForm,
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.txt',
        html_email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url='/password-reset/done/',
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html',
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        form_class=LocalizedSetPasswordForm,
        template_name='registration/password_reset_confirm.html',
        success_url='/reset/done/',
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html',
    ), name='password_reset_complete'),
    path('dashboard/', dashboard_router, name='dashboard_router'),
    # 1. المنصة التعليمية
    path('student/', include('core.urls_students', namespace='student')),
    
    # 2. منصة التدريب التقني (GIS + البرمجة)
    path('gis-training/', include('core.urls_gis', namespace='gis')),
    
    # الخدمات والمميزات
    path('atlases/', atlases_view, name='atlases'),
    path('atlas/', include('atlas_revolution.urls')),
    path('payment/upload/', payment_view, name='payment_upload'),
    path('museum/', museum_view, name='digital_museum'),
    path('library/', library_view, name='library'),
    path('dakira/', include('dakira_haya.urls', namespace='dakira_haya')),
    path('activate/', activate_game, name='activate_game'),
    path('game/', game_main, name='game_main'),
    path('print-cards/', print_keys, name='print_keys'),
    path('map/', map_views.map_view, name='map'),
    path('impact/', include('core.urls_public', namespace='public')),
    # ربط مسارات تطبيق gecc_core بالكامل
    path('', include('gecc_core.urls')),
    # أجب عن هذا السطر لربط مسارات تطبيق المعالم
    path('', include('monuments.urls')),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
