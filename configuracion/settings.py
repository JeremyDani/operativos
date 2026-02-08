from pathlib        import Path
from datetime       import timedelta
from django.conf    import settings
from decouple       import config, Csv
import os

import datetime
import logging.config
import os


# Directorio base del proyecto (usado para construir rutas relativas)
BASE_DIR            = Path(__file__).resolve().parent.parent
# Clave secreta (leer desde .env). NO versionar valores reales.
SECRET_KEY          = config('SECRET_KEY')
# Flag de depuración; controlar en el entorno (True/False)
DEBUG               = config('DEBUG')
# Hosts permitidos para servir la app
ALLOWED_HOSTS   = ['localhost', '127.0.0.1', '0.0.0.0']

BASE_APPS   =   [
                    'jazzmin',
                    'django.contrib.admin',
                    'django.contrib.auth',
                    'django.contrib.contenttypes',
                    'django.contrib.sessions',
                    'django.contrib.messages',
                    'django.contrib.staticfiles',
                ]

LOCAL_APPS  =   [
                    'apps.cuenta',
                    'apps.frontend',
                    'apps.auxiliares',
                    'apps.operativos',
                    'apps.historico',
                ]

THIRD_APPS =    [
                    'corsheaders',
                    'ninja_extra',
                    'ninja_jwt',
                    'django_rest_passwordreset',
                    'simple_history',
                    #'import_export',
                    #'maintenance_mode',
                ]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS

# Lista combinada de apps instaladas: core de Django + apps locales + terceros

MIDDLEWARE      =   [
                        'django.middleware.security.SecurityMiddleware',
                        'django.contrib.sessions.middleware.SessionMiddleware',
                        # Incluida
                        "corsheaders.middleware.CorsMiddleware",
                        'django.middleware.common.CommonMiddleware',
                        'django.middleware.csrf.CsrfViewMiddleware',
                        'django.contrib.auth.middleware.AuthenticationMiddleware',
                        'django.contrib.messages.middleware.MessageMiddleware',
                        'django.middleware.clickjacking.XFrameOptionsMiddleware',
                        #'maintenance_mode.middleware.MaintenanceModeMiddleware',
                    ]

ROOT_URLCONF    =   'configuracion.urls'  # Módulo de rutas raíz del proyecto

TEMPLATES       =   [
                        {
                            'BACKEND'   :   'django.template.backends.django.DjangoTemplates',
                            'DIRS'      :   [os.path.join(BASE_DIR, 'templates')],
                            'APP_DIRS'  :   True,
                            'OPTIONS'   :   {
                                                'context_processors': 
                                                [
                                                    'django.template.context_processors.debug',
                                                    'django.template.context_processors.request',
                                                    'django.contrib.auth.context_processors.auth',
                                                    'django.contrib.messages.context_processors.messages',
                                                ],
                                            },
                        },
                    ]

WSGI_APPLICATION = 'configuracion.wsgi.application'  # Entrada WSGI para servidores de producción


DATABASES = {
                'default' :     {
                                    'ENGINE':           'django.db.backends.postgresql',
                                    'NAME':             config('BD_PRINCIPAL'),
                                    'USER':             config('USUARIO_DESARROLLO'),
                                    'PASSWORD':         config('CLAVE_DESARROLLO'),
                                    'HOST':             config('IP_DESARROLLO'),
                                    'PORT':             config('PUERTO_PREDETERMINADO'),
                                    #"ATOMIC_REQUESTS":  config('ATOMIC_REQUESTS'),
                                    # PARA LEER CON InspectDB un esquema especifico
                                    #'OPTIONS': {'options': '-c search_path=operativos'}
                                },
            }

