import os
import settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '8yk!%k+hx)*e=sp6-pr%nc+z=s-ve^23%p)^(_c1p6apje7=c@'

DEBUG = True

ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'customuser.User'

EMAIL_HOST = settings.SMTP_HOST
EMAIL_HOST_USER = settings.SMTP_LOGIN
EMAIL_HOST_PASSWORD = settings.SMTP_PASSWORD
EMAIL_PORT = settings.SMTP_PORT
EMAIL_USE_TLS = True

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"

SOCIAL_AUTH_VK_OAUTH2_KEY = settings.VK_CLIENT_ID
SOCIAL_AUTH_VK_OAUTH2_SECRET = settings.VK_CLIENT_SECRET

LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']

INSTALLED_APPS = [
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'ckeditor',
    'customuser.apps.CustomuserConfig',
    'staticPage.apps.StaticpageConfig',
    'partner.apps.PartnerConfig',
    'tariff.apps.TariffConfig',
    'technique.apps.TechniqueConfig',
    'chat.apps.ChatConfig',
    'techniqueOrder.apps.TechniqueorderConfig',
    'ya_payment.apps.YaPaymentConfig',
    'feedback.apps.FeedbackConfig'
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend'
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'staticPage.middleware.check_domain.MyMiddleware'
]

ROOT_URLCONF = 'pandiga.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'technique.context_processors.get_technique',
                'customuser.context_processors.check_profile',
            ],
        },
    },
]

WSGI_APPLICATION = 'pandiga.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}




LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = False

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')