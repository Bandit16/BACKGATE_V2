import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatMessage, Member
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # fetch previous messages asynchronously

        previous_messages = await sync_to_async(
            lambda: list(ChatMessage.objects.filter(room_name=self.room_name).order_by('timestamp')),
            thread_sensitive=True
        )()

        for message in previous_messages:
            sender = await sync_to_async(lambda: message.sender.user.username, thread_sensitive=True)()
            profile_pic = await sync_to_async(lambda: message.sender.profile_pic.url if message.sender.profile_pic else "", thread_sensitive=True)()
            file_url = await sync_to_async(lambda: message.file.url if message.file else None, thread_sensitive=True)()
            print("file url mismatch", file_url)

            await self.send(text_data=json.dumps({
                "message": message.message,
                "username": sender,
                "profile_pic": profile_pic,
                "file": file_url,
                "timestamp": message.timestamp.isoformat()
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        
        message = text_data_json.get("message")
        username = text_data_json.get("username")
        profile_pic = text_data_json.get("profile_pic")
        file = text_data_json.get("file")
        print("this is genereting error ",file)

        if not message and not file:
            return  # Ignore messages without content

        # Retrieve the Member instance
        sender = await sync_to_async(Member.objects.get)(user__username=username)

        # Save to db
        if not file:
            chat_message = await sync_to_async(ChatMessage.objects.create)(
                room_name=self.room_name, sender=sender, message=message,
            )

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message, "username": username, "profile_pic": profile_pic, "file": file,"timestamp": datetime.now().isoformat()}
        )
        print(file)
    
    async def chat_message(self, event):
        username = event["username"]
        message = event["message"]
        profile_pic = event["profile_pic"]
        file = event.get('file')
        timestamp = event["timestamp"]
        print("profile_pic_event", file)
        await self.send(text_data=json.dumps({"message": message, "username": username, "profile_pic": profile_pic, "file": file ,"timestamp": timestamp}))