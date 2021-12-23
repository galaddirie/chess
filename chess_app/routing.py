#from channels.routing import route, route_class
#from channels.staticfiles import StaticFilesConsumer
from django.urls import path

#from .consumers import LobbyConsumer


from chess_app import consumers
# routes defined for channel calls
# this is similar to the Django urls, but specifically for Channels

# channel_routing = [
#     route_class(consumers.LobbyConsumer,  path=r"^/game/<uuid:match_id>"),
# ]

ws_urlpatterns = [
    path("game/<uuid:match_id>/", consumers.GameConsumer.as_asgi())
]