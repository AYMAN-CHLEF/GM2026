from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.db import transaction
from django.contrib.sites.shortcuts import get_current_site
import qrcode, base64
from io import BytesIO

from core.views.auth_views import get_user_context
from core.models import Card, Certificate, HistoricalDocument, PaymentRequest, HistoricalGeographicContent, UserProfile
from core.forms import PaymentReceiptForm

ALLOWED_ATLAS_CODES = {
    'resistance', 'intellectual', 'battles', 'barriers', 'leadership',
    'ancient-states', 'islamic-dynasties', 'regency',
}

def home_view(request):
    latest_content = HistoricalGeographicContent.objects.all().order_by('-created_at')[:3]
    return render(request, 'home.html', {'latest_content': latest_content})

def atlases_view(request):
    context = get_user_context(request.user) if request.user.is_authenticated else {}
    return render(request, 'atlases.html', context)

def museum_view(request):
    context = get_user_context(request.user) if request.user.is_authenticated else {}
    return render(request, 'digital_museum.html', context)

def library_view(request):
    context = get_user_context(request.user) if request.user.is_authenticated else {}
    return render(request, 'library.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def payment_view(request):
    atlas_id = (request.POST.get('atlas_id') if request.method == 'POST' else request.GET.get('atlas', '')).strip()
    if atlas_id not in ALLOWED_ATLAS_CODES:
        messages.error(request, 'الأطلس المختار غير صالح.')
        return redirect('atlases')
    form = PaymentReceiptForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            PaymentRequest.objects.create(
                user=request.user,
                atlas_name=atlas_id,
                cpc_receipt=form.cleaned_data['cpc_image'],
            )
            return render(request, 'success.html', {
                'msg': f'تم استلام طلبك للأطلس رقم: {atlas_id}. سيتم التفعيل بعد المراجعة.'
            })
    return render(request, 'payment.html', {'atlas_id': atlas_id, 'form': form})

def show_atlas(request):
    return render(request, 'atlas_revolution.html')

def document_detail(request, doc_id):
    doc = get_object_or_404(HistoricalDocument, id=doc_id)
    if doc.is_premium and not request.user.is_authenticated:
        return render(request, 'subscribe_page.html')
    return render(request, 'document_view.html', {'doc': doc})


def verify_certificate(request, certificate_id):
    certificate = get_object_or_404(
        Certificate.objects.select_related('user', 'course'), certificate_id=certificate_id
    )
    return render(request, 'student/verify_certificate.html', {'certificate': certificate})

@require_http_methods(['GET', 'POST'])
def activate_game(request):
    serial_from_url = request.GET.get('code', '')
    if request.method == 'POST':
        import hashlib
        remote_addr = request.META.get('REMOTE_ADDR', '')
        throttle_key = 'game-card-attempts:' + hashlib.sha256(remote_addr.encode()).hexdigest()
        if cache.get(throttle_key, 0) >= 10:
            messages.error(request, 'تجاوزت عدد المحاولات المسموح. حاول مجدداً بعد 15 دقيقة.')
            response = render(request, 'activate_game.html', {'serial_code': ''})
            response.status_code = 429
            return response
        serial_code = request.POST.get('serial_code', '').strip()[:100]
        with transaction.atomic():
            card = Card.objects.select_for_update().filter(serial_number=serial_code).first() if serial_code else None
            if card and not card.is_used:
                claimed = Card.objects.filter(pk=card.pk, is_used=False).update(is_used=True)
                if claimed:
                    request.session['active_card'] = serial_code
                    cache.delete(throttle_key)
                    messages.success(request, 'تم التفعيل بنجاح!')
                    return redirect('game_main')
            elif card and request.session.get('active_card') == serial_code:
                return redirect('game_main')
        cache.add(throttle_key, 0, timeout=15 * 60)
        try:
            cache.incr(throttle_key)
        except ValueError:
            cache.set(throttle_key, 1, timeout=15 * 60)
        messages.error(request, 'تعذر تفعيل البطاقة. تحقق من الرمز أو تواصل مع الدعم.')
    return render(request, 'activate_game.html', {'serial_code': serial_from_url})

def game_main(request):
    serial_code = request.session.get('active_card')
    if not serial_code:
        return redirect('activate_game')
    puzzle = {
        'question': "في أي دولة تقع مدينة 'تيمقاد' الأثرية التي تعود للعصر الروماني؟",
        'options': ['تونس', 'الجزائر', 'المغرب', 'مصر'],
        'correct': 'الجزائر'
    }
    return render(request, 'game_main.html', {'serial_code': serial_code, 'puzzle': puzzle})

@staff_member_required
def print_keys(request):
    current_site = get_current_site(request)
    keys_with_qr = []
    cards = Card.objects.all()
    for card in cards:
        qr_data = f"https://{current_site.domain}/activate/?code={card.serial_number}"
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        keys_with_qr.append({'serial': card.serial_number, 'qr': base64.b64encode(buffer.getvalue()).decode()})
    return render(request, 'print_cards.html', {'keys': keys_with_qr})
