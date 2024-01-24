#ban log module
from Module import Module
from fastapi import APIRouter
from EventHandler import EventHandler
from twitchAPI.object.eventsub import ChannelBanEvent, ChannelUnbanEvent

class BanLog(Module):
    def __init__(self, eventHandler: EventHandler):
        super().__init__("BanLog", eventHandler)
        self.event_Handler.loginfo(self.name, " module loaded")

    async def on_ban(self, data: ChannelBanEvent):
        self.event_Handler.loginfo(self.name, f'{data.event.user_name} banned')
        self.event_Handler.eventtofrontend(self.name, f'{data.event.user_name} banned')
        self.event_Handler.DBConn.AddBan(data)
        
    async def on_unban(self, data: ChannelUnbanEvent):
        self.event_Handler.loginfo(self.name, f'{data.event.user_name} unbanned')
        self.event_Handler.eventtofrontend(self.name, f'{data.event.user_name} unbanned')
        self.event_Handler.DBConn.AddUnBan(data)
        
        
