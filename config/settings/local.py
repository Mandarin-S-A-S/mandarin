from .base import *
from .base import env
import sys

DEBUG = True

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="JRiMtuME1uNOdfFQfX7YbtBsxe7MFu9hJNqlHc9TtZFC3MplxvwhqnrULD16rqXR",
)

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}

INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

if sys.argv[1] != 'test':
    DATABASES = {"default": env.db("DATABASE_URL")}
else:
    DATABASES = {"default": env.db("DATABASE_TEST_URL")}
