from .common import *  # noqa: F401,F403
import os
from pathlib import Path

# Ensure LOCALE_PATHS is a concrete list/tuple for Django
LOCALE_PATHS = [str(Path(REPO_ROOT) / "conf/locale")]

# Ensure required apps are present without duplicating labels
try:
    INSTALLED_APPS = list(INSTALLED_APPS)
except NameError:  # pragma: no cover
    INSTALLED_APPS = []

if 'openedx.core.djangoapps.content_libraries.apps.ContentLibrariesConfig' not in INSTALLED_APPS:
    INSTALLED_APPS.append('openedx.core.djangoapps.content_libraries.apps.ContentLibrariesConfig')
if 'openedx.core.djangoapps.bookmarks' not in INSTALLED_APPS and 'openedx.core.djangoapps.bookmarks.apps.BookmarksConfig' not in INSTALLED_APPS:
    INSTALLED_APPS.append('openedx.core.djangoapps.bookmarks')

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