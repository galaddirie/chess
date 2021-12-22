import uuid
from django import urls
from django.db import models
from django.contrib.auth.models import User
import json
from datetime import datetime
#from channels import Group
from django.db.models.base import Model

# Create your models here.



class Game(models.Model):
    ...
    #players
    match_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    opponent = models.ForeignKey(User, related_name='opponent', on_delete=models.CASCADE, null=True, blank=True)
    openGame = models.BooleanField(default=True)
    #game_data
    white = models.ForeignKey(User, related_name='white', on_delete=models.CASCADE, null=True, blank=True)
    black = models.ForeignKey(User, related_name='black', on_delete=models.CASCADE, null=True, blank=True)
    fen = models.CharField(max_length=90, blank=True) #current fen 
    pgn = models.TextField(blank=True)
    move_by = models.TimeField(null=True, blank=True)
    winner = models.ForeignKey(User, related_name='winner', on_delete=models.CASCADE, null=True, blank=True)

    # # dates
    completed = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return 'Game #{0}'.format(self.pk)

    @staticmethod
    def get_available_games():
        return Game.objects.filter(openGame=True, completed=None)

    @staticmethod
    def created_count(user):
        return Game.objects.filter(creator=user).count()

    @staticmethod
    def get_by_id(id):
        try:
            return Game.objects.get(pk=id)
        except Game.DoesNotExist:
            # TODO: Handle this Exception
            pass

    @staticmethod
    def create_new(user):
        """
        Create a new game and game squares
        :param user: the user that created the game
        :return: a new game object
        """
        # make the game's name from the username and the number of
        # games they've created
        new_game = Game(creator=user)
        new_game.save()
        # for each row, create the proper number of cells based on rows
       #
        # put first log into the GameLog
        new_game.add_log('Game created by {0}'.format(new_game.creator.username))

        return new_game

    # def send_game_update(self):
    #     """
    #     Send the updated game information and squares to the game's channel group
    #     """
    #     # imported here to avoid circular import
    #     from .serializers import GameSerializer, GameLogSerializer


    #     # get game log
    #     log = self.get_game_log()
    #     log_serializer = GameLogSerializer(log, many=True)

    #     game_serilizer = GameSerializer(self)

    #     message = {'game': game_serilizer.data,
    #                 'log': log_serializer.data,
    #     }

    #     game_group = 'game-{0}'.format(self.id)
    #     Group(game_group).send({'text': json.dumps(message)})

    def mark_complete(self, winner):
        """
        Sets a game to completed status and records the winner
        """
        self.winner = winner
        self.completed = datetime.now()
        self.save()


class Lobby(models.Model):
    ...