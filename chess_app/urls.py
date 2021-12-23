from django.urls import path
from . import views

urlpatterns = [
    path('chess/', views.board, name ='chess-page'),
    path('', views.home, name ='home-page'),
    path('create/', views.create_game, name ='create-game-page'),
    path('game/<uuid:match_id>/', views.game, name ='game-page'),
    path('lobby/', views.lobby, name ='lobby-page'),
]
