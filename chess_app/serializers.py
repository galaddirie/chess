from .models import Game
from rest_framework import serializers
from users.serializers import UserSerializer

class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = '__all__'
        depth = 2



