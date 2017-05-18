# Custom application settings - anything that's not required by core Django
from homesoko.base import *  # pylint: disable=W0614,W0401 @UnusedWildImport

#=============================
# Version number
#============================
VERSION = '0.1'

# static and media files
import homesoko as project_module
PROJECT_DIR = os.path.dirname(os.path.realpath(project_module.__file__))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, '../assets/front'),
    os.path.join(PROJECT_DIR, '../assets/back'),
    os.path.join(PROJECT_DIR, '../assets/zoner'),
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, '../templates'),
)
###########################################
# django-userena settings
###########################################

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ANONYMOUS_USER_ID = -1

AUTH_PROFILE_MODULE = 'users.Profile'

USERENA_MUGSHOT_GRAVATAR = False

USERENA_SIGNIN_REDIRECT_URL = '/dashboard/listings'

LOGIN_REDIRECT_URL = '/accounts/%(username)s/'

LOGIN_URL = '/accounts/signin/'

LOGOUT_URL = '/accounts/signout/'

##############################################
# pinax django-user-accounts
##############################################

ACCOUNT_LOGIN_REDIRECT_URL = '/dashboard/listings'

#======================================================
# Grappelli
#======================================================
GRAPPELLI_ADMIN_TITLE = 'Homesoko Admin'
