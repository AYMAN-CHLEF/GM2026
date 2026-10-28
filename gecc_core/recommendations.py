import math
from .models import HeritageAsset

def calculate_distance(lat1, lon1, lat2, lon2):
    """حساب المسافة الجغرافية البسيطة بين نقطتين بالمكيلومتر (Haversine formula مبسطة)"""
    R = 6371  # نصف قطر الأرض بالكيلومتر
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_smart_recommendations(user_lat, user_lon, user_interests=None, max_distance_km=50):
    """
    محرك التوصية الذكي:
    يقوم بتصفية وترتيب المعالم التراثية بناءً على الموقع الجغرافي واهتمامات السائح.
    """
    assets = HeritageAsset.objects.all()
    recommended_list = []
    interests = [str(item).casefold() for item in (user_interests or [])]

    for asset in assets:
        if asset.latitude is None or asset.longitude is None:
            continue
        distance = calculate_distance(user_lat, user_lon, asset.latitude, asset.longitude)
        if distance > max_distance_km:
            continue
        searchable_text = f'{asset.category} {asset.name} {asset.description}'.casefold()
        interest_score = sum(1 for interest in interests if interest in searchable_text)
        score = max(0, 100 - distance) + interest_score * 10
        recommended_list.append({
            'asset_id': asset.id,
            'name': asset.name,
            'distance_km': round(distance, 2),
            'score': round(score, 2),
        })

    # ترتيب النتائج حسب الأفضلية والأقرب
    recommended_list = sorted(recommended_list, key=lambda x: x['score'], reverse=True)
    return recommended_list[:10] # إرجاع أفضل 10 وجهات مقترحة
