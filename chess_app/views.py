from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import GameCreationForm
from .models import Game
# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required
def create_game(request):
    if request.method == 'POST':
        form = GameCreationForm(request.POST)
        if form.is_valid():
            new_game = form.save(commit=False)
            new_game.creator = request.user

            print(form.cleaned_data['side'])
            if form.cleaned_data['side'] == 'white':
                new_game.white = request.user
            else:
                new_game.black = request.user

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
    
@login_required
def game(request,match_id ):
    game = Game.objects.get(pk=match_id )
    context = {
        'game': game
    }
    return render(request, 'chess/board.html', context)


@login_required
def lobby(request):
    return render(request, 'chess/lobby.html')

def board(request):
    return render(request, 'chess/board.html')