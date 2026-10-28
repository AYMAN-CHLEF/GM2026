from django.urls import path
from . import views

app_name = 'dakira_haya'

urlpatterns = [
    # رابط المكتبة: المسار سيكون http://127.0.0.1:8000/dakira/library/
    path('library/', views.flags_list, name='flags_list'),
    
    # رابط الأطلس: المسار سيكون http://127.0.0.1:8000/dakira/atlas/
    path('atlas/', views.map_view, name='map_page'),
    
    # رابط تفاصيل الشخصية: المسار سيكون http://127.0.0.1:8000/dakira/figure/slug-name/
    path('figure/<slug:slug>/', views.flag_detail, name='flag_detail'),
    
]