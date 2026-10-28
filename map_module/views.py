from django.shortcuts import render
from django.conf import settings # لاستيراد المسارات من الإعدادات

def map_view(request):
    context = {
        'static_url': settings.STATIC_URL 
    }
    return render(request, 'map_module/oran.html', context)