AUTH_USER_MODEL             = 'cuenta.User'
AUTH_PASSWORD_VALIDATORS =  [
                                { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',   },
                                { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',             },
                                { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',            },
                                { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',           },
                            ]


LANGUAGE_CODE       = 'es-ve'
TIME_ZONE           = 'America/Caracas'
USE_I18N            = True
USE_TZ              = True
DEFAULT_AUTO_FIELD  = 'django.db.models.BigAutoField'

STATIC_URL          = 'static/'
STATICFILES_DIRS    = [os.path.join(BASE_DIR, 'static/'),]
STATIC_ROOT         = os.path.join(BASE_DIR, 'staticfiles/')
MEDIA_ROOT          = os.path.join(BASE_DIR, 'media/')
MEDIA_URL           = '/media/'










# En desarrollo usar orígenes explícitos cuando `withCredentials` está activado.
# No usar wildcard '*' junto con credenciales.
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
# Permitir que Django incluya cookies de sesión en respuestas CORS
CORS_ALLOW_CREDENTIALS = True
AUTH_USER_MODEL     = 'cuenta.User'

DATABASE_ROUTERS    =   (
                            #'conexiones.nomina_mppe.PersonalMPPE_DBRouter',
                            #'conexiones.nomina_entes.PersonalEnte_DBRouter',
                            
                            #'conexiones.geo_estado.Estado_DBRouter',
                            #'conexiones.geo_municipio.Municipio_DBRouter',
                            #'conexiones.geo_parroquia.Parroquia_DBRouter',
                            #'conexiones.geo_comunidad.Comunidad_DBRouter',

                            #'conexiones.gescolar_plantel.Plantel_DBRouter',

                            #'conexiones.saime.Saime_DBRouter',
                        )

# Logging Configuration

# Clear prev config
LOGGING_CONFIG = None

# Get log_level from env
LOG_LEVEL = os.getenv("DJANGO_LOG_LEVEL", "info").upper()

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters":   {
                            "console":  {
                                            "format": "%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %("
                                            "message)s",
                                        },
                        },
        "handlers":     {
                            "console": 
                                        {
                                            "class": "logging.StreamHandler",
                                            "formatter": "console",
                                        },
                        },
        "loggers":      {
                            "":         {
                                            "level": LOG_LEVEL,
                                            "handlers": ["console",],
                                        },
                        },
    }
)

# Configuracion del SWagger
SWAGGER_SETTINGS =  {
                        "USE_SESSION_AUTH": False,
                        "api_version":      "0.1",
                        "SECURITY_DEFINITIONS": {"api_key": {"type": "apiKey", "name": "Authorization", "in": "header"},},
                    }

# Configuracion de CELERY
REDIS_URL                       =   os.getenv("BROKER_URL", "redis://localhost:6379")
CELERY_BROKER_URL               =   REDIS_URL
CELERY_BROKER_TRANSPORT_OPTIONS =   {
                                        "visibility_timeout": 3600,  # 1 hour
                                    }
CELERY_ACCEPT_CONTENT           =   ["application/json"]
CELERY_TASK_SERIALIZER          =   "json"
CELERY_RESULT_SERIALIZER        =   "json"
CELERY_TIMEZONE                 =   TIME_ZONE


#NINJA_JWT                       = {'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA': 'apps.cuenta.views.token.MyTokenObtainPairInputSchema',}
# Configuracion del uso de JWT
NINJA_JWT                       =   {
                                        'ACCESS_TOKEN_LIFETIME':    timedelta(minutes=5),
                                        'REFRESH_TOKEN_LIFETIME':   timedelta(days=1),
                                        'ROTATE_REFRESH_TOKENS':    False,
                                        'BLACKLIST_AFTER_ROTATION': False,
                                        'UPDATE_LAST_LOGIN':        False,

                                        'ALGORITHM':                'HS256',
                                        'SIGNING_KEY':              config('SECRET_KEY'),
                                        'VERIFYING_KEY':            None,
                                        'AUDIENCE':                 None,
                                        'ISSUER':                   None,
                                        'JWK_URL':                  None,
                                        'LEEWAY':                   0,

                                        'USER_ID_FIELD':            'id',
                                        'USER_ID_CLAIM':            'user_id',
                                        'USER_AUTHENTICATION_RULE': 'ninja_jwt.authentication.default_user_authentication_rule',

                                        'AUTH_TOKEN_CLASSES':       ('ninja_jwt.tokens.AccessToken',),
                                        'TOKEN_TYPE_CLAIM':         'token_type',
                                        'TOKEN_USER_CLASS':         'ninja_jwt.models.TokenUser',

                                        'JTI_CLAIM':                        'jti',

                                        'SLIDING_TOKEN_REFRESH_EXP_CLAIM':  'refresh_exp',
                                        'SLIDING_TOKEN_LIFETIME':           timedelta(minutes=5),
                                        'SLIDING_TOKEN_REFRESH_LIFETIME':   timedelta(days=1),

                                        # For Controller Schemas
                                        # FOR OBTAIN PAIR
                                        'TOKEN_OBTAIN_PAIR_INPUT_SCHEMA':           "ninja_jwt.schema.TokenObtainPairInputSchema",
                                        'TOKEN_OBTAIN_PAIR_REFRESH_INPUT_SCHEMA':   "ninja_jwt.schema.TokenRefreshInputSchema",
                                        # FOR SLIDING TOKEN
                                        'TOKEN_OBTAIN_SLIDING_INPUT_SCHEMA':        "ninja_jwt.schema.TokenObtainSlidingInputSchema",
                                        'TOKEN_OBTAIN_SLIDING_REFRESH_INPUT_SCHEMA':"ninja_jwt.schema.TokenRefreshSlidingInputSchema",

                                        'TOKEN_BLACKLIST_INPUT_SCHEMA':             "ninja_jwt.schema.TokenBlacklistInputSchema",
                                        'TOKEN_VERIFY_INPUT_SCHEMA':                "ninja_jwt.schema.TokenVerifyInputSchema",
                                    }


JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "SGI-Operativos",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "SGI-Operativos",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "SGI-Operativos",

    # Welcome text on the login screen
    "welcome_sign": "Bienvenido a SGI-Operativos",

    # Copyright on the footer
    "copyright": "SGI-Operativos MPPE",

    "order_with_respect_to": ["auth", "cuenta", "operativos", "historico", "auxiliares"],

    "apps": {
        "auth": {
            "name": "Autenticación",
            "icon": "fas fa-users-cog",
        },
        "cuenta": {
            "name": "Cuentas de Usuario",
            "icon": "fas fa-user",
        },
        "operativos": {
            "name": "Operativos",
            "icon": "fas fa-box",
        },
        "historico": {
            "name": "Histórico",
            "icon": "fas fa-history",
            "models": {
                "historico.registrooperativo": {
                    "label": "Registros de Operativos",
                    "icon": "fas fa-list-alt",
                }
            }
        },
        "auxiliares": {
            "name": "Datos Auxiliares",
            "icon": "fas fa-cogs",
        },
    },

    "icons": {
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
}
