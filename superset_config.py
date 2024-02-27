## Mandatory configuration // Do not change

import os
from cachelib.redis import RedisCache

from superset.tasks.types import ExecutorType


def env(key, default=None):
    return os.getenv(key, default)


CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': env('REDIS_HOST'),
    'CACHE_REDIS_PORT': env('REDIS_PORT'),
    'CACHE_REDIS_PASSWORD': env('REDIS_PASSWORD'),
    'CACHE_REDIS_DB': env('REDIS_DB', 1),
}
DATA_CACHE_CONFIG = CACHE_CONFIG

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{env('DB_USER')}:{env('DB_PASS')}@{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}"
SQLALCHEMY_TRACK_MODIFICATIONS = True


class CeleryConfig(object):
    CELERY_IMPORTS = ('superset.sql_lab',)
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}
    BROKER_URL = f"redis://{env('REDIS_HOST')}:{env('REDIS_PORT')}/0"
    CELERY_RESULT_BACKEND = f"redis://{env('REDIS_HOST')}:{env('REDIS_PORT')}/0"


CELERY_CONFIG = CeleryConfig
RESULTS_BACKEND = RedisCache(
    host=env('REDIS_HOST'),
    port=env('REDIS_PORT'),
    key_prefix='superset_results'
)

# This needs to match the name of the environment variable on your application settings on restack console
SECRET_KEY = env('SUPERSET_SECRET_KEY')

# Feature flags
# https://superset.apache.org/docs/installation/configuring-superset#feature-flags

FEATURE_FLAGS = {
    "EMBEDDABLE_CHARTS": False,
    "EMBEDDED_SUPERSET": False,

    "THUMBNAILS": True,
    "THUMBNAILS_SQLA_LISTENERS": True,
}


# Custom configuration and overrides // Add your configuration below
# https://superset.apache.org/docs/installation/configuring-superset

THUMBNAIL_SELENIUM_USER = "admin"
THUMBNAIL_EXECUTE_AS = [ExecutorType.CURRENT_USER, ExecutorType.SELENIUM]

ENABLE_PROXY_FIX = True


# Superset specific config
ROW_LIMIT = 5000


TALISMAN_CONFIG = {
    "content_security_policy": {
        "base-uri": ["'self'"],
        "default-src": ["'self'"],
        "img-src": [
            "'self'",
            "blob:",
            "data:",
            "https://apachesuperset.gateway.scarf.sh",
            "https://static.scarf.sh/",
        ],
        "worker-src": ["'self'", "blob:"],
        "connect-src": [
            "'self'",
            "https://api.mapbox.com",
            "https://events.mapbox.com",
        ],
        "object-src": "'none'",
        "style-src": [
            "'self'",
            "'unsafe-inline'",
        ],
        "script-src": ["'self'", "'strict-dynamic'"],
        "frame-ancestors": "datakimia-superset-embedded-demo.vercel.app"
    },
    "content_security_policy_nonce_in": ["script-src"],
    "force_https": False,
    "session_cookie_secure": False,
}

# Enable CORS
ENABLE_CORS = True

# Configure CORS options if necessary (this is optional and can be customized as needed)
CORS_OPTIONS = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': ['*'],
    'origins': ['datakimia-superset-embedded-demo.vercel.app'],  # add the domains you want to enable or keep * to allow all domains.
    # Add other options here as per your requirements
}
