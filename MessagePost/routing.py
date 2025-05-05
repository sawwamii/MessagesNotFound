from django.urls import re_path

from . import consumers

# idk really but it basically(?) routes this websocket url to this specific consumer method (clickconsumer)
websocket_urlpatterns = [
    re_path(r"ws/post/$", consumers.ClickConsumer.as_asgi()),
]