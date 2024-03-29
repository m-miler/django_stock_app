import environ
from django.core.management.utils import get_random_secret_key

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, get_random_secret_key()),
    DEVELOPMENT=(bool, False),
    # POSTGRES
    POSTGRES=(bool, True),
    DB_NAME=(str, "postgres"),
    DB_USER=(str, "postgres"),
    DB_PASSWORD=(str, "postgres"),
    DB_HOST=(str, "db"),
    DB_PORT=(str, "5432"),
    # Twitter
    API_KEY=(str, ""),
    API_KEY_SECRET=(str, ""),
    BEARER_TOKEN=(str, ""),
    ACCESS_TOKEN=(str, ""),
    ACCESS_TOKEN_SECRET=(str, ""),
    # Celery
    CELERY_BROKER=(str, "redis://redis:6379/0"),
)
