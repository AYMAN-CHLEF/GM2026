import re

from rest_framework import serializers
from .models import Location, HeritageAsset, VisitorFlow, FieldReport, TouristService, BookingRequest

class BaseTranslatedSerializer(serializers.ModelSerializer):
    """سيريالايزر أساسي يحتوي على منطق الترجمة المشترك"""
    
    def get_translated_field(self, obj, field_name):
        request = self.context.get('request')
        # استخراج اللغة من الهيدر (Default: ar)
        lang = request.headers.get('Accept-Language', 'ar') if request else 'ar'
        data = getattr(obj, field_name, {})
        # إذا كانت البيانات مخزنة كـ JSON/Dict للترجمة
        if isinstance(data, dict):
            fallback = data.get('en', data.get('ar', '')) if lang == 'es' else data.get('ar', '')
            return data.get(lang, fallback)
        if isinstance(data, str) and ' | ' in data:
            parts = [part.strip() for part in data.split(' | ')]
            if len(parts) >= 3:
                return parts[{'ar': 0, 'fr': 1, 'en': 2, 'tr': 2, 'es': 2}.get(lang, 0)]
            if len(parts) == 2:
                if lang == 'fr':
                    return parts[1]
                first = parts[0]
                if ' - ' in first:
                    local_name, english_name = first.split(' - ', 1)
                    return local_name if lang == 'ar' else english_name
                return parts[0] if lang == 'ar' else parts[1]
        if isinstance(data, str) and lang != 'ar' and ' - ' in data:
            return data.split(' - ', 1)[1].strip()
        return data

class LocationSerializer(BaseTranslatedSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj): 
        return self.get_translated_field(obj, 'name')

    class Meta:
        model = Location
        fields = ['id', 'name', 'coordinates', 'created_at']

class HeritageAssetSerializer(BaseTranslatedSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_name(self, obj): 
        return self.get_translated_field(obj, 'name')
        
    def get_description(self, obj): 
        return self.get_translated_field(obj, 'description')

    class Meta:
        model = HeritageAsset
        fields = '__all__'

class VisitorFlowSerializer(BaseTranslatedSerializer):
    class Meta:
        model = VisitorFlow
        fields = '__all__'

class FieldReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldReport
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class TouristServiceSerializer(BaseTranslatedSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    def get_name(self, obj): 
        return self.get_translated_field(obj, 'name')
        
    def get_description(self, obj): 
        return self.get_translated_field(obj, 'description')

    class Meta:
        model = TouristService
        fields = '__all__'

class BookingRequestSerializer(serializers.ModelSerializer):
    def validate_duration_value(self, value):
        limits = {'days': 365, 'weeks': 52, 'months': 36}
        duration_type = self.initial_data.get('duration_type', 'days')
        maximum = limits.get(duration_type)
        if maximum is None or not 1 <= value <= maximum:
            raise serializers.ValidationError('مدة الحجز خارج النطاق المسموح.')
        return value

    def validate_phone(self, value):
        value = value.strip()
        digits = sum(character.isdigit() for character in value)
        if not re.fullmatch(r'\+?[0-9][0-9 ()-]{5,23}', value) or not 7 <= digits <= 15:
            raise serializers.ValidationError('أدخل رقم هاتف صالحاً للتواصل.')
        return value

    def validate_visitor_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('الاسم مطلوب.')
        return value

    def validate_notes(self, value):
        if len(value) > 2000:
            raise serializers.ValidationError('يجب ألا تتجاوز الملاحظات 2000 حرف.')
        return value

    class Meta:
        model = BookingRequest
        fields = ['id', 'service', 'visitor_name', 'phone', 'duration_type', 'duration_value', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']
