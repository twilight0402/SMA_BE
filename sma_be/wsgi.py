"""
WSGI config for sma_be project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
from sma_be.sectorservice import Update

from django.core.wsgi import get_wsgi_application

# 启动线程，更新数据库
Update.update()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sma_be.settings')

application = get_wsgi_application()
