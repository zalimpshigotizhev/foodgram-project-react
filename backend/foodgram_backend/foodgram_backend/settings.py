from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split()

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS').split()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    'djoser',
    'users.apps.UsersConfig',
    'api.apps.ApiConfig',
    'recipes.apps.RecipesConfig',
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

ROOT_URLCONF = 'foodgram_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'foodgram_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('POSTGRES_DB', 'django'),
#         'USER': os.getenv('POSTGRES_USER', 'django'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
#         'HOST': os.getenv('DB_HOST', ''),
#         'PORT': os.getenv('DB_PORT', 5432)
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / MEDIA_URL

LANGUAGE_CODE = "ru"


TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'users.CustomUser'

STATIC_URL = '/backend_static/'
STATIC_ROOT = BASE_DIR / 'static'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
DJOSER = {
    "LOGIN_FIELD": "email",
    "HIDE_USERS": False,
    "PERMISSIONS": {
        "resipe": ("api.permissions.AuthorStaffOrReadOnly,",),
        "recipe_list": ("api.permissions.AuthorStaffOrReadOnly",),
        "user": ("api.permissions.OwnerUserOrReadOnly",),
        "user_list": ("api.permissions.OwnerUserOrReadOnly",),
    },
    "SERIALIZERS": {
        "user": "api.serializers.CustomUserSerializer",
        "user_list": "api.serializers.CustomUserSerializer",
        "current_user": "api.serializers.CustomUserSerializer",
        "user_create": "api.serializers.CustomUserSerializer",
    },
}
