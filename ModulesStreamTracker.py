import asyncio
from Module import Module
from EventHandler import EventHandler
import logging
from twitchAPI.object.eventsub import *
from twitchAPI.chat import ChatMessage
from twitchAPI.object.api import ChannelInformation
import time

def get_time():
    return int(time.time())

class title():
    def __init__(self, title, changetime):
        self.title = title
        self.changetime = changetime

class game():
    def __init__(self, game, changetime):
        self.game = game
        self.changetime = changetime

class follow():
    def __init__(self, user, followtime):
        self.user = user
        self.followtime = followtime
        
class sub():
    def __init__(self, user, subtime, sublevel, resub = False, submessage:str = None):
        self.user = user
        self.subtime = subtime
        self.submessage = submessage
        self.sublevel = sublevel
        self.resub = resub

class subgift():
    def __init__(self, user, subtime, sublevel, count, submessage:str = None):
        self.user = user
        self.subtime = subtime
        self.submessage = submessage
        self.sublevel = sublevel
        self.count = count

class raid():
    def __init__(self, user, raidtime, raiders):
        self.user = user
        self.raidtime = raidtime
        self.numberofraiders = raiders

class cheer():
    def __init__(self, user, cheertime, bits, message:str = None):
        self.user = user
        self.cheertime = cheertime
        self.bits = bits
        self.message = message

class shoutout():
    def __init__(self, user, shoutouttime):
        self.user = user
        self.shoutouttime = shoutouttime


class stream_instance():
    def __init__(self):
        self.stream_start_time = get_time()
        self.stream_end_time = None
        self.stream_duration = None
        self.stream_title: list[title]= []
        self.stream_game: list[game] = []
        self.follows_during_stream: list[follow] = []
        self.subs_during_stream: list[sub] = []
        self.giftsubs_during_stream: list[subgift] = []
        self.raids_during_stream: list[raid] = []
        self.cheers_during_stream: list[cheer] = []
        self.shoutouts_during_stream: list[shoutout] = []
        self.active_chatter = []
        self.num_of_messages_during_stream = 0
        
        #we need a worker for this next part
        #updates every x ammount of time
        self.update_time = 60
        self.number_of_veiwers_during_stream = []

    def updatewasrun(self):
        logging.info("stream_instance.updatewasrun: update was run")
        logging.info(f"stream_instance.updatewasrun: {self.stream_start_time} was starttime")
        logging.info(f"stream_instance.updatewasrun: {self.num_of_messages_during_stream} messages were sent")
        logging.info(f"stream_instance.updatewasrun: {len(self.active_chatter)} chatters were active")
        logging.info(f"stream_instance.updatewasrun: {len(self.follows_during_stream)} follows were made")
        logging.info(f"stream_instance.updatewasrun: {len(self.subs_during_stream)} subs were made")
        logging.info(f"stream_instance.updatewasrun: {len(self.giftsubs_during_stream)} gift subs were made")
        logging.info(f"stream_instance.updatewasrun: {len(self.raids_during_stream)} raids were made")
        logging.info(f"stream_instance.updatewasrun: {len(self.cheers_during_stream)} cheers were made")
        logging.info(f"stream_instance.updatewasrun: {len(self.shoutouts_during_stream)} shoutouts were made")
        if(self.stream_end_time != None):
            logging.info(f"stream_instance.updatewasrun: {self.stream_end_time} was endtime")
            logging.info(f"stream_instance.updatewasrun: {self.stream_duration} was duration")
        
        

    def end_stream(self):
        self.stream_end_time = get_time()
        self.stream_duration = self.stream_end_time - self.stream_start_time
        self.updatewasrun()

    def add_title(self, streamtitle, changetime):
        self.stream_title.append(title(streamtitle, changetime))
        self.updatewasrun()

    
    def add_game(self, game, changetime):
        self.stream_game.append(game(game, changetime))
        self.updatewasrun()

    def add_follow(self, user, followtime):
        self.follows_during_stream.append(follow(user, followtime))
        self.updatewasrun()

    def add_sub(self, user, subtime, sublevel, resub = False, submessage:str = None):
        self.subs_during_stream.append(sub(user, subtime, sublevel, resub,submessage))
        self.updatewasrun()

    def add_subgift(self, user, subtime, sublevel, count, submessage:str = None):
        self.giftsubs_during_stream.append(subgift(user, subtime, sublevel, count, submessage))
        self.updatewasrun()
        
    def add_raid(self, user, raidtime, raiders):
        self.raids_during_stream.append(raid(user, raidtime, raiders))
        self.updatewasrun()
        
    def add_cheer(self, user, cheertime, bits, message:str = None):
        self.cheers_during_stream.append(cheer(user, cheertime, bits, message))
        self.updatewasrun()
        
    def add_shoutout(self, user, shoutouttime):
        self.shoutouts_during_stream.append(shoutout(user, shoutouttime))
        self.updatewasrun()
        
    def add_message(self, chatername):
        self.num_of_messages_during_stream += 1
        if chatername not in self.active_chatter:
            self.active_chatter.append(chatername)
        self.updatewasrun()


