from channels import sessions
from chess.asgi import application
from django.test import TransactionTestCase

import pytest
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from chess.settings import CHANNEL_LAYERS
from chess_app.models import Game
from users.models import Profile


TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


@database_sync_to_async
def create_game():
    """
    Returns a serilized game with the given primary key(pk)
    """
    game = Game.objects.create()
    return game


@database_sync_to_async
def get_game(pk):
    """
    Returns a serilized game with the given primary key(pk)
    """
    game = Game.objects.get(pk=pk)
    return game


@database_sync_to_async
def create_player():
    """
    Returns a serilized game with the given primary key(pk)
    """
    player = Profile.objects.create(session_id='anon_user')
    return player


class GameWebSocketTestCase(TransactionTestCase):
    """
    Test Module for Game websocket consumer.
    """

    async def test_can_connect_to_server(self):
        self.game = await create_game()
        self.settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
        communicator = WebsocketCommunicator(
            application=application,
            path=f'game/{str(self.game.match_id)}/'
        )

        connected, subprotocol = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_can_send_json_and_recive_json(self):
        self.game = await create_game()
        self.settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
        communicator = WebsocketCommunicator(
            application=application,
            path=f'game/{self.game.match_id}/'
        )

        await communicator.connect()

        message = {
            'event': 'ECHO',
            'data': 'TEST'
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_can_brodcast_message(self):
        self.game = await create_game()
        self.settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
        communicator = WebsocketCommunicator(
            application=application,
            path=f'game/{self.game.match_id}/'
        )

        await communicator.connect()

        message = {
            'type': 'echo.message',
            'event': 'ECHO',
            'data': 'TEST'
        }

        channel_layer = get_channel_layer()
        await channel_layer.group_send('test_group', message=message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_update_game(self):
        self.game = await create_game()
        self.settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
        communicator = WebsocketCommunicator(
            application=application,
            path=f'game/{self.game.match_id}/'
        )

        await communicator.connect()

        message = {
            'event': 'MOVE',
            'message': {'game': {'fen': 'test_string', 'completed': None}}
        }
        channel_layer = get_channel_layer()
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        updated_game = await get_game(self.game.match_id)
        assert updated_game.fen == 'test_string'
        await communicator.disconnect()

    # TODO force sign user in test case so we can
    # test player based events insde recive_json, for now
    # We can assume that if test_can_send_json_and_recive_json,
    # test_can_brodcast_message works, and tets_update_game works
    # that the events inside recive json work

    # async def test_can_connect_to_game(self):
    #     self.game = await create_game()
    #     self.player = await create_player()
    #     self.settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
    #     communicator = WebsocketCommunicator(
    #         application=application,
    #         path=f'game/{str(self.game.match_id)}/'
    #     )

    #     connected, subprotocol = await communicator.connect()

    #     message = {
    #         'event': 'CONNECT',
    #         "message": {"player": self.player.player_id}
    #     }

    #     channel_layer = get_channel_layer()
    #     group_name = f'game_{str(self.game.match_id)}'
    #     await communicator.send_json_to(message=message)
    #     response = await communicator.receive_json_from()
    #     assert response == message
    #     await communicator.disconnect()

    # async def test_can_join_game(self):
    #     self.game = await create_game()
    #     self.player = await create_player()
    #     self.settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
    #     communicator = WebsocketCommunicator(
    #         application=application,
    #         path=f'game/{str(self.game.match_id)}/'
    #     )

    #     connected, subprotocol = await communicator.connect()

    #     message = {
    #         'event': 'JOIN',
    #         "message": {"player": self.player.player_id}
    #     }

    #     channel_layer = get_channel_layer()
    #     group_name = f'game_{str(self.game.match_id)}'
    #     await channel_layer.group_send(group_name, message=message)
    #     response = await communicator.receive_json_from()
    #     assert self.game.opponent == self.player
    #     await communicator.disconnect()
