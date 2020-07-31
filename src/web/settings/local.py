from qsystem.settings import *
from django.conf import settings
from django.urls import include, path


ALLOWED_HOSTS = ['*']
DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



# Local Static_root
STATIC_ROOT 	= os.path.join(os.path.dirname(BASE_DIR), 'static')
MEDIA_ROOT 		= os.path.join(os.path.dirname(BASE_DIR), 'media')