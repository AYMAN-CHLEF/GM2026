from django.urls import path
from . import views

urlpatterns = [
    # هذا الرابط سيصبح بالمتصفح: /atlas/revolution/
    path('revolution/', views.atlas_view, name='atlas_view'), 
    
    # هذا الرابط سيصبح بالمتصفح: /atlas/api/events/
    path('api/events/', views.get_events_json, name='get_events_json'),
]