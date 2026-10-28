from django.contrib import admin
from .models import Flag, PathStep

# إضافة الخطوات داخل صفحة العلم لتسهيل الإدخال
class PathStepInline(admin.TabularInline):
    model = PathStep
    extra = 1  # عدد الخانات الفارغة المضافة تلقائياً
    fields = ('order', 'title', 'latitude', 'longitude', 'description', 'image')

@admin.register(Flag)
class FlagAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date', 'is_ready')
    list_editable = ('is_ready',)
    search_fields = ('full_name', 'biography')
    prepopulated_fields = {'slug': ('full_name',)}
    inlines = [PathStepInline]
    
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('full_name', 'biography', 'birth_date', 'slug', 'is_ready')
        }),
        ('الموقع الجغرافي', {
            'fields': ('latitude', 'longitude')
        }),
        ('الوسائط', {
            'fields': ('image',), 
            'description': "قم برفع صورة العلم مباشرة من جهازك، وسيتم حفظها وعرضها تلقائياً."
        }),
    )

# تسجيل نموذج الخطوات بشكل منفصل أيضاً (اختياري)
@admin.register(PathStep)
class PathStepAdmin(admin.ModelAdmin):
    list_display = ('title', 'flag', 'order')
    list_filter = ('flag',)
    search_fields = ('title', 'description')