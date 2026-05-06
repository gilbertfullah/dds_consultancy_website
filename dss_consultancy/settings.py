from pathlib import Path
import dj_database_url
from decouple import config
from dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
import cloudinary_storage

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-cq4w*p30)2p%(jt!v)uvtqef6y3(xc@(q4t(yy=t_xv+@f@w!y'

# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', default=False)

port = int(os.environ.get('PORT', 8000))

ENV_ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS') or ""
ALLOWED_HOSTS = [
    'ddsconsultancy.org', 
    'www.ddsconsultancy.org', 
    '127.0.0.1', 
    'localhost',
    '.onrender.com'
]
if ENV_ALLOWED_HOSTS:
    ALLOWED_HOSTS.extend(ENV_ALLOWED_HOSTS.split(','))

# Application definition

INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'tailwind',
    'django_browser_reload',
    'cloudinary_storage',
    'cloudinary',
    'ckeditor',
    
    # Local apps
    'theme', # your tailwind theme app
    'core.apps.CoreConfig',
]

TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ["127.0.0.1"]
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # Should be near the top
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = 'dss_consultancy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dss_consultancy.wsgi.application'


# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'), # Use getenv for safety
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# ==============================================================================
# FILE STORAGE CONFIGURATION (FIXED)
# ==============================================================================

# Static files (CSS, JavaScript) are handled by WhiteNoise
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/' # This is a virtual URL; files are served from Cloudinary

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUD_NAME'),
    'API_KEY': os.getenv('API_KEY'),
    'API_SECRET': os.getenv('API_SECRET'),
}

cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET'),
    secure=True
)

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    "default": {
        "skin": "moono",
        "toolbar": "full",
        'height': 300,
        'width': '100%',
        "extraPlugins": ",".join(
            [
                'about',
                'filetools',
                'find',
                'iframe',
                'image',
                'image2',
                'link',
                'smiley',
                'table',
                'tabletools',
                'uploadimage',
                'widget',
                'dialog',
            ]
        ),
    }
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Or your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'DDS <noreply@ddsconsultancy.org>')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'info@ddsconsultancy.org')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# UNFOLD ADMIN CONFIGURATION
# ==============================================================================
UNFOLD = {
    "THEME": "light",
    "SITE_TITLE": "DDS Admin",
    "SITE_HEADER": "DDS Research & Consultancy",
    "SITE_URL": "/",
    "COLORS": {
        "primary": {
            "50": "oklch(97% .02 250)",
            "100": "oklch(93.2% .032 254)",
            "200": "oklch(88.2% .059 254)",
            "300": "oklch(80.9% .105 251)",
            "400": "oklch(70.7% .165 254)",
            "500": "oklch(62.3% .209 259)",
            "600": "oklch(54.6% .245 262)",
            "700": "oklch(48.8% .243 264)",
            "800": "oklch(42.4% .199 265)",
            "900": "oklch(37.9% .146 265)",
            "950": "oklch(28.2% .091 267)",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Content Management",
                "separator": True,
                "items": [
                    {
                        "title": "Projects",
                        "icon": "folder",
                        "link": "/admin/core/project/",
                    },
                    {
                        "title": "Services",
                        "icon": "work",
                        "link": "/admin/core/service/",
                    },
                    {
                        "title": "Blog Posts",
                        "icon": "article",
                        "link": "/admin/core/blogpost/",
                    },
                    {
                        "title": "News Posts",
                        "icon": "newspaper",
                        "link": "/admin/core/newspost/",
                    },
                    {
                        "title": "Publications",
                        "icon": "menu_book",
                        "link": "/admin/core/publication/",
                    },
                ],
            },
            {
                "title": "Organization",
                "separator": True,
                "items": [
                    {
                        "title": "Team Members",
                        "icon": "group",
                        "link": "/admin/core/teammember/",
                    },
                    {
                        "title": "Inquiries",
                        "icon": "mail",
                        "link": "/admin/core/contact/",
                    },
                ],
            },
            {
                "title": "System Access",
                "separator": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": "/admin/auth/user/",
                    },
                    {
                        "title": "Groups",
                        "icon": "group_work",
                        "link": "/admin/auth/group/",
                    },
                ],
            },
        ],
    },
    "SCRIPTS": [
        "/static/js/force_light.js",
    ],
    "STYLES": [
        "/static/css/admin_custom.css",
    ],
}

# Trigger reload
