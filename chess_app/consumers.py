# import logging
# #from channels import Group
# from channels.sessions import channel_session
# from .models import Game
# from channels.auth import channel_session_user
# from channels.generic.websocket import JsonWebsocketConsumer
import json
from random import randint
from asyncio import sleep

from channels.generic.websocket import AsyncJsonWebsocketConsumer

class GameConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        print(self.scope['user'])
        self.game_group_name = 'game_%s' % self.match_id
        await self.channel_layer.group_add(
            self.game_group_name,
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
        message = response.get("message", None)
        if event == 'MOVE':
            # Send message to room group
            print(message)
            await self.channel_layer.group_send(self.game_group_name, {
                'type': 'send_game_data',
                'content': message,
                'event': 'MOVE',
                
            })

        if event == 'START':
            
            await self.channel_layer.group_send(self.game_group_name, {
                'type': 'send_game_data',
                'content': message,
                'event': 'START',
                
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
        
        await self.send_json({'payload':content})
