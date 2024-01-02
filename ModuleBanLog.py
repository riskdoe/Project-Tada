#ban log module
from Module import Module
from fastapi import APIRouter
from EventHandler import EventHandler
from twitchAPI.object.eventsub import ChannelBanEvent
import logging

class Bandata():
    def __init__(self,
                 userID: str,
                 userName: str,
                 moderatorID: str,
                 moderatorName: str,
                 reason: str,
                 bantime: int,
                 endtime: int,
                 permanent: bool):
        self.userID = userID
        self.userName = userName
        self.moderatorID = moderatorID
        self.moderatorName = moderatorName
        self.reason = reason
        self.bantime = bantime
        if endtime == None:
            self.endtime = 0
        else:
            self.endtime = endtime
        if permanent == True:
            self.permanent = 1
        else:
            self.permanent = 0    
        
        
    def __str__(self):
        return f"{self.userName} was banned by {self.moderatorName} for {self.reason}"

class BanLog(Module):
    def __init__(self, eventHandler: EventHandler):
        super().__init__("BanLog", eventHandler)

    def on_ban(self, data: ChannelBanEvent):
        logging.info(f'{self.name}: {data.event.user_name} banned')
        data.event.user_name
        self.event_Handler.DBConn.AddBan(data)
        
