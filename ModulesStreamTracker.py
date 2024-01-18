import asyncio
from Module import Module
from EventHandler import EventHandler
import logging
from twitchAPI.object.eventsub import *
from twitchAPI.chat import ChatMessage
from twitchAPI.object.api import ChannelInformation,GetChattersResponse
import time
from datetime import datetime
from StreamClasses import *

def get_time():
    return int(time.time())

class StreamTracker(Module):
    def check_if_recording(self):
        if self.active_stream == None:
            return False
        else:
            return True
    
    async def on_channel_update(self, data: ChannelUpdateEvent):
        if self.check_if_recording() != True:
            logging.debug("StreamTracker.on_channel_update: not recording")
            pass
        else:
            logging.info("StreamTracker.on_channel_update: detected title change")
            self.active_stream.add_title(data.event.title, get_time())
            self.active_stream.add_game(data.event.category_name, get_time())
    
    async def on_channel_follow(self, data: ChannelFollowEvent):
        if self.check_if_recording() != True:
            logging.debug("StreamTracker.on_channel_follow: not recording")
            pass
        else:
            logging.info("StreamTracker.on_channel_follow: detected follow")
            self.active_stream.add_follow(data.event.user_name, get_time())
    
    async def on_channel_subscribe(self, data: ChannelSubscribeEvent):
        if self.check_if_recording() != True:
            logging.debug("StreamTracker.on_channel_subscribe: not recording")
            pass
        else:
            logging.info("StreamTracker.on_channel_subscribe: detected sub")
            self.active_stream.add_sub(data.event.user_name, get_time(), data.event.tier) 
    
    async def on_channel_subscription_gift(self, data: ChannelSubscriptionGiftEvent):
        if self.check_if_recording() != True:
            logging.debug("StreamTracker.on_channel_subscription_gift: not recording")
            pass
        else:
            username = ""
            if data.event.is_anonymous:
                username = "Anonymous"
            else:
                username = data.event.user_name
            logging.info("StreamTracker.on_channel_subscription_gift: detected sub gift")
            self.active_stream.add_subgift(username, get_time(), data.event.tier, data.event.total, submessage = data.event.message)
                
    async def on_channel_subscription_message(self, data: ChannelSubscriptionMessageEvent):
        if self.check_if_recording() != True:
            logging.debug("StreamTracker.on_channel_subscription_message: not recording")
            pass
        else:
            logging.info("StreamTracker.on_channel_subscription_message: detected sub message")
            self.active_stream.add_sub(data.event.user_name, get_time(), data.event.tier, resub = True , submessage = data.event.message)
        
    
    async def on_channel_cheer(self, data: ChannelCheerEvent):
        if self.check_if_recording() != True:
            logging.debug("StreamTracker.on_channel_cheer: not recording")
            pass
        else:
            username = ""
            if data.event.is_anonymous:
                username = "Anonymous"
            else:
                username = data.event.user_name
            logging.info(f"StreamTracker.on_channel_cheer: detected cheer")
            self.active_stream.add_cheer(username, get_time(), data.event.bits, data.event.message)
    
    async def on_channel_raid(self, data: ChannelRaidEvent):
        if self.check_if_recording() != True:
            logging.debug("StreamTracker.on_channel_raid: not recording")
            pass
        else:
            logging.info("StreamTracker.on_channel_raid: detected raid")
            self.active_stream.add_raid(data.event.from_broadcaster_user_name, get_time(), data.event.viewers)
        
    
    async def on_stream_online(self, data: StreamOnlineEvent):
        streamid = self.event_Handler.DBConn.getnextStreamID()
        self.active_stream = stream_instance(self,streamid)
        await self.active_stream.check_for_chatters()
        #await self.active_stream.start_worker()
        logging.info("StreamTracker.on_stream_online: recording")
        streaminfo: ChannelInformation = await self.event_Handler.TwitchAPI.get_channel_info()
        self.active_stream.add_title(streaminfo[0].title,get_time())
        self.event_Handler.go_live(streamid)

    
    async def on_stream_offline(self, data: StreamOfflineEvent):
        if self.check_if_recording() != True:
            logging.debug("StreamTracker.on_stream_offline: not recording")
            pass
        else:
            self.active_stream.end_stream()
            logging.info("StreamTracker.on_stream_offline: stream ended")
            self.reocorced_streams.append(self.active_stream)
            self.active_stream = None
            self.event_Handler.go_offline()
    
    async def on_shoutout_received(self, data: ChannelShoutoutReceiveEvent):
        if self.check_if_recording() != True:
            logging.debug("StreamTracker.on_shoutout_received: not recording")
            pass
        else:
            logging.info("StreamTracker.on_shoutout_received: detected shoutout")
            self.active_stream.add_shoutout(data.user.name, get_time())
        
    
    async def on_message(self, data: ChatMessage):
        if self.check_if_recording() != True:
            logging.debug("StreamTracker.on_message: not recording")
            pass
        else:
            logging.info("StreamTracker.on_message: detected message")
            self.active_stream.add_message(data.user.name)
        
    async def on_webfrontend_message(self, command:str):
        logging.info("StreamTracker.on_webfrontend_message: recieved command")
        logging.info(command)
        if command == "startstream":
            logging.info("testing start stream")
            await self.fake_start_stream()
        elif command == "endstream":
            logging.info("testing end stream")
            await self.fake_end_stream()
    
    async def fake_start_stream(self):
        '''this is for testing purposes only'''
        streamid = self.event_Handler.DBConn.getnextStreamID()
        self.active_stream = stream_instance(self,streamid)
        await self.active_stream.check_for_chatters()
        #await self.active_stream.start_worker()
        logging.info("StreamTracker.on_stream_online: recording")
        streaminfo: ChannelInformation = await self.event_Handler.TwitchAPI.get_channel_info()
        self.active_stream.add_title(streaminfo[0].title,get_time())
        self.event_Handler.go_live(streamid)

    
    async def fake_end_stream(self):
        '''this is for testing purposes only'''
        logging.info(self.check_if_recording())
        if self.check_if_recording() != True:
            logging.info("StreamTracker.on_stream_offline: not recording")
        elif self.check_if_recording() == True:
            self.active_stream.end_stream()
            logging.info("StreamTracker.test_on_stream_offline: stream ended")
            #self.reocorced_streams.append(self.active_stream)
            self.event_Handler.DBConn.add_stream(self.active_stream)
            self.active_stream = None
            self.event_Handler.go_offline()
            #write stream details to db

    async def do_worker(self):
        logging.info("StreamTracker.do_worker: workered")
        if self.check_if_recording():
            await self.active_stream.check_for_chatters()



    def __init__(self, event_handler: EventHandler):
        super().__init__("stream_tracker",event_handler)
        
        self.active_stream: stream_instance = None
        self.reocorced_streams: list[stream_instance] = []
