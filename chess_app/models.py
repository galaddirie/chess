from __future__ import annotations
from typing import TYPE_CHECKING, Union

from django.db.models.query import QuerySet
if TYPE_CHECKING:
    from .models import Game

import uuid
from django.db import models
from django.contrib.auth.models import User
from users.models import Profile

from datetime import datetime, timezone
import pytz
import humanize


from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
# Create your models here.

from django.db.models import Q


class Game(models.Model):

    # players
    match_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(
        Profile, blank=True, null=True, related_name='creator', on_delete=models.CASCADE)

    opponent = models.ForeignKey(
        Profile, related_name='opponent', on_delete=models.CASCADE, null=True, blank=True)
    openGame = models.BooleanField(default=True)

    # game_data
    white = models.ForeignKey(
        Profile, related_name='white', on_delete=models.CASCADE, null=True, blank=True)
    black = models.ForeignKey(
        Profile, related_name='black', on_delete=models.CASCADE, null=True, blank=True)
    fen = models.CharField(max_length=90, blank=True)  # current fen
    pgn = models.TextField(blank=True)
    move_by = models.TimeField(null=True, blank=True)
    winner = models.ForeignKey(
        Profile, related_name='winner', on_delete=models.CASCADE, null=True, blank=True)

    # dates
    completed = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self) -> str:
        return 'Game #{0}'.format(self.pk)

    @staticmethod
    def get_all_open_games() -> QuerySet[Game]:
        """
        Returns a queryset of Games where that are not complete and have no opponent
        """
        return Game.objects.filter(openGame=True, completed=None)

    @staticmethod
    def created_count(user: Profile) -> int:
        """
        Returns a count of total Games created by user
        """
        return Game.objects.filter(creator=user).count()

    @staticmethod
    def get_completed(user: Profile) -> QuerySet[Game]:
        """
        Returns a queryset of Games where a given user participated and completed
        """
        return Game.objects.filter(Q(creator=user) | Q(opponent=user), completed__isnull=False)

    @staticmethod
    def get_live(user: Profile) -> QuerySet[Game]:
        """
        Returns a queryset of Games where a given user participated and did not complete
        """
        return Game.objects.filter(Q(creator=user) | Q(opponent=user), completed=None, openGame=False)

    @staticmethod
    def get_by_id(id: str) -> Game:
        """
        Returns a Game with a matching id
        """
        try:
            return Game.objects.get(pk=id)
        except Game.DoesNotExist:
            # TODO: Handle this Exception
            pass

    @staticmethod
    def create_new(user: Profile) -> Game:
        """
        Create a new game
        """

        new_game = Game(creator=user)
        new_game.save()

        return new_game

    def get_length(self) -> str:
        """
        Returns natrual representation of the timedelta between the game 
        completion and game creation.
        """
        td = self.completed - self.created
        return humanize.naturaldelta(td)

    def time_since(self, asof: datetime = datetime.now(timezone.utc)) -> str:
        """
        Returns a natrual representation of time, between the current time
        and the game completion. 
        """
        td = asof-self.completed
        return humanize.naturaltime(td)

    def mark_complete(self, winner: Profile) -> None:
        """
        Sets a game to completed status and records the winner
        """
        self.winner = winner
        self.completed = datetime.now()
        self.save()


class Lobby(models.Model):
    ...
