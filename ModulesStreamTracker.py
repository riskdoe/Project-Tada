import asyncio
from Module import Module
from EventHandler import EventHandler
from twitchAPI.object.eventsub import *
from twitchAPI.chat import ChatMessage
from twitchAPI.object.api import ChannelInformation,GetChattersResponse
import time
from datetime import datetime
from StreamClasses import *
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_htmx import htmx, htmx_init

def get_time():
    return int(time.time())

streamcordingactive = False
streamstarttime = ""
streamTitle = ""
streamgame = ""
streamfollows = ""
streamsubs = ""
streamgiftsubs = ""
streamraids = ""
streamcheers = ""
streamshoutouts = ""
streammumberofactivechatters = ""
streamnumberofmessages = ""



router = APIRouter()

htmx_init(templates = Jinja2Templates(directory="templates"))

def construct_stream_info():
    if streamcordingactive:
        return {
            "starttime": streamstarttime,
            "title": streamTitle,
            "game": streamgame,
            "follows": streamfollows,
            "subs": streamsubs,
            "giftsubs": streamgiftsubs,
            "raids": streamraids,
            "cheers": streamcheers,
            "shoutouts": streamshoutouts,
            "mumberofactivechatters": streammumberofactivechatters,
            "numberofmessages": streamnumberofmessages,
        }
    else:
        return {
            "starttime": "00:00",
            "title": "No Stream",
            "game": "No Stream",
            "follows": "0",
            "subs": "0",
            "giftsubs": "0",
            "raids": "0",
            "cheers": "0",
            "shoutouts": "0",
            "mumberofactivechatters": "0",
            "numberofmessages": "0",
        }


@router.get("/streamstats", response_class=HTMLResponse)
@htmx("streamstats", "index", construct_stream_info)
def streamstats(request: Request):
    pass

