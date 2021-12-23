from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver    
from rest_framework import serializers, viewsets
from rest_framework import permissions
from rest_framework.response import Response

from django.contrib.auth.models import User
from .models import Profile
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
            return redirect('home-page')
    else:
        form = UserRegisterForm()
    context = {'form':form}
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    return render(request, 'users/profile.html')

