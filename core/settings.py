"""
Django settings for core project.
"""

from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env(
    DJANGO_DEBUG=(bool, True),
    DJANGO_ALLOWED_HOSTS=(list, ["*"]),
    DB_ENGINE=(str, "local"),
    DB_NAME=(str, ""),
    DB_USER=(str, ""),
    DB_PASSWORD=(str, ""),
    DB_HOST=(str, ""),
    DB_PORT=(str, "5432"),
    EMAIL_HOST_USER=(str, ""),
    EMAIL_HOST_PASSWORD=(str, ""),
)
environ.Env.read_env(BASE_DIR / ".env")

# ─────────────────────────────────────────────────────────────
#  SEGURIDAD
# ─────────────────────────────────────────────────────────────
SECRET_KEY = env(
    "SECRET_KEY",
    default=env(
        "DJANGO_SECRET_KEY",
        default="django-insecure-)1t4q$yd=#qejd0tu*58*n89e8i^(=)&*=5()7it#l0b997(w^",
    ),
)
DEBUG = env("DJANGO_DEBUG", default=env("DEBUG", default=True))
ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS", default=env.list("ALLOWED_HOSTS", default=["*"])
)


# ─────────────────────────────────────────────────────────────
#  APLICACIONES
# ─────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "devoluciones",
    "usuario",
    "prestamo",
    "inventario",
    "almacenamiento",
    "pagina_principal",
    "mantenimiento",
    "reportes",
    "configuracion",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates", BASE_DIR / "usuario" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# ─────────────────────────────────────────────────────────────
#  BASE DE DATOS
# ─────────────────────────────────────────────────────────────

db_engine = env("DB_ENGINE", default="local")

if db_engine == "nube":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT", default="5432"),
            "CONN_MAX_AGE": 300,
            "OPTIONS": {
                "sslmode": "require",
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ─────────────────────────────────────────────────────────────
#  VALIDACIÓN DE CONTRASEÑAS
# ─────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        )
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ─────────────────────────────────────────────────────────────
#  INTERNACIONALIZACIÓN
# ─────────────────────────────────────────────────────────────
LANGUAGE_CODE = "es-co"

TIME_ZONE = "America/Bogota"

USE_I18N = True
USE_TZ = True


# ─────────────────────────────────────────────────────────────
#  ARCHIVOS ESTÁTICOS Y MEDIA
# ─────────────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ─────────────────────────────────────────────────────────────
#  SESIONES
# ─────────────────────────────────────────────────────────────
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# ─────────────────────────────────────────────────────────────
#  REDIRECCIONES DE AUTH
# ─────────────────────────────────────────────────────────────
LOGIN_URL = "/"
LOGIN_REDIRECT_URL = "/home/"
LOGOUT_REDIRECT_URL = "/"


# ─────────────────────────────────────────────────────────────
#  CORREO
# ─────────────────────────────────────────────────────────────
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")

if EMAIL_HOST_USER:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "no-reply@mineinventory.com"


# ─────────────────────────────────────────────────────────────
#  CAMPO PK POR DEFECTO
# ─────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Permite que JS lea la cookie CSRF
CSRF_COOKIE_HTTPONLY = False

# Silencia el warning Cross-Origin-Opener-Policy en desarrollo HTTP
# (en producción con HTTPS esto no es necesario)
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
