from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from .models import Chat,Group
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from time import sleep

class MySyncConsumer(SyncConsumer):
  def websocket_connect(self,event):
   # print('websocket connected',event)
    print('channel layer......',self.channel_layer)
    # async_to_sync(self.channel_layer.group_add)(
    #   'programmers',self.channel_name
    #   )
    
    self.group_name=self.scope['url_route']['kwargs']['groupkaname']
    print('group name.......',self.group_name)
    async_to_sync(self.channel_layer.group_add)(
      self.group_name,self.channel_name
      )
    self.send({
     'type':'websocket.accept'
    })
      
    

  def websocket_receive(self,event):
    print("user.........")
    print('websocket received from client',self.scope['user'])
    data=json.loads(event['text'])
    

    group= Group.objects.get(name=self.group_name)
    if self.scope['user'].is_authenticated:
      chat=Chat(
      content=data['msg'],
      group=group
      )
      chat.save()
      data['user']=self.scope['user'].username
      print('data...',data)
      async_to_sync(self.channel_layer.group_send)(self.    group_name,{
      'type':'chat.message',
      'message':json.dumps(data)
      })
    else:
      self.send({
        'type':'websocket.send',
        'text':json.dumps({"msg":"Login required","user":"guest"})
      })

  

  def chat_message(self,event):
    print('event...',event)
    self.send({
      'type':'websocket.send',
      'text':event['message']
    })
  #   print("user.........")
  #   print('websocket received from client',self.scope['user'])
  #   data=json.loads(event['text'])
    

  #   group= Group.objects.get(name=self.group_name)
  #   if self.scope['user'].is_authenticated:
  #     chat=Chat(
  #     content=data['msg'],
  #     group=group
  #     )
  #     chat.save()
  #     async_to_sync(self.channel_layer.group_send)(self.    group_name,{
  #     'type':'chat.message',
  #     'message':event['text']
  #     })
  #   else:
  #     self.send({
  #       'type':'websocket.send',
  #       'text':json.dumps({"msg":"Login required"})
  #     })

  

  # def chat_message(self,event):
  #   print('event...',event)
  #   self.send({
  #     'type':'websocket.send',
  #     'text':event['message']
  #   })
  

  def websocket_disconnect(self,event):
    #print('websocket disconneted',event)
    print('channel layer.....',self.channel_layer)
    print('channel name......',self.channel_name)
    async_to_sync(self.channel_layer.group_discard)(self.group_name,self.channel_name)
    raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):
  async def websocket_connect(self,event):
   # print('websocket connected',event)
    print('channel layer......',self.channel_layer)
    self.group_name=self.scope['url_route']['kwargs']['groupkaname']
    await self.channel_layer.group_add(
      'programmers',self.channel_name
      )
    await self.send({
     'type':'websocket.accept'
    })
      
    

  async def websocket_receive(self,event):

    data=json.loads(event['text'])
    group= await database_sync_to_async(Group.objects.get)(name=self.group_name)
    chat=Chat(
      content=data['msg'],
      group=group
    )
    await database_sync_to_async(chat.save)()
    print('websocket received from client',event['text'])
    await self.channel_layer.group_send('programmers',{
      'type':'chat.message',
      'message':event['text']
    })
    data=json.loads(event['text'])
    group= await database_sync_to_async(Group.objects.get)(name=self.group_name)
    chat=Chat(
      content=data['msg'],
      group=group
    )
    await database_sync_to_async(chat.save)()
  async def chat_message(self,event):
    print('event...',event)
    await self.send({
      'type':'websocket.send',
      'text':event['message']
    })

  async def websocket_disconnect(self,event):
    #print('websocket disconneted',event)
    print('channel layer.....',self.channel_layer)
    print('channel name......',self.channel_name)
    await self.channel_layer.group_discard('programmers',self.channel_name)
    raise StopConsumer()
  
class MyWebsocketConsumer(WebsocketConsumer):
  def connect(self):
    print('ws connected')
    self.accept()
   # self.close() #to reject the connection

  def receive(self, text_data=None, bytes_data=None):
    print('msg received.....',text_data)
    for i in range(25): 
      self.send(text_data=str(i))
    
      sleep(1)

    


  def disconnect(self, close_code):
    print('ws closed',close_code)

class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    print('ws connected')
    await self.accept()
   # self.close() #to reject the connection

  async def receive(self, text_data=None, bytes_data=None):
    print('msg received.....',text_data)
    await self.send(text_data="msg from server")
    await self.close()


  async def disconnect(self, close_code):
    print('ws closed',close_code)

