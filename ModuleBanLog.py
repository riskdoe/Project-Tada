#ban log module
from Module import Module
from fastapi import APIRouter
from EventHandler import EventHandler
from twitchAPI.object.eventsub import ChannelBanEvent, ChannelUnbanEvent
import logging

class BanLog(Module):
    def __init__(self, eventHandler: EventHandler):
        super().__init__("BanLog", eventHandler)

    async def on_ban(self, data: ChannelBanEvent):
        logging.info(f'{self.name}: {data.event.user_name} banned')
        self.event_Handler.DBConn.AddBan(data)
        
    async def on_unban(self, data: ChannelUnbanEvent):
        logging.info(f'{self.name}: {data.event.user_name} unbanned by {data.event.moderator_user_name}')
        self.event_Handler.DBConn.AddUnBan(data)
        
        
