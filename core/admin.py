from django.contrib import admin
from django.shortcuts import render, redirect
from .models import (
    UserProfile, HistoricalGeographicContent, Course, Module, Lesson, 
    UserCourse, PaymentRequest, StudentLessonProgress, Certificate, 
    HistoricalDocument, Card, PrepaidCard, InteractiveMap
)
from atlas_revolution.models import HistoricalEvent 
from django.urls import path
from django import forms
from django.contrib import messages
import uuid

# تخصيص عنوان لوحة التحكم باللغة العربية
admin.site.site_header = "إدارة منصة ذاكرة وجغرافيا الجزائر"
admin.site.site_title = "لوحة التحكم"
admin.site.index_title = "إدارة النظام والبيانات التعليمية"

# 1. إعدادات الـ Inlines (تظهر داخل الصفحات الرئيسية)
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    verbose_name = "درس"
    verbose_name_plural = "الدروس"

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    verbose_name = "وحدة تعليمية"
    verbose_name_plural = "الوحدات التعليمية"

# Inline خاص بالخريطة التفاعلية لتظهر مباشرة داخل صفحة تعديل الدرس
class InteractiveMapInline(admin.StackedInline):
    model = InteractiveMap
    can_delete = True
    verbose_name = "الخريطة التفاعلية المرتبطة"
    verbose_name_plural = "الخريطة التفاعلية"
    extra = 0

# 2. تسجيل النماذج مع تعريب كامل للوحات العرض والتصفية

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'level', 'points')
    list_filter = ('user_type', 'level')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(HistoricalGeographicContent)
class HistAdmin(admin.ModelAdmin):
    list_display = ('title', 'location_name', 'event_date', 'created_at')
    list_filter = ('event_date',)
    search_fields = ('title', 'location_name')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_type', 'price', 'is_free', 'created_at')
    list_filter = ('course_type', 'is_free')
    search_fields = ('title',)
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform_type', 'module', 'subject', 'level', 'order')
    list_filter = ('platform_type', 'subject', 'level', 'module__course')
    search_fields = ('title', 'content')
    # إضافة خريطة الدرس مباشرة كـ Inline داخل صفحة الدرس
    inlines = [InteractiveMapInline]

# تسجيل نموذج الخريطة التفاعلية المتقدمة بشكل مستقل أيضاً للتحكم الكامل
@admin.register(InteractiveMap)
class InteractiveMapAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'latitude', 'longitude', 'allow_student_drawing', 'allow_student_markers')
    list_filter = ('allow_student_drawing', 'allow_student_markers')
    search_fields = ('title', 'lesson__title')

@admin.register(StudentLessonProgress)
class StudentLessonProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'is_completed', 'completed_at')
    list_filter = ('is_completed', 'lesson__subject', 'lesson__level')
    search_fields = ('student__username', 'lesson__title')

@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'purchased_at')
    list_filter = ('course',)
    search_fields = ('user__username', 'course__title')

@admin.register(PaymentRequest)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'atlas_name', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('user__username', 'atlas_name')

@admin.register(HistoricalDocument)
class HistoricalDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'latitude', 'longitude', 'is_premium', 'created_at')
    list_filter = ('category', 'is_premium')
    search_fields = ('title', 'description', 'category')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'course_name', 'language', 'issue_date')
    list_filter = ('language', 'issue_date')
    search_fields = ('user__username', 'course_name', 'certificate_id')

@admin.register(HistoricalEvent)
class HistoricalEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'wilaya', 'date')
    list_filter = ('event_type', 'wilaya')
    search_fields = ('name', 'wilaya')

# نموذج البطاقات مع دعم التوليد التلقائي
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'is_used', 'session_id', 'created_at')
    list_filter = ('is_used',)
    search_fields = ('serial_number', 'session_id')
    actions = ['generate_cards_action']

    @admin.action(description="توليد 10 بطاقات تفعيل جديدة")
    def generate_cards_action(self, request, queryset):
        for _ in range(10):
            new_code = f"GM-{uuid.uuid4().hex[:12].upper()}"
            Card.objects.create(serial_number=new_code)
        self.message_user(request, "تمت إضافة 10 بطاقات جديدة بنجاح.")
        
@admin.register(PrepaidCard)
class PrepaidCardAdmin(admin.ModelAdmin):
    list_display = ('pin_code', 'duration_days', 'is_used', 'used_by')
    list_filter = ('is_used', 'duration_days')
    search_fields = ('pin_code',)
