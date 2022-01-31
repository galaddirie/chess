from __future__ import annotations
from typing import TYPE_CHECKING, Union, Dict
if TYPE_CHECKING:
    from uuid import UUID
    from .models import Game
    from users.models import Profile

import datetime
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async


class GameConsumer(AsyncJsonWebsocketConsumer):
    """
    Attributes
    ----------
    match_id: a uuid that is the primary key for game objects
    game: the generated game
    player: a serialized profile object
    game_group_name: the name of the global brodcasting group channel 
    player_group_name:  a unique name for a group only a single user is 
                        connected too, generated from the authenticated user or
                        if user is anonymous, from their session_key
    """
    match_id: str
    game: Game
    player: Dict
    game_group_name: str
    player_group_name: str

    async def connect(self) -> None:
        """
        Generates channel groups from match_id and player_id  
        and establishes a long polling connection
        """
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.game = await self.get_game(self.match_id)
        self.player = None
        self.game_group_name = f'game_{self.match_id}'
        await self.channel_layer.group_add(
            'test_group',
            self.channel_name
        )

        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )

        if self.scope['user'].is_authenticated:
            pid = f"{self.scope['user']}"
        else:
            pid = f"{self.scope['session'].session_key}"

        self.player_group_name = f'player_{pid}'
        await self.channel_layer.group_add(
            self.player_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        """
        Disconnects user from channel groups
        """
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )
        await self.channel_layer.group_discard(
            self.player_group_name,
            self.channel_name
        )

    async def echo_message(self, content):
        await self.send_json(content)

    async def receive_json(self, content: Dict) -> None:
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = content
        event = response.get("event", None)
        message = response.get("message", {})
        if event == 'ECHO':
            await self.send_json(content)
        if event == 'JOIN':
            print('JOIN')
            await self.update_game(message['game'])
            message['game'] = await self.serialize_game()

        if event == 'UPDATE':
            # is it faster to modify the instance and save vs query, the issue with modifying the model
            # instance is that we will be savinging the game again and since the update meathod is
            # called by every user who is in the group after a join event
            self.game = await self.get_game(self.match_id)

        if event == 'MOVE':
            # game is updated once, all players recive the a serialized version
            # and update their game in the client, self.game will be out of sync
            # in other player instances until they make an update tehmselves, any new connections(or reconnections),
            # will recive the most updated version when they request the game from the database
            if message['gameUpdates']['completed']:
                message['gameUpdates']['completed'] = datetime.datetime.now().__str__()
            await self.update_game(message['gameUpdates'])
            message['game'] = await self.serialize_game()

        if event == 'END':
            ...

        if event == 'CONNECT':
            # We send two messages, one contain
            self.player = await self.serialize_player(message['player'])
            message['player'] = self.player
            # we send a message containg the game data to the player only,
            # but we send player data to everyone on connect, we are sending
            # player data to the one connecting twice as a consequence
            # this is worse for cases of  all users when num_of_users <= 2  and
            # this will always be worse for the connecting user
            message_copy = message.copy()
            message_copy['game'] = await self.serialize_game()
            await self.event_response(
                event, message_copy, self.player_group_name)
        await self.event_response(event, message, self.game_group_name)

    async def event_response(self, event: str, message: Dict, group: str) -> None:
        """
        Helper function to handle brodcasting messages
        """
        await self.channel_layer.group_send(group, {
            'type': 'send_game_data',
            'message': message,
            'event': event,
        })

    async def send_game_data(self, content: Dict) -> None:
        """ 
        Receive message from game group 
        """
        print(self.player_group_name)
        await self.send_json(content)

    @database_sync_to_async
    def get_game(self, pk: Union[UUID, str]) -> Game:
        """
        Returns a serilized game with the given primary key(pk)
        """
        from .models import Game
        return Game.get_by_id(pk)

    @database_sync_to_async
    def serialize_game(self) -> Dict:
        """
        Returns a serilized copy of a game instance
        """
        from .serializers import GameSerializer
        return GameSerializer(self.game).data

    @database_sync_to_async
    def serialize_player(self, pk: str) -> Dict:
        """
        Returns a serilized copy of a profile with the given primary key (pk)
        """
        from users.models import Profile
        from users.serializers import ProfileSerializer
        player = ProfileSerializer(Profile.objects.get(pk=pk))
        return player.data

    @database_sync_to_async
    def update_game(self, new_game: Dict) -> None:
        """
        Recives serilized game data and updates each attribute 
        """
        from users.models import Profile
        for attr, value in new_game.items():
            if(attr in ['creator', 'white', 'black', 'opponent', 'winner']):
                # in Onlinematch.js when a player joins the game we initlize it,
                # the game attr with a profile type are initlized with just
                # a player_id, after that any profile atributes will contain a
                # serilized object containing player data
                if isinstance(value, dict):
                    pid = value['player_id']
                else:
                    pid = value
                if value is not None:
                    profile = Profile.objects.get(pk=pid)
                    setattr(self.game, attr, profile)
            else:
                setattr(self.game, attr, value)
        self.game.save()

        # if message['game']['winner']:
        #     await self.channel_layer.group_send(self.game_group_name, {
        #         'type': 'receive_json',
        #         'content': message,
        #         'event': 'END',
        #     })
