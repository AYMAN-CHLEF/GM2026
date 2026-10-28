from django.urls import path
from core.views.gis_views import (
    gis_dashboard, 
    gis_training_view, 
    course_detail_view
)

app_name = 'gis' 

urlpatterns = [
    path('dashboard/', gis_dashboard, name='dashboard'),
    path('training/', gis_training_view, name='training'),
    path('course/<int:course_id>/', course_detail_view, name='course_detail'),
]