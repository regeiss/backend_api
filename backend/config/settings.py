"""
Django settings for Cadastro Unificado API
"""
import os
from pathlib import Path
from datetime import timedelta
from decouple import config, Csv
import dj_database_url
from datetime import timedelta

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'rest_framework_simplejwt',
    'django_extensions',

    # Local apps
    'apps.cadastro',
    'apps.api',
    'authentication',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='postgresql://postgres:postgres@10.13.66.8:5432/dev_cadastro_unificado')
    )
}

# Configuração para não criar migrations das tabelas existentes
# Será configurado após inspectdb
class DatabaseRouter:
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'cadastro':
            return False  # Não criar migrations para models do banco existente
        return True

DATABASE_ROUTERS = ['config.settings.DatabaseRouter']

# Password validation
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
LANGUAGE_CODE = config('LANGUAGE_CODE', default='pt-br')
TIME_ZONE = config('TIME_ZONE', default='America/Sao_Paulo')
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
#CORS Configuration
CORS_ALLOWED_ORIGINS = config(
     'CORS_ALLOWED_ORIGINS',
     default='http://10.13.65.37:8001,http://10.13.65.37:8081',
     cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = True  # Apenas para desenvolvimento

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Spectacular Settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Cadastro Unificado API',
    'DESCRIPTION': 'Documentação da API de Cadastro Unificado',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,  # Não inclua o schema no endpoint principal /api/schema/
    # Prefixo para filtrar as rotas que aparecerão na documentação.
    # Se suas APIs estão em /api/v1/, use 'SCHEMA_PATH_PREFIX': '/api/v1/'
    'SCHEMA_PATH_PREFIX': '/api/v1/', # AJUSTE ESTE VALOR PARA O PREFIXO DA SUA API
    'APPEND_COMPONENTS': {
        # Exemplo: Se você tiver um serializador base que não é visível automaticamente
        # 'MyCustomSerializer': 'path.to.your.serializers.MyCustomSerializer',
    },

    # Configurações para servir os arquivos estáticos da UI (Swagger/Redoc)
    'SWAGGER_UI_DIST': 'SIDECAR', # Usa os arquivos do drf-spectacular-sidecar
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR', # Usa o favicon do sidecar
    'REDOC_DIST': 'SIDECAR', # Usa os arquivos do drf-spectacular-sidecar

    # Gerador de schema padrão (já está correto)
    'DEFAULT_GENERATOR_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # Permissões para acessar a documentação (ex: apenas usuários logados)
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'], # Ou 'rest_framework.permissions.IsAdminUser'

    # Configurações da UI do Swagger
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': False,
        'defaultModelRendering': 'example',
        'defaultModelExpandDepth': 1,
        'defaultModelsExpandDepth': 1,
        'displayRequestDuration': True,
        'docExpansion': 'none', # 'none', 'list', 'full'
        'filter': True, # Habilita o campo de filtro
        'showExtensions': True,
        'showCommonExtensions': True,
    },

    # Processamento do Schema
    'COMPONENT_SPLIT_REQUEST': True, # Separa request/response bodies em componentes
    'COMPONENT_SPLIT_PATCH': True, # Separa PATCH em um componente diferente
    'SORT_OPERATIONS': False, # Manter a ordem de definição das rotas
    'DISABLE_ERRORS_AND_WARNINGS': False, # Habilitar para depuração
    'SCHEMA_COERCE_PATH_PK': True, # Converte :pk para {id} em paths

    # Mapeamento de métodos (já está correto)
    'SCHEMA_COERCE_METHOD_NAMES': {
        'retrieve': 'get',
        'list': 'list',
        'create': 'create',
        'update': 'update',
        'partial_update': 'partial_update',
        'destroy': 'delete'
    },

    # Hooks (manter vazio a menos que você crie hooks personalizados)
    'POSTPROCESSING_HOOKS': [],
    'PREPROCESSING_HOOKS': [],

    # Autenticação (se você tem rotas que exigem auth para serem documentadas)
    # 'AUTHENTICATION_WHITELIST': ['drf_spectacular.authentication.TokenAuth'], # Exemplo
    'AUTHENTICATION_WHITELIST': [], # Deixar vazio se não for usar autenticação específica para o schema

    # Enum handling
    'ENUM_NAME_OVERRIDES': {},
    'GENERIC_ADDITIONAL_PROPERTIES': 'dict',
    'CAMELIZE_NAMES': False, # Não camelizar nomes de campos
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
       'LOCATION': config('REDIS_URL', default='redis://redis:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Email Configuration (opcional)
if config('EMAIL_HOST', default=''):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

# Logging para debug
