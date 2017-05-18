"""
WSGI config for homesoko project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import socket
if socket.gethostname() == 'ip-10-0-0-5':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homesoko.settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homesoko.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
