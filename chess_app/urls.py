from django.urls import path
from . import views

urlpatterns = [
    path('chess/', views.board, name ='chess-page'),
    path('', views.home, name ='home-page'),
    
    #path('summoner/', views.get_summoner, name ='player-page'),
]