class stream_instance():
    def __init__(self, caller, stream_id:int):
        self.owner = caller
        self.stream_id = stream_id
        
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
        self.update_time = caller.event_Handler.config.worker_update_rate
        self.veiwer_watchtime = {}
        self.active = True
        global streamcordingactive
        streamcordingactive = True
        
        
        self.veiwer_total_watchtime = {}

        for user in self.owner.event_Handler.DBConn.get_all_user_watchtime():
            self.veiwer_total_watchtime[user[0]] = user[1]
        
        
        global streamstarttime

        streamstarttime = datetime.now().strftime("%H:%M")


        
    
    async def check_for_chatters(self):
        chattersresponse : GetChattersResponse = await self.owner.event_Handler.TwitchAPI.get_chat_users()
        chatters = chattersresponse.data
        for chatter in chatters:
            
            name = chatter.user_name.lower()
            
            
            if name not in self.veiwer_total_watchtime:
                self.veiwer_total_watchtime[name] = self.update_time
                self.owner.event_Handler.DBConn.addveiwer(name, self.veiwer_total_watchtime[name])
            else:

                self.veiwer_total_watchtime[name] += self.update_time
                self.owner.event_Handler.DBConn.updatetotalwatchtime(name, self.veiwer_total_watchtime[name])

            if name not in self.veiwer_watchtime:
                self.veiwer_watchtime[name] = 0
            else:
                self.veiwer_watchtime[name] += self.update_time
        

    def updatewasrun(self):            
        global  streamfollows, streamsubs, streamgiftsubs, streamraids, streamcheers, streamshoutouts, streammumberofactivechatters, streamnumberofmessages
        streamfollows = len(self.follows_during_stream)
        streamsubs = len(self.subs_during_stream)
        streamgiftsubs = len(self.giftsubs_during_stream)
        streamraids = len(self.raids_during_stream)
        streamcheers = len(self.cheers_during_stream)
        streamshoutouts = len(self.shoutouts_during_stream)
        streammumberofactivechatters = len(self.active_chatter)
        streamnumberofmessages = self.num_of_messages_during_stream
        
        

    def end_stream(self):
        self.stream_end_time = get_time()
        self.stream_duration = self.stream_end_time - self.stream_start_time
        self.active = False
        global streamcordingactive
        streamcordingactive = False
        self.updatewasrun()

    def add_title(self, streamtitle, changetime):
        global streamTitle
        streamTitle = streamtitle
        self.stream_title.append(title(streamtitle, changetime))
        self.updatewasrun()

    
    def add_game(self, newgame, changetime):
        global streamgame
        streamgame = newgame
        self.stream_game.append(game(newgame, changetime))
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
            pass
        else:
            self.active_stream.add_title(data.event.title, get_time())
            self.active_stream.add_game(data.event.category_name, get_time())
    
    async def on_channel_follow(self, data: ChannelFollowEvent):
        if self.check_if_recording() != True:
            pass
        else:
            self.active_stream.add_follow(data.event.user_name, get_time())
    
    async def on_channel_subscribe(self, data: ChannelSubscribeEvent):
        if self.check_if_recording() != True:
            pass
        else:
            self.active_stream.add_sub(data.event.user_name, get_time(), data.event.tier) 
    
    async def on_channel_subscription_gift(self, data: ChannelSubscriptionGiftEvent):
        if self.check_if_recording() != True:
            pass
        else:
            username = ""
            if data.event.is_anonymous:
                username = "Anonymous"
            else:
                username = data.event.user_name
            self.active_stream.add_subgift(username, get_time(), data.event.tier, data.event.total, submessage = data.event.message)
                
    async def on_channel_subscription_message(self, data: ChannelSubscriptionMessageEvent):
        if self.check_if_recording() != True:
            pass
        else:
            self.active_stream.add_sub(data.event.user_name, get_time(), data.event.tier, resub = True , submessage = data.event.message)
        
    
    async def on_channel_cheer(self, data: ChannelCheerEvent):
        if self.check_if_recording() != True:
            pass
        else:
            username = ""
            if data.event.is_anonymous:
                username = "Anonymous"
            else:
                username = data.event.user_name
            self.active_stream.add_cheer(username, get_time(), data.event.bits, data.event.message)
    
    async def on_channel_raid(self, data: ChannelRaidEvent):
        if self.check_if_recording() != True:
            pass
        else:
            self.active_stream.add_raid(data.event.from_broadcaster_user_name, get_time(), data.event.viewers)
        
    
    async def on_stream_online(self, data: StreamOnlineEvent):
        streamid = self.event_Handler.DBConn.getnextStreamID()
        self.active_stream = stream_instance(self,streamid)
        await self.active_stream.check_for_chatters()
        #await self.active_stream.start_worker()
        self.event_Handler.loginfo(self.name, ".on_stream_online: recording")
        streaminfo: ChannelInformation = await self.event_Handler.TwitchAPI.get_channel_info()
        self.active_stream.add_title(streaminfo[0].title,get_time())
        self.active_stream.add_game(streaminfo[0].game_name,get_time())
        self.event_Handler.go_live(streamid)

    
    async def on_stream_offline(self, data: StreamOfflineEvent):
        if self.check_if_recording() != True:
            pass
        else:
            self.event_Handler.loginfo(self.name, ".on_stream_offline: stream ended")
            self.active_stream.end_stream()
            self.reocorced_streams.append(self.active_stream)
            self.active_stream = None
            self.event_Handler.go_offline()
    
    async def on_shoutout_received(self, data: ChannelShoutoutReceiveEvent):
        if self.check_if_recording() != True:
            pass
        else:
            self.active_stream.add_shoutout(data.user.name, get_time())
        
    
    async def on_message(self, data: ChatMessage):
        if self.check_if_recording() != True:
            pass
        else:
            self.active_stream.add_message(data.user.name)
        
    async def on_webfrontend_message(self, command:str):
        if command == "startstream":
            await self.fake_start_stream()
        elif command == "endstream":
            await self.fake_end_stream()
    
    async def fake_start_stream(self):
        '''this is for testing purposes only'''
        streamid = self.event_Handler.DBConn.getnextStreamID()
        self.active_stream = stream_instance(self,streamid)
        await self.active_stream.check_for_chatters()
        #await self.active_stream.start_worker()
        self.event_Handler.loginfo(self.name, ".on_stream_online: recording")
        streaminfo: ChannelInformation = await self.event_Handler.TwitchAPI.get_channel_info()
        self.active_stream.add_title(streaminfo[0].title,get_time())
        self.active_stream.add_game(streaminfo[0].game_name,get_time())
        self.event_Handler.go_live(streamid)

    
    async def fake_end_stream(self):
        '''this is for testing purposes only'''
        if self.check_if_recording() != True:
            self.event_Handler.loginfo(self.name, ".on_stream_offline: not recording")
        elif self.check_if_recording() == True:
            self.active_stream.end_stream()
            self.event_Handler.loginfo(self.name, ".on_stream_offline: stream ended")
            #self.reocorced_streams.append(self.active_stream)
            self.event_Handler.DBConn.add_stream(self.active_stream)
            self.active_stream = None
            self.event_Handler.go_offline()
            #write stream details to db

    async def do_worker(self):
        if self.check_if_recording():
            await self.active_stream.check_for_chatters()



    def __init__(self, event_handler: EventHandler):
        super().__init__("stream_tracker",event_handler)
        
        self.active_stream: stream_instance = None
        self.reocorced_streams: list[stream_instance] = []
