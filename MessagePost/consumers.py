import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import postData
from asgiref.sync import sync_to_async
from django.core.files.base import ContentFile
import base64 # For potential base64 encoded small files

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

        title = data.get("title") # Use .get for safer access
        body = data.get("body")
        author = data.get("author")
        photo_data_url = data.get("photo") # Expecting data URL for photo
        video_data_url = data.get("video") # Expecting data URL for video

        # prepare data for saving, including file URLs/paths
        post_instance = postData(
            data=json.dumps({"title": title, "body": body, "author": author}) # Keep original text data structure if needed
        )

        photo_url_to_send = None
        if photo_data_url:
            try:
                # assuming photo_data_url is a base64 encoded string: "data:image/png;base64,iVBORw0KGgo..."
                format, imgstr = photo_data_url.split(';base64,') 
                ext = format.split('/')[-1] 
                # You might want to generate a unique filename
                photo_file = ContentFile(base64.b64decode(imgstr), name=f"photo.{ext}")
                post_instance.photo = photo_file
                # After saving, post_instance.photo.url will be available if MEDIA_URL is set
            except Exception as e:
                print(f"Error processing photo: {e}")
                # Handle error, maybe log it or send an error message back

        video_url_to_send = None
        if video_data_url:
            try:
                # assuming video_data_url is a base64 encoded string: "data:video/mp4;base64,..."
                format, videostr = video_data_url.split(';base64,')
                ext = format.split('/')[-1]
                video_file = ContentFile(base64.b64decode(videostr), name=f"video.{ext}")
                post_instance.video = video_file
            except Exception as e:
                print(f"Error processing video: {e}")


        await sync_to_async(post_instance.save)() # save the instance with photo and video

        # Construct URLs for sending over WebSocket if files were saved
        if post_instance.photo:
            photo_url_to_send = post_instance.photo.url
        if post_instance.video:
            video_url_to_send = post_instance.video.url
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_post",
                "title": title,
                "body": body,
                "author": author,
                "photo_url": photo_url_to_send, # Send URL of saved photo
                "video_url": video_url_to_send  # Send URL of saved video
            }
        )

    async def send_post(self, event):
        # sends a message back to the user's websocket, i think?
        await self.send(text_data=json.dumps({
            "title": event.get("title"),
            "body": event.get("body"),
            "author": event.get("author"),
            "photo_url": event.get("photo_url"),
            "video_url": event.get("video_url")
        }))