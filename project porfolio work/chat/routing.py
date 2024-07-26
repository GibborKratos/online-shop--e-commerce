from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from . import consumers
from django.core.asgi import get_asgi_application

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]


