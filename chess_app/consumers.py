
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
        self.player = None
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
 
        if event == 'JOIN':
            await self.update_game(message['game'])
        
        if event == 'UPDATE':
            ...
           
        if event == 'MOVE':
            await self.update_game(message['game'])
            
        if event == 'END':
            # Send message to room group
            ...
        
        message['game'] =  await self.serialize_game()
        if event == 'CONNECT':
            print('CONNECT')
            self.player = await self.serialize_player(message['player'])
            print(self.player)
            message['player'] = self.player
            #print(message['game'])
            await self.event_response(event,message,self.game_group_name) #TODO SET group to game_group_name when connection checks are in place

        else:
            await self.event_response(event,message,self.game_group_name)
    
    async def event_response(self, event, message, group):
        await self.channel_layer.group_send(group, {
                'type': 'send_game_data',
                'content': message,
                'event': event,
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
    def serialize_game(self):
        from .serializers import GameSerializer
        return GameSerializer(self.game).data

    @database_sync_to_async
    def serialize_player(self, pk):
        from users.models import Profile
        from users.serializers import ProfileSerializer
        player =ProfileSerializer(Profile.objects.get(pk=pk))
        
        return player.data

    @database_sync_to_async
    def update_game(self,new_game):
        from users.models import Profile
        print(new_game)
        print('-----------------------------------------------------')
        for attr, value in new_game.items():
            print(attr)
            if(attr in ['creator', 'white', 'black', 'opponent']):
                ...
                print(type(value))
                
                if isinstance(value,dict):
                    pid = value['player_id']
                else:
                    pid = value
                
                try:
                    profile = Profile.objects.get(pk=pid)
                    setattr(self.game, attr, profile)
                except Profile.DoesNotExist:
                    ...
                
            else:
                setattr(self.game, attr, value)
            

        self.game.save()