from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomAuthToken,
    LocationViewSet, 
    HeritageAssetViewSet, 
    VisitorFlowViewSet,
    FieldReportViewSet,
    TouristServiceViewSet,      # تسجيل الفيو الجديد للخدمات
    BookingRequestViewSet,      # تسجيل الفيو الجديد للحجوزات
    DigitalDashboardView,
    SmartRecommendationAPIView,
    MapDataAPIView,             # استيراد نقطة نهاية الخريطة الموحدة
    AnalyticsDashboardAPIView,  # نقطة نهاية API لتحليلات الذكاء الاصطناعي
    analytics_dashboard_view    # دالة عرض لوحة تحليلات الذكاء الاصطناعي التقليدية
)

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'heritage-assets', HeritageAssetViewSet, basename='heritageasset')
router.register(r'visitor-flows', VisitorFlowViewSet, basename='visitorflow')
router.register(r'field-reports', FieldReportViewSet, basename='fieldreport')
router.register(r'tourist-services', TouristServiceViewSet, basename='touristservice') # تسجيل مسار الخدمات
router.register(r'booking-requests', BookingRequestViewSet, basename='bookingrequest') # تسجيل مسار الحجوزات

urlpatterns = [
    # مسار لوحة القيادة الرقمية
    path('tahwissa/', DigitalDashboardView.as_view(), name='digital_twin_dashboard'),
    
    # مسار لوحة تحليلات الذكاء الاصطناعي (Template View)
    path('ai-dashboard/', analytics_dashboard_view, name='ai_dashboard_view'),
    
    # نقطة نهاية المصادقة وإصدار التوكن
    path('api/gecc/auth/token/', CustomAuthToken.as_view(), name='api_token_auth'),
    
    # مسارات الـ API الخاصة بالـ ViewSets
    path('api/gecc/', include(router.urls)),
    
    # نقطة نهاية التوصيات الذكية
    path('api/gecc/recommendations/', SmartRecommendationAPIView.as_view(), name='smart_recommendations'),
    
    # نقطة نهاية تحليلات الذكاء الاصطناعي والطلب المستقبلي (API)
    path('api/gecc/ai-analytics/', AnalyticsDashboardAPIView.as_view(), name='api_ai_analytics'),
    
    # نقطة نهاية الخريطة الموحدة (جلب المعالم + الخدمات)
    path('api/gecc/map-data/', MapDataAPIView.as_view(), name='api_map_data'),
    
    
]