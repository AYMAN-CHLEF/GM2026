import os
import secrets
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# اللغات المدعومة في المنصة
LANGUAGES = [
    ('ar', 'العربية'),
    ('fr', 'Français'),
    ('en', 'English'),
    ('tr', 'Türkçe'),
    ('es', 'Español'),
]

LANGUAGE_CODE = 'ar'  # اللغة الافتراضية

USE_I18N = True
USE_L10N = True
USE_TZ = True

# المسار الأساسي للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# إعدادات الأمان
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() in {'1', 'true', 'yes'}
IS_PRODUCTION = os.environ.get('DJANGO_ENV', '').lower() == 'production'
SECRET_KEY = os.environ.get('SECRET_KEY')
if IS_PRODUCTION and not SECRET_KEY:
    raise ImproperlyConfigured('Set a persistent SECRET_KEY before starting in production.')
SECRET_KEY = SECRET_KEY or secrets.token_urlsafe(64)
ALLOWED_HOSTS = [host.strip() for host in os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if host.strip()]
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',') if origin.strip()]
if os.environ.get('DJANGO_TRUST_X_FORWARDED_PROTO', '').lower() in {'1', 'true', 'yes'}:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# التطبيقات المثبتة (مصححة ومنسقة)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'core',
    'atlas_revolution',
    'dakira_haya',
    'map_module',
    'rest_framework',      # للتعامل مع الـ APIs
    'rest_framework.authtoken',
    'gecc_core', # التطبيق الجديد
    'monuments', # إضافة التطبيق الثانوي الجديد هنا

]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Africa/Algiers'
USE_I18N = True
USE_TZ = True

# إعدادات الملفات الثابتة (WhiteNoise)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# إعدادات الوسائط (Media) عبر Cloudinary
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
CLOUDINARY_CONFIGURED = all(os.getenv(name) for name in ('CLOUDINARY_CLOUD_NAME', 'CLOUDINARY_API_KEY', 'CLOUDINARY_API_SECRET'))
STORAGES = {
    'default': {'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage' if CLOUDINARY_CONFIGURED else 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
LOCALE_PATHS = [BASE_DIR / 'locale']

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET', ''),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# A shared Redis cache keeps login and API limits effective across workers.
# Local memory cache is used for a standalone development instance.
REDIS_URL = os.environ.get('REDIS_URL')
if IS_PRODUCTION and not REDIS_URL:
    raise ImproperlyConfigured('Set REDIS_URL in production so security throttles are shared across workers.')
if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL,
            'KEY_PREFIX': 'geo_memory',
            'TIMEOUT': 300,
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'geo-memory-auth-throttle',
            'TIMEOUT': 300,
        }
    }

REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    'booking_create': '5/hour',
    'auth_token': '10/hour',
    'public_ai': '60/hour',
    'public_map': '600/hour',
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Email delivery is replaceable through environment variables; local development
# prints confirmation/reset links to the console instead of requiring SMTP.
if IS_PRODUCTION and not os.environ.get('EMAIL_HOST'):
    raise ImproperlyConfigured('Set EMAIL_HOST in production so account verification and password recovery can work.')
EMAIL_BACKEND = os.environ.get(
    'DJANGO_EMAIL_BACKEND',
    'django.core.mail.backends.smtp.EmailBackend' if (IS_PRODUCTION or os.environ.get('EMAIL_HOST')) else
    'django.core.mail.backends.console.EmailBackend',
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', str(EMAIL_PORT != 465)).lower() in {'1', 'true', 'yes'}
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', str(EMAIL_PORT == 465)).lower() in {'1', 'true', 'yes'}
EMAIL_TIMEOUT = int(os.environ.get('EMAIL_TIMEOUT', '10'))
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'Geo-Memory <no-reply@geo-memory.local>')
if IS_PRODUCTION and not os.environ.get('DEFAULT_FROM_EMAIL'):
    raise ImproperlyConfigured('Set DEFAULT_FROM_EMAIL to a verified sender address in production.')
PASSWORD_RESET_TIMEOUT = 60 * 60

# Session and browser security defaults. Enable HTTPS redirect/HSTS explicitly
# after HTTPS is configured at the application server or reverse proxy.
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = os.environ.get('DJANGO_SECURE_COOKIES', str(IS_PRODUCTION)).lower() in {'1', 'true', 'yes'}
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', 'false').lower() in {'1', 'true', 'yes'}
SECURE_HSTS_SECONDS = int(os.environ.get('DJANGO_HSTS_SECONDS', '0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_HSTS_SECONDS > 0
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024
