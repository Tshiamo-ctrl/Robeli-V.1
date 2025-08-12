from .common import *  # noqa: F401,F403
import os
from pathlib import Path
import sys
from openedx.envs.common import make_mako_template_dirs
from urllib.parse import urlparse, parse_qs

# Ensure LOCALE_PATHS is a concrete list/tuple for Django
LOCALE_PATHS = [str(Path(REPO_ROOT) / "conf/locale")]

# Ensure TEMPLATES backend DIRS is a concrete list
try:
    for _backend in TEMPLATES:  # type: ignore[name-defined]
        if _backend.get('NAME') == 'mako':
            _backend['DIRS'] = make_mako_template_dirs(sys.modules[__name__])
        else:
            dirs = _backend.get('DIRS', [])
            if not isinstance(dirs, (list, tuple)):
                _backend['DIRS'] = []
except NameError:  # pragma: no cover
    pass

# Ensure required apps are present without duplicating labels
try:
    INSTALLED_APPS = list(INSTALLED_APPS)
except NameError:  # pragma: no cover
    INSTALLED_APPS = []

if 'openedx.core.djangoapps.theming.apps.ThemingConfig' not in INSTALLED_APPS:
    INSTALLED_APPS.append('openedx.core.djangoapps.theming.apps.ThemingConfig')
if 'openedx.core.djangoapps.content_libraries.apps.ContentLibrariesConfig' not in INSTALLED_APPS:
    INSTALLED_APPS.append('openedx.core.djangoapps.content_libraries.apps.ContentLibrariesConfig')
if 'openedx.core.djangoapps.bookmarks' not in INSTALLED_APPS and 'openedx.core.djangoapps.bookmarks.apps.BookmarksConfig' not in INSTALLED_APPS:
    INSTALLED_APPS.append('openedx.core.djangoapps.bookmarks')
if 'openedx.core.djangoapps.discussions' not in INSTALLED_APPS and 'openedx.core.djangoapps.discussions.apps.DiscussionsConfig' not in INSTALLED_APPS:
    INSTALLED_APPS.append('openedx.core.djangoapps.discussions')
if 'openedx.core.djangoapps.content_staging.apps.ContentStagingAppConfig' not in INSTALLED_APPS:
    INSTALLED_APPS.append('openedx.core.djangoapps.content_staging.apps.ContentStagingAppConfig')

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

# Allow overriding DB settings via DATABASE_URL (e.g., Railway Postgres plugin)
DATABASE_URL = os.getenv('DATABASE_URL', '')
if DATABASE_URL.startswith(('postgres://', 'postgresql://')):
    try:
        parsed = urlparse(DATABASE_URL)
        db_name = (parsed.path or '').lstrip('/') or DATABASES['default']['NAME']
        db_user = parsed.username or DATABASES['default']['USER']
        db_password = parsed.password or DATABASES['default']['PASSWORD']
        db_host = parsed.hostname or DATABASES['default']['HOST']
        db_port = str(parsed.port or DATABASES['default']['PORT'])
        query = parse_qs(parsed.query or '')
        sslmode = query.get('sslmode', [DATABASES['default']['OPTIONS'].get('sslmode', 'prefer')])[0]
        DATABASES['default'].update({
            'NAME': db_name,
            'USER': db_user,
            'PASSWORD': db_password,
            'HOST': db_host,
            'PORT': db_port,
        })
        DATABASES['default'].setdefault('OPTIONS', {})
        DATABASES['default']['OPTIONS']['sslmode'] = sslmode
    except Exception:
        # Fall back silently if parsing fails
        pass

# Hosts and security settings suitable for Railway reverse proxy

def _parse_hosts_csv(hosts_csv: str) -> list[str]:
    values: list[str] = []
    for token in hosts_csv.split(','):
        token = token.strip()
        if not token:
            continue
        token = token.replace('https://', '').replace('http://', '')
        token = token.split('/')[0]
        values.append(token)
    return values

_raw_hosts = os.getenv('DJANGO_ALLOWED_HOSTS') or os.getenv('ALLOWED_HOSTS') or os.getenv('RAILWAY_PUBLIC_DOMAIN', '')
_allowed_hosts = _parse_hosts_csv(_raw_hosts) if _raw_hosts else []
if not _allowed_hosts:
    _allowed_hosts = ['*']
ALLOWED_HOSTS = _allowed_hosts

# Trust Railway/Heroku-style proxy headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# CSRF trusted origins derived from allowed hosts (cannot include wildcards)
_csrf_origins = []
for _host in _allowed_hosts:
    if _host == '*':
        continue
    _csrf_origins.extend([f'https://{_host}', f'http://{_host}'])
if _csrf_origins:
    try:
        CSRF_TRUSTED_ORIGINS = list(set((locals().get('CSRF_TRUSTED_ORIGINS', []) or [])) | set(_csrf_origins))
    except Exception:
        CSRF_TRUSTED_ORIGINS = _csrf_origins

# Secure cookies in hosted environments
_secure_cookies = os.getenv('DJANGO_SECURE_COOKIES', 'true').lower() == 'true'
SESSION_COOKIE_SECURE = _secure_cookies
CSRF_COOKIE_SECURE = _secure_cookies

# Ensure Open edX events use plain booleans, not Derived values, to satisfy openedx_events validation
try:
    _event_cfg = EVENT_BUS_PRODUCER_CONFIG['org.openedx.learning.certificate.created.v1']
    _enable_cert_events = os.getenv('ENABLE_CERTIFICATE_EVENTS', 'false').lower() in ('1', 'true', 'yes', 'on')
    _event_cfg['learning-certificate-lifecycle']['enabled'] = bool(_enable_cert_events)
except Exception:
    pass