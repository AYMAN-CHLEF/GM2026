import logging
import math

from django.shortcuts import render
from .ai_engine.services import GeoMemoryAIEngine
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission, SAFE_METHODS
from rest_framework.throttling import ScopedRateThrottle
from django.views.generic import TemplateView

from .recommendations import get_smart_recommendations
from .models import Location, HeritageAsset, VisitorFlow, FieldReport, TouristService, BookingRequest
from .serializers import (
    LocationSerializer, 
    HeritageAssetSerializer, 
    VisitorFlowSerializer,
    FieldReportSerializer,
    TouristServiceSerializer,
    BookingRequestSerializer
)

logger = logging.getLogger(__name__)


class PublicReadAdminWrite(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or bool(request.user and request.user.is_staff)


class PublicBookingCreate(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('POST', 'OPTIONS'):
            return True
        return bool(request.user and request.user.is_staff)

class CustomAuthToken(ObtainAuthToken):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth_token'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'message': 'تم المصادقة بنجاح وإصدار رمز الدخول'
        })

class DigitalDashboardView(TemplateView):
    """
    لوحة القيادة الرقمية الرئيسية (تتضمن بيانات الذكاء الاصطناعي المحقونة مباشرة لسرعة العرض)
    """
    template_name = 'gecc_core/digital_twin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # 1. جلب المعالم الحقيقية من قاعدة البيانات للتحليل
            real_locations = list(HeritageAsset.objects.values('id', 'name', 'category', 'description'))
            for loc in real_locations:
                loc['tags'] = f"{loc.get('category', '')}, {loc.get('description', '')}"
            
            user_interests = ['تاريخ', 'أثري']
            recommendations = GeoMemoryAIEngine.get_personalized_recommendations(user_interests, real_locations)
            
            # 2. جلب سجلات الزوار الحقيقية للتنبؤ بالطلب المستقبلي
            historical_visits = list(VisitorFlow.objects.values_list('visitor_count', flat=True).order_by('timestamp'))
            if len(historical_visits) < 3:
                historical_visits = [100, 115, 130, 145, 170]
            
            predicted_visits = GeoMemoryAIEngine.predict_future_demand(historical_visits)

            context['ai_recommendations'] = recommendations
            context['predicted_visits'] = predicted_visits
        except Exception:
            context['ai_recommendations'] = []
            context['predicted_visits'] = 0
            
        return context

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [PublicReadAdminWrite]

class HeritageAssetViewSet(viewsets.ModelViewSet):
    queryset = HeritageAsset.objects.all()
    serializer_class = HeritageAssetSerializer
    permission_classes = [PublicReadAdminWrite]

class VisitorFlowViewSet(viewsets.ModelViewSet):
    queryset = VisitorFlow.objects.all()
    serializer_class = VisitorFlowSerializer
    permission_classes = [PublicReadAdminWrite]

class TouristServiceViewSet(viewsets.ModelViewSet):
    """إدارة الخدمات السياحية، الإقامات، والحرفيين"""
    queryset = TouristService.objects.all()
    serializer_class = TouristServiceSerializer
    permission_classes = [PublicReadAdminWrite]

class BookingRequestViewSet(viewsets.ModelViewSet):
    """إدارة طلبات حجز المبيت أو التواصل"""
    queryset = BookingRequest.objects.all().order_by('-created_at')
    serializer_class = BookingRequestSerializer
    permission_classes = [PublicBookingCreate]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'booking_create'

    def get_queryset(self):
        if self.request.user.is_staff:
            return BookingRequest.objects.all().order_by('-created_at')
        return BookingRequest.objects.none()

class FieldReportViewSet(viewsets.ModelViewSet):
    queryset = FieldReport.objects.all().order_by('-created_at')
    serializer_class = FieldReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return FieldReport.objects.all().order_by('-created_at')
        return FieldReport.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # ربط التقرير تلقائياً بالمستخدم المُصادق عليه حالياً
        serializer.save(user=self.request.user)

class MapDataAPIView(APIView):
    """نقطة نهاية موحدة لجلب المعالم التراثية والخدمات السياحية للخريطة"""
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'public_map'

    def get(self, request):
        try:
            # 1. جلب المعالم التراثية
            assets = list(HeritageAsset.objects.values(
                'id', 'name', 'description', 'latitude', 'longitude', 'category'
            ))
            
            # 2. جلب الخدمات (فنادق، مطاعم، حرفيين، مرشدين)
            services = []
            for service in TouristService.objects.all():
                services.append({
                    'id': service.id,
                    'name': service.name,
                    'category': service.category,
                    'category_display': service.get_category_display(),
                    'description': service.description,
                    'latitude': service.latitude,
                    'longitude': service.longitude,
                    'contact_person': service.contact_person,
                    'phone': service.phone,
                    'price': float(service.price_per_unit) if service.price_per_unit else None,
                    'image_url': service.image.url if service.image else None,
                    'supports_duration': service.supports_duration_booking,
                    'related_asset_id': service.related_asset.id if service.related_asset else None
                })
                
            return Response({
                'status': 'success',
                'heritage_assets': assets,
                'tourist_services': services,
                'message': 'تم جلب بيانات الخريطة بنجاح'
            })
        except Exception:
            logger.exception('Failed to assemble public map data.')
            return Response({
                'status': 'error',
                'message': 'تعذر تحميل بيانات الخريطة حالياً.'
            }, status=500)

class SmartRecommendationAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'public_ai'

    def get(self, request):
        try:
            lat = float(request.GET.get('lat', 36.7538))  # الافتراضي إحداثيات الجزائر العاصمة
            lon = float(request.GET.get('lon', 3.0588))
            max_dist = float(request.GET.get('max_distance', 100))
            if not all(map(math.isfinite, (lat, lon, max_dist))) or not (-90 <= lat <= 90) or not (-180 <= lon <= 180) or not (0 < max_dist <= 500):
                raise ValueError
            
            interests = request.GET.getlist('interests')
            recommendations = get_smart_recommendations(lat, lon, user_interests=interests, max_distance_km=max_dist)
            
            return Response({
                'status': 'success',
                'user_location': {'lat': lat, 'lon': lon},
                'recommended_assets': recommendations,
                'message': 'تم توليد التوصيات السياحية الذكية بنجاح بناءً على الموقع الجغرافي والتحليل المكاني'
            })
        except (TypeError, ValueError):
            return Response({
                'status': 'error',
                'message': 'قيم الموقع أو المسافة غير صالحة.'
            }, status=400)
        except Exception:
            logger.exception('Failed to generate public heritage recommendations.')
            return Response({'status': 'error', 'message': 'تعذر إنشاء التوصيات حالياً.'}, status=500)

class AnalyticsDashboardAPIView(APIView):
    """
    نقطة نهاية API لربط لوحة التحليلات بمحرك الذكاء الاصطناعي والبيانات الحقيقية
    """
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'public_ai'

    def get(self, request):
        try:
            # 1. جلب المعالم الحقيقية من قاعدة البيانات
            real_locations = list(HeritageAsset.objects.values('id', 'name', 'category', 'description'))
            for loc in real_locations:
                loc['tags'] = f"{loc.get('category', '')}, {loc.get('description', '')}"

            # 2. اهتمامات السائح
            user_interests = [value[:80] for value in request.GET.getlist('interests')[:10] if value.strip()] or ['تاريخ', 'أثري', 'سياحة']

            # 3. توليد التوصيات الشخصية الذكية
            recommendations = GeoMemoryAIEngine.get_personalized_recommendations(user_interests, real_locations)

            # 4. جلب سجلات تدفق الزوار التاريخية الحقيقية للتنبؤ بالطلب المستقبلي
            historical_visits = list(VisitorFlow.objects.values_list('visitor_count', flat=True).order_by('timestamp'))
            if len(historical_visits) < 3:
                historical_visits = [100, 115, 130, 145, 170]

            # 5. التنبؤ بالطلب القادم عبر النموذج الخطي
            predicted_demand = GeoMemoryAIEngine.predict_future_demand(historical_visits)

            return Response({
                'status': 'success',
                'ai_recommendations': recommendations,
                'predictive_analytics': {
                    'historical_data': historical_visits,
                    'predicted_next_period_demand': predicted_demand
                },
                'message': 'تم جلب تحليلات الذكاء الاصطناعي وتوقعات الطلب بنجاح'
            })
        except Exception:
            logger.exception('Failed to generate public analytics.')
            return Response({
                'status': 'error',
                'message': 'تعذر إنشاء التحليلات حالياً.'
            }, status=500)

def analytics_dashboard_view(request):
    """
    دالة العرض التقليدية (Template View) المدعومة بالبيانات الحقيقية ومحرك الذكاء الاصطناعي
    """
    try:
        real_locations = list(HeritageAsset.objects.values('id', 'name', 'category', 'description'))
        for loc in real_locations:
            loc['tags'] = f"{loc.get('category', '')}, {loc.get('description', '')}"
            
        user_interests = ['تاريخ', 'أثري']
        
        recommendations = GeoMemoryAIEngine.get_personalized_recommendations(user_interests, real_locations)
        historical_visits_data = list(VisitorFlow.objects.values_list('visitor_count', flat=True).order_by('timestamp'))
        
        if len(historical_visits_data) < 3:
            historical_visits_data = [100, 115, 130, 145, 170]
            
        predicted_visits = GeoMemoryAIEngine.predict_future_demand(historical_visits_data)
    except Exception:
        logger.exception('Failed to render the analytics dashboard.')
        recommendations = []
        predicted_visits = 0
    
    context = {
        'recommendations': recommendations,
        'predicted_visits': predicted_visits,
    }
    return render(request, 'gecc_core/ai_dashboard.html', context)
