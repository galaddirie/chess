from __future__ import annotations
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from uuid import UUID

from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import GameCreationForm
from .models import Game
from rest_framework import serializers, viewsets
from rest_framework import permissions

from .models import Game
from users.models import Profile
from .serializers import GameSerializer


class GameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]


def home(request) -> HttpResponse:
    """
    Returns an HttpResponse containing the home page template
    """
    return render(request, 'home.html')


def create_player_helper(request) -> Profile:
    """
    Returns a Player Profile, if the user is not authenticted we generate 
    a temporary profile for them based on their session id
    """
    if not request.session.session_key:
        request.session.create()
    print(request.session.session_key)
    if request.user.is_authenticated:
        player = request.user.profile
    else:
        try:
            player = Profile.objects.get(
                session_id=request.session.session_key)
        except Profile.DoesNotExist:
            player = Profile.objects.create(
                session_id=request.session.session_key)
            print(player, request.session.session_key)
        # player.save()
    return player


def create_game(request) -> HttpResponseRedirect:
    """
    Game Creation Form, redirects users to the generated game page.
    """
    if request.method == 'POST':
        form = GameCreationForm(request.POST)
        if form.is_valid():
            new_game = form.save(commit=False)
            player = create_player_helper(request)
            new_game.creator = player

            if form.cleaned_data['side'] == 'white':
                new_game.white = player
            else:
                new_game.black = player
            new_game.save()
            url = '/game/' + str(new_game.match_id)
            context = {
                'url': url
            }
            return redirect('online-game-page', match_id=new_game.match_id)

    else:
        url = None
        form = GameCreationForm()
    context = {'form': form, 'url': url}
    return render(request, 'chess/create_game.html', context)


def online_game(request, match_id: Union[UUID, str]) -> HttpResponse:
    """
    Returns a HttpResponse containing the game page template, 
    initlizes the game and player for the consumer. 
    """
    game = Game.get_by_id(match_id)
    player = create_player_helper(request)
    context = {
        'game': game,
        'player': player
    }
    return render(request, 'chess/board.html', context)


def lobby(request) -> HttpResponse:
    return render(request, 'chess/lobby.html')
