# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import abspath, dirname, join
from secrets import token_hex

import dj_database_url

PROJECT_DIR = dirname(dirname(abspath(__file__)))
BASE_DIR = dirname(PROJECT_DIR)

SECRET_KEY = os.getenv("SECRET_KEY", token_hex(64))
DEBUG = os.getenv("DEBUG", "False") == "True"

THEME = os.getenv("THEME")
THEME_DIR = os.getenv("THEME_DIR")
if THEME_DIR:
    THEME_DIR = abspath(THEME_DIR)

if THEME and THEME_DIR:
    TEMPLATE_DIRS = [join(THEME_DIR, "templates"), join(PROJECT_DIR, "templates")]
    STATICFILES_DIRS = [join(THEME_DIR, "static"), join(PROJECT_DIR, "static")]
else:
    TEMPLATE_DIRS = [join(PROJECT_DIR, "templates")]
    STATICFILES_DIRS = [join(PROJECT_DIR, "static")]


ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
if os.getenv("ALLOWED_HOSTS"):
    ALLOWED_HOSTS += os.getenv("ALLOWED_HOSTS").split(",")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    "bulma",
    "coldcms.blocks",
    "coldcms.home",
    "coldcms.legal_notice",
    "coldcms.simple_page",
    "coldcms.contact",
    "coldcms.generic_page",
    "coldcms.faq",
    "coldcms.partners",
    "coldcms.site_settings",
    "coldcms.blog",
    "coldcms.form_page",
    "coldcms.wagtail_customization",
    "svg",
    "django_assets",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.admin",
    "wagtail.core",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.settings",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "bakery",
    "robots",
    "wagtailbakery",
    "colorfield",
    "wagtailyoast"
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "coldcms.wagtail_customization.middleware.ColdCsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "coldcms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": TEMPLATE_DIRS,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ]
        },
    }
]

WSGI_APPLICATION = "coldcms.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

db_name = os.getenv("DB_NAME", "coldcms")

db_url = os.getenv("DB_URL", "sqlite:///" + join(BASE_DIR, db_name) + ".db")

DATABASES = {"default": dj_database_url.parse(db_url, conn_max_age=600)}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
DCAPV = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": DCAPV + ".UserAttributeSimilarityValidator"},
    {"NAME": DCAPV + ".MinimumLengthValidator"},
    {"NAME": DCAPV + ".CommonPasswordValidator"},
    {"NAME": DCAPV + ".NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-en"
LANGUAGES = [("fr", "Français"), ("en", "English")]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [join(PROJECT_DIR, "locale")]

WY_LOCALE = 'fr_FR'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail
# upgrade).
# See https://docs.djangoproject.com/en/2.1/ref/contrib/staticfiles/
# #manifeststaticfilesstorage
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

default_static_root = join(os.path.dirname(BASE_DIR), "static")
STATIC_ROOT = os.getenv("STATIC_ROOT", default_static_root)
STATIC_URL = "/static/"

# Config django-assets
ASSETS_MODULES = ["coldcms.assets"]
ASSETS_URL_EXPIRE = True
ASSETS_VERSIONS = "timestamp"
THEME_SCSS = None
THEME_VARIABLES_SCSS = None
if THEME and THEME_DIR:
    THEME_SCSS = os.path.join(STATIC_ROOT, 'scss', THEME)
    THEME_VARIABLES_SCSS = f"{THEME_SCSS}_variables"

# Wagtail settings
WAGTAIL_SITE_NAME = "coldcms"
WAGTAILIMAGES_JPEG_QUALITY = 80
WAGTAIL_ALLOW_UNICODE_SLUGS = False
WAGTAIL_ENABLE_UPDATE_CHECK = False
WAGTAILDOCS_SERVE_METHOD = "direct"

# Base URL to use when referring to full URLs within the Wagtail admin backend
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = "http://example.com"

# Wagtail-bakery config
BUILD_DIR = os.getenv("BUILD_DIR", "/srv/app/coldcms/build/")
BAKERY_VIEWS = ("wagtailbakery.views.AllPublishedPagesView",)

MEDIA_ROOT = join(BUILD_DIR, "media")
MEDIA_URL = "/media/"

# SVG settings


SVG_DIRS = [
    join(STATICFILES_DIRS[len(STATICFILES_DIRS) - 1], "svg", path)
    for path in [
        "",
        "fontawesome/solid/",
        "fontawesome/regular/",
        "fontawesome/brands/",
    ]
]
if THEME and THEME_DIR:
    SVG_DIRS.append(join(STATICFILES_DIRS[0], "svg"))


# Email settings
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "465"))
DEFAULT_FROM_EMAIL = os.getenv("DJANGO_DEFAULT_FROM_EMAIL")
DEFAULT_FROM_EMAIL_NAME = os.getenv("DJANGO_DEFAULT_FROM_EMAIL_NAME")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False") == "True"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False") == "True"

# Colors variables
BLACK = "#0a0a0a"
BLACK_BIS = "#121212"
BLACK_TER = "#242424"

GREY_DARKER = "#363636"
GREY_DARK = "#4a4a4a"
GREY = "#7a7a7a"
GREY_LIGHT = "#b5b5b5"
GREY_LIGHTER = "#dbdbdb"
GREY_LIGHTEST = "#ededed"

WHITE_TER = "#f5f5f5"
WHITE_BIS = "#fafafa"
WHITE = "#ffffff"

ORANGE = "#ff470f"
YELLOW = "#ffe08a"
GREEN = "#48c78e"
TURQUOISE = "#00d1b2"
CYAN = "#3e8ed0"
BLUE = "#485fc7"
PURPLE = "#b86bff"
RED = "#f14668"

PRIMARY = "#38b2db"
INFO = CYAN
SUCCESS = GREEN
WARNING = YELLOW
DANGER = RED
