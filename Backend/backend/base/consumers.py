import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth.models import User
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    def connect(self):
        # self.room_name = 'chat_room'
        # self.room_group_name = f'chat_{self.room_name}'

        # await self.channel_layer.group_add(
        #     self.room_group_name,
        #     self.channel_name
        # )

        self.accept()

        self.send(text_data=json.dumps({
            'type':'connection_established',
            'message':'you are now connected',
        }))

    #async def disconnect(self, close_code):
    #    await self.channel_layer.group_discard(
    #        self.room_group_name,
    #        self.channel_name
    #    )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        #sender_id = text_data_json.get('sender_id')
        #recipient_id = text_data_json.get('recipient_id')

        print('Message:', message_content)
        # Retrieve sender and recipient from the database
        # sender = User.objects.get(id=sender_id)
        # recipient = User.objects.get(id=recipient_id)

        # # Save the message to the database
        # message = Message.objects.create(
        #     sender=sender,
        #     recipient=recipient,
        #     content=message_content,
        #     timestamp=timezone.now()
        # )

        # # Send message to the group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message_content,
        #         'sender': sender.username,
        #         'timestamp': message.timestamp.isoformat()
        #     }
        # )

    #async def chat_message(self, event):
    #    message = event['message']
    #    sender = event['sender']
    #    timestamp = event['timestamp']

    #    await self.send(text_data=json.dumps({
    #        'message': message,
    #        'sender': sender,
    #        'timestamp': timestamp
    #    }))