class StreamTracker(Module):
    def check_if_recording(self):
        if self.active_stream == None:
            return False
        else:
            return True
    
    async def on_channel_update(self, data: ChannelUpdateEvent):
        if self.check_if_recording() != True:
            logging.info("StreamTracker.on_channel_update: not recording")
            pass
        else:
            logging.info("StreamTracker.on_channel_update: detected title change")
            self.active_stream.add_title(data.event.title, get_time())
            self.active_stream.add_game(data.event.category_name, get_time())
    
    async def on_channel_follow(self, data: ChannelFollowEvent):
        if self.check_if_recording() != True:
            logging.info("StreamTracker.on_channel_follow: not recording")
            pass
        else:
            logging.info("StreamTracker.on_channel_follow: detected follow")
            self.active_stream.add_follow(data.event.user_name, get_time())
    
    async def on_channel_subscribe(self, data: ChannelSubscribeEvent):
        if self.check_if_recording() != True:
            logging.info("StreamTracker.on_channel_subscribe: not recording")
            pass
        else:
            logging.info("StreamTracker.on_channel_subscribe: detected sub")
            self.active_stream.add_sub(data.event.user_name, get_time(), data.event.tier) 
    
    async def on_channel_subscription_gift(self, data: ChannelSubscriptionGiftEvent):
        if self.check_if_recording() != True:
            logging.info("StreamTracker.on_channel_subscription_gift: not recording")
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
            logging.info("StreamTracker.on_channel_subscription_message: not recording")
            pass
        else:
            logging.info("StreamTracker.on_channel_subscription_message: detected sub message")
            self.active_stream.add_sub(data.event.user_name, get_time(), data.event.tier, resub = True , submessage = data.event.message)
        
    
    async def on_channel_cheer(self, data: ChannelCheerEvent):
        if self.check_if_recording() != True:
            logging.info("StreamTracker.on_channel_cheer: not recording")
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
            logging.info("StreamTracker.on_channel_raid: not recording")
            pass
        else:
            logging.info("StreamTracker.on_channel_raid: detected raid")
            self.active_stream.add_raid(data.event.from_broadcaster_user_name, get_time(), data.event.viewers)
        
    
    async def on_stream_online(self, data: StreamOnlineEvent):
        self.active_stream = stream_instance()
        logging.info("StreamTracker.on_stream_online: recording")
        streaminfo: ChannelInformation = self.event_Handler.TwitchAPI.get_stream_info()
        self.active_stream.add_title(streaminfo.title,get_time())
    
    async def on_stream_offline(self, data: StreamOfflineEvent):
        if self.check_if_recording() != True:
            logging.info("StreamTracker.on_stream_offline: not recording")
            pass
        else:
            self.active_stream.end_stream()
            logging.info("StreamTracker.on_stream_offline: stream ended")
            self.reocorced_streams.append(self.active_stream)
            self.active_stream = None
    
    async def on_shoutout_received(self, data: ChannelShoutoutReceiveEvent):
        if self.check_if_recording() != True:
            logging.info("StreamTracker.on_shoutout_received: not recording")
            pass
        else:
            logging.info("StreamTracker.on_shoutout_received: detected shoutout")
            self.active_stream.add_shoutout(data.user.name, get_time())
        
    
    async def on_message(self, data: ChatMessage):
        if self.check_if_recording() != True:
            logging.info("StreamTracker.on_message: not recording")
            pass
        else:
            logging.info("StreamTracker.on_message: detected message")
            self.active_stream.add_message(data.user.name)
        
    async def on_webfrontend_message(self, command:str):
        if command == "streamstream":
            logging.info("testing start stream")
            await self.fake_start_stream()
        elif command == "endstream":
            logging.info("testing end stream")
            await self.fake_end_stream()
    
    async def fake_start_stream(self):
        '''this is for testing purposes only'''
        self.active_stream = stream_instance()
        logging.info("StreamTracker.test_on_stream_online: recording")
        streaminfo: ChannelInformation = await self.event_Handler.TwitchAPI.get_channel_info()
        #logging.info(streaminfo[0].title)
        self.active_stream.add_title(streaminfo[0].title,get_time())
        pass
    
    async def fake_end_stream(self):
        '''this is for testing purposes only'''
        if self.check_if_recording() != True:
            logging.info("StreamTracker.on_stream_offline: not recording")
            pass
        else:
            self.active_stream.end_stream()
            logging.info("StreamTracker.test_on_stream_offline: stream ended")
            self.reocorced_streams.append(self.active_stream)
            self.active_stream = None
        pass

    def __init__(self, event_handler: EventHandler):
        super().__init__("stream_tracker",event_handler)
        
        self.active_stream: stream_instance = None
        self.reocorced_streams: list[stream_instance] = []
