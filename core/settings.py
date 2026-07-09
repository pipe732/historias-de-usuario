"""
Django settings for core project.
"""

from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ─────────────────────────────────────────────────────────────
#  LEER .ENV PARA VARIABLES DE ENTORNO
# ─────────────────────────────────────────────────────────────
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / ".env")


# ─────────────────────────────────────────────────────────────
#  SEGURIDAD
# ─────────────────────────────────────────────────────────────
SECRET_KEY = env("DJANGO_SECRET_KEY")  # sin default → truena si falta. Correcto.
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost"])


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
db_engine = env("DB_ENGINE", default="nube")

DATABASES = {
    "neon_db": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT", default="5432"),
        "CONN_MAX_AGE": 300,
        "OPTIONS": {
            "sslmode": "require",
            "channel_binding": "require",
        },
    },
    "local_db": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

# Asignar la base de datos default según el .env
DATABASES["default"] = DATABASES["local_db"] if db_engine == "local" else DATABASES["neon_db"]


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
LANGUAGE_CODE = "es-co"  # ✅ cambiado a español Colombia

TIME_ZONE = "America/Bogota"  # ✅ zona horaria correcta

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
SESSION_COOKIE_AGE = 3600  # sesión expira en 1 hora (segundos)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # cierra sesión al cerrar el navegador


# ─────────────────────────────────────────────────────────────
#  REDIRECCIONES DE AUTH
# ─────────────────────────────────────────────────────────────
LOGIN_URL = "/"  # si no está logueado, va al login (ruta raíz)
LOGIN_REDIRECT_URL = "/home/"  # después de login exitoso, va a home
LOGOUT_REDIRECT_URL = "/"  # después de logout, vuelve al login


# ─────────────────────────────────────────────────────────────
#  CORREO
# ─────────────────────────────────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# ─────────────────────────────────────────────────────────────
#  CAMPO PK POR DEFECTO
# ─────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Permite que JS lea la cookie CSRF (necesario para peticiones AJAX con token CSRF)
CSRF_COOKIE_HTTPONLY = False

# Silencia el warning Cross-Origin-Opener-Policy en desarrollo HTTP
# (en producción con HTTPS esto no es necesario)
SECURE_CROSS_ORIGIN_OPENER_POLICY = None