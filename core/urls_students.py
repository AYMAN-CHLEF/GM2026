from django.urls import path
from core.views import student_views

app_name = 'student'

urlpatterns = [
    path('dashboard/', student_views.student_dashboard, name='student_dashboard'),
    path('lesson/<int:lesson_id>/', student_views.lesson_detail, name='lesson_detail'),
    path('lesson/complete/<int:lesson_id>/', student_views.mark_lesson_complete, name='mark_lesson_complete'),
    #path('profile/', student_views.profile_settings, name='profile_settings'),
    path('certificate/', student_views.student_certificate, name='student_certificate'),
    path('activate-subscription/', student_views.activate_subscription, name='activate_subscription'),
]