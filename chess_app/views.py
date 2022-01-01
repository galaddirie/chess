from django.contrib.auth.models import AnonymousUser
from django.db.models import constraints
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import GameCreationForm
from .models import Game
# Create your views here.
from rest_framework import serializers, viewsets
from rest_framework import permissions

from .models import Game
from  users.models import Profile
from .serializers import GameSerializer



class GameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    

def home(request):
    return render(request, 'home.html')


def create_player_helper(request):
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
            player = Profile.objects.get(session_id=request.session.session_key)        
        except Profile.DoesNotExist:
            player = Profile(session_id=request.session.session_key)
            print(player, request.session.session_key)
        player.save()
    return player

def create_game(request):
    """
    Game Creation Form, redirects users to the generated game page
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
    context = {'form':form, 'url': url}
    return render(request, 'chess/create_game.html',context)
    
def online_game(request,match_id ):
    game = Game.objects.get(pk=match_id )
    player = create_player_helper(request)
    context = {
        'game': game,
        'player': player
    }
    return render(request, 'chess/board.html', context)

def lobby(request):
    return render(request, 'chess/lobby.html')

def board(request):
    return render(request, 'chess/board.html')