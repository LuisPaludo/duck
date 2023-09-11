"""
Django settings for duck project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from decouple import config
from datetime import timedelta

import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_cleanup.apps.CleanupConfig",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "dj_rest_auth",
    "storages",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
    "corsheaders",
    "drf_yasg",
    
    "locations",
    "user_data",
    "prize",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "duck.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "duck.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT', default='5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": config("AUTH_PASSWORD_VALIDATORS_1"),
    },
    {
        "NAME": config("AUTH_PASSWORD_VALIDATORS_2"),
    },
    {
        "NAME": config("AUTH_PASSWORD_VALIDATORS_3"),
    },
    {
        "NAME": config("AUTH_PASSWORD_VALIDATORS_4"),
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

USE_S3 = config('USE_S3', default=0, cast=bool)

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'utils.storages.StaticStorage'
    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'utils.storages.PublicMediaStorage'
else:
    STATIC_URL = '/staticfiles/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_URL = '/mediafiles/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Essa configuração define o caminho absoluto no sistema de arquivos onde os arquivos de mídia serão armazenados
# quando forem carregados pela aplicação.
# No seu caso, 'duck/assets' é o diretório onde os arquivos de mídia serão armazenados.
MEDIA_ROOT = "duck/assets"

# --------------------------------------------------------------------------------------------------------------------------------------#

# Novas configurações


# Essa configuração define o URL relativo usado para servir os arquivos de mídia. Quando um arquivo de mídia é carregado e
# armazenado em MEDIA_ROOT, o URL completo para esse arquivo será construído usando MEDIA_URL + o caminho do arquivo relativo ao MEDIA_ROOT.
# No seu caso, '/media/' é o URL relativo usado para servir arquivos de mídia. Isso significa que, quando você desejar acessar um arquivo de mídia,
# você usará URLs como http://seu_domain/media/seu_arquivo.jpg.
MEDIA_URL = "/media/"


# Define um novo modelo para o usuário padrão autenticado
# Modelo em user_data -> models.py -> CustomUser
AUTH_USER_MODEL = "user_data.CustomUser"

REST_FRAMEWORK = {
    # Essa opção define as classes de autenticação que serão aplicadas por padrão a todas as suas vistas da API REST.
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

# O SITE_ID é uma configuração do Django que indica qual site está sendo usado para a aplicação.
# Geralmente, em uma aplicação com um único site, o valor padrão é 1. Isso é importante para as bibliotecas
# django-allauth e dj-rest-auth para lidar com múltiplos sites caso você tenha mais de um site configurado.
SITE_ID = 1

# Essa seção de configuração está relacionada à biblioteca dj-rest-auth, que fornece endpoints de autenticação RESTful e
# é construída sobre o django-allauth, que lida com autenticação e autorização em Django.
REST_AUTH = {
    # USE_JWT: Essa opção indica se a autenticação JWT (JSON Web Token) deve ser usada ou não. Quando configurada como True,
    # a autenticação JWT será ativada.
    "USE_JWT": True,
    # Essa opção controla se o token JWT deve ser definido como um cookie HTTPOnly no cabeçalho da resposta.
    # A opção False permite que o token JWT seja acessado por JavaScript (o que pode ser útil em algumas situações),
    # enquanto True impede que o JavaScript acesse o token, aumentando a segurança.
    "JWT_AUTH_HTTPONLY": False,
    # Estas opções definem os caminhos para os serializers personalizados usados para processar os dados do usuário durante o registro e
    # para exibir os detalhes do usuário, respectivamente.
    "REGISTER_SERIALIZER": "user_data.api.serializers.CustomRegisterSerializer",
    "USER_DETAILS_SERIALIZER": "user_data.api.serializers.CustomUserSerializer",
}

#  Define a duração da validade do token de acesso
ACCESS_TOKEN_LIFETIME = config("ACCESS_TOKEN_LIFETIME", default=5, cast=int)
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_TOKEN_LIFETIME),
}

# Define o mecanismo de backend para enviar e-mails
EMAIL_BACKEND = config("EMAIL_BACKEND")
# O host para usar ao enviar e-mails.
EMAIL_HOST = config("EMAIL_HOST")
# A porta para usar ao enviar e-mails. Normalmente é 587 para conexões TLS ou 465 para SSL.
EMAIL_PORT = config("EMAIL_PORT")
# Uma variável booleana que determina se deve ser usada uma conexão TLS segura ao conectar ao servidor SMTP
EMAIL_USE_TLS = config("EMAIL_USE_TLS")
#  A conta de e-mail que será usada para enviar os e-mails.
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
# A senha da conta de e-mail.
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

# Determina se o e-mail é um campo obrigatório durante o registro.
ACCOUNT_EMAIL_REQUIRED = True
# Como os e-mails de verificação são tratados mandatory" exige que o usuário verifique seu e-mail.
# Se True, a confirmação de e-mail acontecerá quando o usuário acessar o link de confirmação, sem a necessidade de um POST adicional.
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

#  Path para uma classe customizada que adapta ou estende a funcionalidade do allauth.
ACCOUNT_ADAPTER = "user_data.api.adapter.CustomAccountAdapter"
# O endereço URL do frontend. Útil para redirecionar ou criar URLs em e-mails, por exemplo.
URL_FRONTEND = config("URL_FRONTEND", default="http://localhost:4200")

# Se True, todas as origens estarão autorizadas. Isso pode ser perigoso em produção,
# pois permite que qualquer site faça solicitações à sua API.
CORS_ALLOW_ALL_ORIGINS = True
# Se True, os cookies também serão compartilhados em solicitações de origem cruzada.
CORS_ALLOW_CREDENTIALS = True

# Uma lista dos URLs que estão autorizados a fazer solicitações
# de origem cruzada para sua API.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:4200",
    "https://luispaludo.github.io",
]

# Define o método de autenticação. Aqui, está configurado para usar e-mail em vez de nome de usuário.
ACCOUNT_AUTHENTICATION_METHOD = "email"
# Se False, o nome de usuário não é obrigatório durante o registro.
ACCOUNT_USERNAME_REQUIRED = False

# Following is added to enable registration with email instead of username
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

CSRF_TRUSTED_ORIGINS = [
    'https://web-production-1c42.up.railway.app'
]