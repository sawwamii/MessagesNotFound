import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import postData
from asgiref.sync import sync_to_async

# handles websocket stuff, i think its vaguely understandable
class ClickConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # handles connection, assigns anyone who connects to a group and then "accepts" the connection
        self.room_group_name = "click_group"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        # yeah, disconnection
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # after receiving a message, sends a message to all users in the group (notice how type has the name of the method "send_post")
        data = json.loads(text_data)

        title = data["title"]
        body = data["body"]
        author = data["author"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_post",
                "title": title,
                "body": body,
                "author": author
            }
        )
        await sync_to_async(postData.objects.create)(data=text_data)

    async def send_post(self, event):
        # sends a message back to the user's websocket, i think?
        await self.send(text_data=json.dumps({
            "title": event["title"],
            "body": event["body"],
            "author": event["author"]
        }))