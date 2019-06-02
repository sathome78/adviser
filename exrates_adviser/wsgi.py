# -*- coding: utf-8 -*-
"""
WSGI config for exrates_adviser project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""
# -*- coding: utf-8 -*-
import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exrates_adviser.settings')


application = get_wsgi_application()
application = WhiteNoise(application)
