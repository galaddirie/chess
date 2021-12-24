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


def create_game(request):
    if request.method == 'POST':
        form = GameCreationForm(request.POST)
        if form.is_valid():
            new_game = form.save(commit=False)
            if not request.session.session_key:
                print('no session')
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
            return redirect('game-page', match_id=new_game.match_id)
    else:
        url = None
        form = GameCreationForm()
    context = {'form':form, 'url': url}
    return render(request, 'chess/create_game.html',context)
    

def game(request,match_id ):
    game = Game.objects.get(pk=match_id )
    #print(request.scope)
    # if request.method == 'POST':
    #     ...
    #     if game.openGame and request.user != game.creator:
    #         ...
    #         print(request.user)
    #         game.opponent = request.user
    #         if game.white:
    #             game.black = request.user
    #         else:
    #             game.white = request.user
        
    context = {
        'game': game
    }
    #TODO create LOGIC SO A UNIQUE USER JOINS THE GAME, AND ALL OTHER USERS WHO VIST AFTER NOW JUST SPECTATE THE GAME, SPECTATE IS SECONDAYR
    
    return render(request, 'chess/board.html', context)



def lobby(request):
    return render(request, 'chess/lobby.html')

def board(request):
    return render(request, 'chess/board.html')