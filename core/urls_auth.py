from django.urls import path
from core.views.auth_views import register_student, login_view, logout_view

# app_name اختياري هنا، لكن يفضل استخدامه للتنظيم
app_name = 'auth'

urlpatterns = [
    path('register/', register_student, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]