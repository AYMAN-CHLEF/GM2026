from django.shortcuts import get_object_or_404, render
from django.utils.translation import get_language
from .models import Monument

def monument_tech_card(request, slug):
    monument = get_object_or_404(Monument, slug=slug)
    
    # استقبال اللغة من المتصفح أو الرابط (افتراضياً العربية)
    lang = request.GET.get('lang', get_language())
    if lang not in ['ar', 'fr', 'en', 'tr', 'es']:
        lang = 'ar'
    
    # اختيار النصوص بناءً على لغة السائح
    if lang == 'fr':
        name = monument.name_fr
        description = monument.description_fr
        ui_texts = {
            "view_drone": "Vue aérienne (Drone)",
            "overview": "Aperçu historique et architectural",
            "navigate": "Y aller (Google Maps)",
            "scan_hint": "Scannez le QR Code pour guide audio/vidéo",
            "brand": "Guide Touristique Intelligent"
        }
    elif lang == 'en':
        name = monument.name_en
        description = monument.description_en
        ui_texts = {
            "view_drone": "Drone Aerial View",
            "overview": "Historical & Architectural Overview",
            "navigate": "Get Directions (Google Maps)",
            "scan_hint": "Scan QR Code for interactive guide",
            "brand": "Smart Tourist Guide"
        }
    elif lang == 'tr':
        name = monument.name_en
        description = monument.description_en
        ui_texts = {
            "view_drone": "Drone hava görüntüsü",
            "overview": "Tarihî ve mimari genel bakış",
            "navigate": "Yol tarifi al (Google Maps)",
            "scan_hint": "Etkileşimli rehber için QR kodunu tarayın",
            "brand": "Akıllı Turist Rehberi"
        }
    elif lang == 'es':
        name = monument.name_en
        description = monument.description_en
        ui_texts = {
            "view_drone": "Vista aérea con dron",
            "overview": "Resumen histórico y arquitectónico",
            "navigate": "Cómo llegar (Google Maps)",
            "scan_hint": "Escanea el código QR para abrir la guía interactiva",
            "brand": "Guía turística inteligente"
        }
    else:
        name = monument.name_ar
        description = monument.description_ar
        ui_texts = {
            "view_drone": "نظرة جوية بالدرون (Drone View)",
            "overview": "نبذة تاريخية ومعمارية",
            "navigate": "الانتقال إلى الموقع (Google Maps)",
            "scan_hint": "امسح الرمز لاستكشاف المعلم",
            "brand": "دليلك السياحي الذكي"
        }
        
    context = {
        'monument': monument,
        'name': name,
        'description': description,
        'current_lang': lang,
        'ui_texts': ui_texts,
    }
    return render(request, 'monuments/tech_card.html', context)
