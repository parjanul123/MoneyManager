"""
Django Channels routing for BT Pay WebSocket
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/btpay/live/$', consumers.BTPayliveConsumer.as_asgi()),
    re_path(r'ws/btpay/notify/$', consumers.BTPayNotificationConsumer.as_asgi()),
]
