from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'url', 'profile', 'email', 'groups']


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1
