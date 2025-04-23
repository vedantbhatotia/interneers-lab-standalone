import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from mongoengine import connect

BASE_DIR = Path(__file__).resolve().parent.parent

print(f"📂 Loading environment from: {os.path.join(BASE_DIR, '.env')}") 
load_dotenv(os.path.join(BASE_DIR, ".env"))

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "product",
    "rest_framework",
    "django_filters",
    "corsheaders",  
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  
    "django.middleware.common.CommonMiddleware",  
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",  
    "http://localhost:5500",  
]

ROOT_URLCONF = "django_app.urls"

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

WSGI_APPLICATION = "django_app.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": BASE_DIR / os.getenv("DB_NAME", "db.sqlite3"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
TEST_MONGO_DB_NAME = os.getenv("TEST_MONGO_DB_NAME", "interneers_lab_test")

try:
    IS_TESTING = "pytest" in os.path.basename(sys.argv[0]) or "test" in sys.argv
    print(" MongoDB Connection Settings:")
    print(f" IS_TESTING = {IS_TESTING}")
    print(f" MONGO_DB_NAME = {MONGO_DB_NAME}")
    print(f" TEST_MONGO_DB_NAME = {TEST_MONGO_DB_NAME}")
    print(f" HOST = {MONGO_HOST}:{MONGO_PORT}")
    print(f" USER = {MONGO_USER}")
    print(f" sys.argv = {sys.argv}")

    if IS_TESTING:
        print(" Connecting to TEST MongoDB...")
        connect(
            db=TEST_MONGO_DB_NAME,
            host=f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin",
            alias="default",
            uuidRepresentation="standard"
        )
        print(" Connected to TEST MongoDB")
    else:
        print("Connecting to PROD MongoDB...")
        connect(
            db=MONGO_DB_NAME,
            host=f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin",
            alias="default",
            uuidRepresentation="standard"
        )
        print(" Connected to PROD MongoDB")

except Exception as e:
    print(" MongoDB connection failed!")
    print(f"Error: {e}")
