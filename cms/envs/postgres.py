from .common import *  # noqa: F401,F403
import os
from pathlib import Path

# Ensure LOCALE_PATHS is a concrete list/tuple for Django
LOCALE_PATHS = [str(Path(REPO_ROOT) / "conf/locale")]

# Enable content libraries and related apps explicitly
INSTALLED_APPS += [
    'openedx.core.djangoapps.content_libraries.apps.ContentLibrariesConfig',
    'openedx.core.djangoapps.content_tagging',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB', os.getenv('DB_NAME', 'robeli')),
        'USER': os.getenv('POSTGRES_USER', os.getenv('DB_USER', 'robeli')),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', os.getenv('DB_PASSWORD', '')),
        'HOST': os.getenv('POSTGRES_HOST', os.getenv('DB_HOST', 'localhost')),
        'PORT': os.getenv('POSTGRES_PORT', os.getenv('DB_PORT', '5432')),
        'CONN_MAX_AGE': int(os.getenv('DB_CONN_MAX_AGE', '60')),
        'OPTIONS': {
            'sslmode': os.getenv('POSTGRES_SSLMODE', os.getenv('DB_SSLMODE', 'prefer')),
        },
        'ATOMIC_REQUESTS': True,
    }
}