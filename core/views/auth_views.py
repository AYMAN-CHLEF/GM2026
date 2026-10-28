import hashlib
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core import signing
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import get_language
from django.views.decorators.http import require_http_methods, require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction

from core.forms import GISRegisterForm, StudentRegisterForm
from core.models import UserProfile

logger = logging.getLogger(__name__)
EMAIL_TOKEN_SALT = 'core.email-verification.v1'
EMAIL_TOKEN_MAX_AGE = 60 * 60 * 24
LOGIN_FAILURE_LIMIT = 8
LOGIN_IP_FAILURE_LIMIT = 50
LOGIN_LOCK_SECONDS = 15 * 60
REGISTRATION_LIMIT = 5
REGISTRATION_WINDOW_SECONDS = 30 * 60
RESEND_LIMIT = 3
RESEND_WINDOW_SECONDS = 20 * 60
PASSWORD_RESET_LIMIT = 5
PASSWORD_RESET_WINDOW_SECONDS = 60 * 60


def _language_text(ar, fr, en, tr, es):
    language = (get_language() or 'ar').split('-')[0]
    return {'ar': ar, 'fr': fr, 'en': en, 'tr': tr, 'es': es}.get(language, ar)


def _send_verification_email(request, user):
    token = signing.dumps({'user_id': user.pk, 'email': user.email}, salt=EMAIL_TOKEN_SALT)
    verify_path = reverse('verify_email', kwargs={'token': token})
    verify_url = (
        f'https://{request.get_host()}{verify_path}'
        if settings.IS_PRODUCTION else request.build_absolute_uri(verify_path)
    )
    subject = _language_text(
        'تأكيد البريد الإلكتروني في Geo-Memory',
        'Confirmez votre adresse e-mail Geo-Memory',
        'Confirm your Geo-Memory email address',
        'Geo-Memory e-posta adresinizi doğrulayın',
        'Confirma tu correo electrónico de Geo-Memory',
    )
    body = _language_text(
        f'مرحباً {user.first_name or user.username}،\n\nأكد بريدك الإلكتروني لإكمال إنشاء حسابك:\n{verify_url}\n\nينتهي الرابط خلال 24 ساعة.',
        f"Bonjour {user.first_name or user.username},\n\nConfirmez votre adresse pour activer votre compte :\n{verify_url}\n\nCe lien expire dans 24 heures.",
        f"Hello {user.first_name or user.username},\n\nConfirm your email address to activate your account:\n{verify_url}\n\nThis link expires in 24 hours.",
        f"Merhaba {user.first_name or user.username},\n\nHesabınızı etkinleştirmek için e-posta adresinizi doğrulayın:\n{verify_url}\n\nBu bağlantının süresi 24 saat içinde dolar.",
        f"Hola {user.first_name or user.username},\n\nConfirma tu correo para activar la cuenta:\n{verify_url}\n\nEste enlace caduca en 24 horas.",
    )
    return send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)


