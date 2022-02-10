from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from rest_framework import serializers, viewsets
from rest_framework import permissions
from django.contrib.auth.models import User
from .models import Profile
from chess_app.models import Game
from .serializers import UserSerializer, ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Profiles to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Thanks for Signing Up! {username}')
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    #live_games = Game.get_live(profile)
    match_history = Game.get_completed(profile)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your Profile Was Updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'player': profile,
        'match_history': match_history
    }
    return render(request, 'users/profile.html', context)


def player_search(request):
    if request.method == 'GET':
        username = request.GET['username']
        santaized_name = username.lower()
        santaized_name = ''.join(santaized_name.split())
        if username == '':
            return render(request, 'users/player_page_empty.html')
        try:
            profile = Profile.objects.get(sanitized_name=santaized_name)
        except Profile.DoesNotExist:
            return render(request, 'users/player_page_dne.html', {'username': username})
        match_history = Game.get_completed(profile)

        context = {
            'player': profile,
            'match_history': match_history
        }
        return render(request, 'users/profile.html', context)


def public_profile(request, player_id):
    ...
