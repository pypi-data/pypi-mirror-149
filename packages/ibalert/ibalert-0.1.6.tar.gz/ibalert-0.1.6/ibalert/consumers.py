import logging
import json
import coloredlogs
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.auth import login

logging.getLogger().setLevel(logging.DEBUG)
coloredlogs.install()
User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        text_data = json.loads(text_data)
        user_id = text_data.get("userID")
        user = await get_user(user_id)
        username = getattr(user, "id")
        await login(self.scope, user)
        await database_sync_to_async(self.scope["session"].save)()
        if self.channel_layer:
            await self.channel_layer.group_add(f"notification-{username}", self.channel_name)

    async def disconnect(self, close_code):
        if self.channel_layer:
            user = self.scope["user"]
            username = getattr(user, "id")
            await self.channel_layer.group_discard(f"notification-{username}", self.channel_name)

    async def new_notification(self, event):
        user = self.scope.get("user")
        if not user:
            await self.close()
        await self.send_json(event)
