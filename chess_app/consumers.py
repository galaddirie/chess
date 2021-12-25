
import json
from re import S
import uuid
from random import randint
from asyncio import sleep

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer

class GameConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.game = await self.get_game(self.match_id)
        
        #brodcast group
        self.game_group_name = 'game_%s' % self.match_id
        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )
        if self.scope['user'].is_authenticated:
            self.player = f"{self.scope['user']}"
        else:
            self.player = f"{self.scope['session'].session_key}"
        
        #unique player group for messages specific to this user
        self.player_group_name = 'player_%s' % self.player
        await self.channel_layer.group_add(
            self.player_group_name,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, close_code):
            print("Disconnected")
            # Leave room group
            await self.channel_layer.group_discard(
                self.game_group_name,
                self.channel_name
            )

    async def receive_json(self, content):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = content
        
        event = response.get("event", None)
        message = response.get("message", {})

        if event == 'CONNECT':
            await self.channel_layer.group_send(self.player_group_name, {
                'type': 'send_game_data',
                'content': message,
                'event': 'CONNECT',
            })

        if event == 'UPDATE':
            # NOTE this event is only called from model
            await self.channel_layer.group_send(self.game_group_name, {
                'type': 'send_game_data',
                'content': message,
                'event': 'UPDATE',  
            })

        if event == 'MOVE':
            await self.update_fen(message['fen'])
            await self.channel_layer.group_send(self.game_group_name, {
                'type': 'send_game_data',
                'content': message,
                'event': 'MOVE',  
            })

        if event == 'END':
            # Send message to room group
            await self.channel_layer.group_send(self.game_group_name, {
                'type': 'send_game_data',
                'content': message,
                'event': 'END',
                
            })

    async def send_game_data(self, content):
        """ Receive message from game group """
        #print(content)
        await self.send_json({'payload':content})
    
    @database_sync_to_async
    def get_game(self, pk):
        from .models import Game
        return Game.objects.get(pk=pk)

    @database_sync_to_async
    def update_fen(self,fen):
        print('UPDATING')
        self.game.fen = fen
        self.game.save()