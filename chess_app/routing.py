#from channels.routing import route, route_class
#from channels.staticfiles import StaticFilesConsumer
from django.urls import path

#from .consumers import LobbyConsumer


from chess_app import consumers
# routes defined for channel calls
# this is similar to the Django urls, but specifically for Channels
# channel_routing = [
#     route_class(consumers.LobbyConsumer,  path=r"^/lobby/"),
# ]

ws_urlpatterns = [
    #path('ws/some_url', LobbyConsumer.as_asgi())
]