def _create_account(request, form, user_type):
    if not form.is_valid():
        return None
    user = form.save(commit=False)
    user.is_active = False
    try:
        with transaction.atomic():
            user.save()
            UserProfile.objects.update_or_create(user=user, defaults={
                'user_type': user_type,
                'first_name_ar': user.first_name,
                'last_name_ar': user.last_name,
            })
    except IntegrityError:
        form.add_error('email', _language_text(
            'هذا البريد مسجل بالفعل. استخدم صفحة استرجاع كلمة المرور إن كان الحساب لك.',
            'Cette adresse est déjà utilisée. Utilisez la réinitialisation si le compte vous appartient.',
            'That email is already registered. Use password reset if the account is yours.',
            'Bu e-posta zaten kayıtlı. Hesap size aitse şifre sıfırlamayı kullanın.',
            'Ese correo ya está registrado. Si la cuenta es tuya, restablece la contraseña.',
        ))
        return render(request, 'register.html', {
            'form': form,
            'target_space': 'gis_training' if user_type == 'gis_trainee' else 'education',
        })
    try:
        _send_verification_email(request, user)
    except Exception:
        logger.exception('Could not send the account verification message.')
        messages.warning(request, _language_text(
            'تم إنشاء الحساب وهو غير مفعّل بعد. تعذر إرسال رسالة التأكيد حالياً؛ استخدم خيار إعادة الإرسال بعد ضبط البريد.',
            "Le compte a été créé mais reste inactif. L'e-mail de confirmation n'a pas pu être envoyé ; réessayez après configuration du service e-mail.",
            'Your account was created but remains inactive. The confirmation email could not be sent; retry after the email service is configured.',
            'Hesabınız oluşturuldu ancak etkin değil. Doğrulama e-postası gönderilemedi; e-posta hizmeti yapılandırıldıktan sonra yeniden deneyin.',
            'La cuenta se creó, pero sigue inactiva. No se pudo enviar el correo de confirmación; inténtalo de nuevo cuando el correo esté configurado.',
        ))
    else:
        messages.success(request, _language_text(
            'أرسلنا رابط تأكيد إلى بريدك الإلكتروني. افتحه لإكمال التسجيل.',
            'Un lien de confirmation a été envoyé à votre adresse e-mail.',
            'A confirmation link was sent to your email address.',
            'E-posta adresinize bir doğrulama bağlantısı gönderildi.',
            'Enviamos un enlace de confirmación a tu correo electrónico.',
        ))
    return redirect('verification_pending')


