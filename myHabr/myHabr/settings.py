"""
Django settings for myHabr project.

Generated by 'django-admin startproject' using Django 3.2.14.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^ad&9_sasovwpi8f4gcl25n6cy)(8wq$3g8-qi+f7+q+zysk21'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp',
    'authapp',
    'faq',
    'blogapp',
    'adminapp',
    'profiles',
    'social_django',
    "ckeditor",
    "ckeditor_uploader",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myHabr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mainapp.context_processors.categories',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',

            ],
            'loaders': ['admin_tools.template_loaders.Loader',
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                        ]
        },
    },
]

WSGI_APPLICATION = 'myHabr.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_URL = '/static/'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
AUTH_USER_MODEL = 'authapp.MyHabrUser'
LOGIN_URL = '/auth/login'
LOGIN_REDIRECT_URL = '/'

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'dr0nx@yandex.ru  '
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True

AUTHENTICATION_BACKENDS = (
    'social_core.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_VK_OAUTH2_KEY = '51401064'
SOCIAL_AUTH_VK_OAUTH2_SECRET = '89SMzLUskdzszIbJFUle'
SOCIAL_AUTH_VK_OAUTH2_API_VERSION = '5.131'
SOCIAL_AUTH_VK_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']

CSRF_TRUSTED_ORIGINS = ['https://kibarium.ru']

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            {'name': 'clipboard', 'items': ['Undo', 'Redo']},
            {'name': 'styles', 'items': ['Format', 'Font', 'FontSize']},
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'RemoveFormat', 'CopyFormatting']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'align', 'items': ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote']},
            {'name': 'insert', 'items': ['Image', 'Table']},
            {'name': 'tools', 'items': ['Maximize']},
            {'name': 'editing', 'items': ['Scayt']}
        ],
        'customConfig': '',
        'disallowedContent': 'img{width,height,float}',
        'extraAllowedContent': 'img[width,height,align]',
        'extraPlugins': ','.join([
            'tableresize',
            'uploadimage',
            # 'easyimage',
            # 'uploadfile'
        ]),
        'height': 800,
        'bodyClass': 'document-editor',
        'format_tags': 'p;h1;h2;h3;pre',
        'removeDialogTabs': 'image:advanced;link:advanced',
        'stylesSet': [
            {'name': 'Marker', 'element': 'span', 'attributes': {'class': 'marker'}},
            {'name': 'Cited Work', 'element': 'cite'},
            {'name': 'Inline Quotation', 'element': 'q'},
            {
                'name': 'Special Container',
                'element': 'div',
                'styles': {
                    'padding': '5px 10px',
                    'background': '#eee',
                    'border': '1px solid #ccc'
                }
            },
            {
                'name': 'Compact table',
                'element': 'table',
                'attributes': {
                    'cellpadding': '5',
                    'cellspacing': '0',
                    'border': '1',
                    'bordercolor': '#ccc'
                },
                'styles': {
                    'border-collapse': 'collapse'
                }
            },
            {'name': 'Borderless Table', 'element': 'table',
             'styles': {'border-style': 'hidden', 'background-color': '#E6E6FA'}},
            {'name': 'Square Bulleted List', 'element': 'ul', 'styles': {'list-style-type': 'square'}}
        ],
    },
}
