import json
from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers.json import DjangoJSONEncoder
from .models import Flag

def flags_list(request):
    # إظهار الأعلام الجاهزة فقط أو كل الأعلام (يمكنك تغيير الفلتر)
    flags = Flag.objects.all()
    return render(request, 'flags_list.html', {'flags': flags})

def map_view(request):
    figure_slug = request.GET.get('figure')
    
    if not figure_slug:
        return redirect('dakira_haya:flags_list')
        
    flag = get_object_or_404(Flag, slug=figure_slug)
    
    if not flag.is_ready:
        return redirect('dakira_haya:flags_list')

    # تجهيز البيانات
    science_data = {
        "title": flag.full_name,
        # هنا التعديل: ندمج المسار يدوياً مع اسم الملف المخزن في قاعدة البيانات
        "bg_card": flag.image.url if flag.image else "",
        "animation_steps": [
            {
                "name": step.title,
                "coords": [step.longitude, step.latitude],
                "action": step.description,
                "image": step.image.url if step.image else ""
            }
            for step in flag.steps.all()
        ]
    }
    
    return render(request, 'map.html', {
        'flag': flag,
        'science_data_json': json.dumps(science_data, cls=DjangoJSONEncoder)
    })
    
def flag_detail(request, slug):
    flag = get_object_or_404(Flag, slug=slug)
    return render(request, 'dakira_haya/detail.html', {'flag': flag})