@require_http_methods(['GET', 'POST'])
def register_student(request):
    throttle_key = _login_throttle_key(request, 'registration')
    if request.method == 'POST' and cache.get(throttle_key, 0) >= REGISTRATION_LIMIT:
        response = render(request, 'register.html', {'form': StudentRegisterForm(), 'rate_limited': True})
        response.status_code = 429
        return response
    form = StudentRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        _increment_counter(throttle_key, REGISTRATION_WINDOW_SECONDS)
        chosen_space = request.POST.get('account_space', 'education')
        user_type = 'gis_trainee' if chosen_space == 'gis_training' else 'student'
        return _create_account(request, form, user_type)
    return render(request, 'register.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def register_gis(request):
    throttle_key = _login_throttle_key(request, 'registration')
    if request.method == 'POST' and cache.get(throttle_key, 0) >= REGISTRATION_LIMIT:
        response = render(request, 'register.html', {'form': GISRegisterForm(), 'target_space': 'gis_training', 'rate_limited': True})
        response.status_code = 429
        return response
    form = GISRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        _increment_counter(throttle_key, REGISTRATION_WINDOW_SECONDS)
        return _create_account(request, form, 'gis_trainee')
    return render(request, 'register.html', {'form': form, 'target_space': 'gis_training'})


@require_http_methods(['GET', 'POST'])
def verification_pending(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().casefold()
        resend_key = _login_throttle_key(request, f'resend:{email[:254]}')
        may_send = cache.get(resend_key, 0) < RESEND_LIMIT
        _increment_counter(resend_key, RESEND_WINDOW_SECONDS)
        from django.contrib.auth import get_user_model
        user = get_user_model().objects.filter(email__iexact=email, is_active=False).first() if may_send else None
        if user and email:
            try:
                _send_verification_email(request, user)
            except Exception:
                logger.exception('Could not resend the account verification message.')
        messages.info(request, _language_text(
            'إذا كان الحساب غير مفعّل، فستصلك رسالة جديدة قريباً.',
            "Si le compte existe et n'est pas activé, un nouvel e-mail sera envoyé.",
            'If the account exists and is inactive, a new email will be sent shortly.',
            'Hesap mevcut ve etkin değilse yeni bir e-posta gönderilecektir.',
            'Si la cuenta existe y está inactiva, recibirás un nuevo correo pronto.',
        ))
        return redirect('verification_pending')
    return render(request, 'registration/verification_pending.html')


@require_http_methods(['GET', 'POST'])
def verify_email(request, token):
    try:
        payload = signing.loads(token, salt=EMAIL_TOKEN_SALT, max_age=EMAIL_TOKEN_MAX_AGE)
        from django.contrib.auth import get_user_model
        user = get_user_model().objects.get(pk=payload['user_id'], email__iexact=payload['email'])
    except (signing.BadSignature, signing.SignatureExpired, KeyError, TypeError, ValueError, ObjectDoesNotExist):
        return render(request, 'registration/verify_email.html', {'valid_link': False})

    if request.method == 'POST':
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=['is_active'])
        messages.success(request, _language_text(
            'تم تأكيد بريدك. يمكنك تسجيل الدخول الآن.', 'Adresse confirmée. Vous pouvez vous connecter.',
            'Email confirmed. You can now sign in.', 'E-posta doğrulandı. Şimdi giriş yapabilirsiniz.',
            'Correo confirmado. Ya puedes iniciar sesión.',
        ))
        return redirect('login')
    return render(request, 'registration/verify_email.html', {'valid_link': True, 'token': token})


def _login_throttle_key(request, username):
    remote_addr = request.META.get('REMOTE_ADDR', '')
    digest = hashlib.sha256(f'{remote_addr}:{username.strip().casefold()}'.encode()).hexdigest()
    return f'auth:login-failures:{digest}'


def _increment_counter(key, timeout):
    if cache.add(key, 1, timeout=timeout):
        return 1
    try:
        return cache.incr(key)
    except ValueError:
        cache.set(key, 1, timeout=timeout)
        return 1


class SafePasswordResetView(auth_views.PasswordResetView):
    def post(self, request, *args, **kwargs):
        key = _login_throttle_key(request, 'password-reset')
        if cache.get(key, 0) >= PASSWORD_RESET_LIMIT:
            response = self.render_to_response(self.get_context_data(form=self.get_form(), rate_limited=True))
            response.status_code = 429
            return response
        _increment_counter(key, PASSWORD_RESET_WINDOW_SECONDS)
        return super().post(request, *args, **kwargs)


class LocalizedPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = _language_text(
            'البريد الإلكتروني', 'Adresse e-mail', 'Email address', 'E-posta adresi', 'Correo electrónico'
        )
        self.fields['email'].widget.attrs.update({'autocomplete': 'email', 'dir': 'ltr'})


class LocalizedSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].label = _language_text(
            'كلمة المرور الجديدة', 'Nouveau mot de passe', 'New password', 'Yeni şifre', 'Nueva contraseña'
        )
        self.fields['new_password2'].label = _language_text(
            'تأكيد كلمة المرور', 'Confirmer le mot de passe', 'Confirm password', 'Şifreyi doğrulayın', 'Confirmar contraseña'
        )


@require_http_methods(['GET', 'POST'])
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    username = request.POST.get('username', '') if request.method == 'POST' else ''
    throttle_key = _login_throttle_key(request, username)
    ip_key = _login_throttle_key(request, 'ip-wide-limit')
    if request.method == 'POST':
        attempts = cache.get(throttle_key, 0)
        if attempts >= LOGIN_FAILURE_LIMIT or cache.get(ip_key, 0) >= LOGIN_IP_FAILURE_LIMIT:
            response = render(request, 'login.html', {'form': form, 'login_throttled': True})
            response.status_code = 429
            return response
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            cache.delete(throttle_key)
            # نوع المساحة محفوظ عند التسجيل ولا يمكن تغييره من نموذج تسجيل الدخول.
            profile, _ = UserProfile.objects.get_or_create(user=user)
            return redirect('dashboard_router')
        _increment_counter(throttle_key, LOGIN_LOCK_SECONDS)
        _increment_counter(ip_key, LOGIN_LOCK_SECONDS)
    return render(request, 'login.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')


def dashboard_router(request):
    if not request.user.is_authenticated:
        return redirect('login')
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if profile.user_type == 'gis_trainee':
        return redirect('gis:dashboard')
    return redirect('student:student_dashboard')


def get_user_context(user):
    profile = getattr(user, 'userprofile', None)
    return {'profile': profile, 'user': user}
