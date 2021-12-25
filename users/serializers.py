from django.contrib.auth.models import User,Group
from .models import Profile
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'url','profile','email', 'groups']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Profile
        fields = ['user', 'image', 'created', 'last_activity', 'session_id']
        depth = 1

