#from channels.routing import route, route_class
#from channels.staticfiles import StaticFilesConsumer
from django.urls import path

#from .consumers import LobbyConsumer


from chess_app import consumers

ws_urlpatterns = [
    path("game/<uuid:match_id>/", consumers.GameConsumer.as_asgi())
]