from django.shortcuts import render
from django.http import JsonResponse
from .models import HistoricalEvent

def atlas_view(request):
    """عرض صفحة الأطلس التفاعلي"""
    context = {
        'title': 'أطلس الثورة الجزائرية',
        'description': 'خريطة تفاعلية توثق معارك ومراكز قيادة الثورة التحريرية.'
    }
    return render(request, 'atlas_revolution/atlas_revolution.html', context)

def get_events_json(request):
    """جلب المعارك والمراكز بتنسيق GeoJSON متوافق مع Leaflet"""
    events = HistoricalEvent.objects.all()
    
    # تحويل البيانات إلى هيكل GeoJSON
    features = []
    for e in events:
        feature = {
            "type": "Feature",
            "properties": {
                "name": e.name,
                "type": e.event_type,
                "wilaya": e.wilaya,
                "date": str(e.date),
                "leader": e.leader,
                "description": e.description,
                "outcome": e.outcome
            },
            "geometry": {
                "type": "Point",
                "coordinates": [e.lng, e.lat] # ملاحظة: GeoJSON يستخدم [خط الطول، خط العرض]
            }
        }
        features.append(feature)
    
    return JsonResponse({"type": "FeatureCollection", "features": features}, safe=False)