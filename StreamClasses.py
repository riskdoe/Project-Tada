from twitchAPI.object.eventsub import *
from twitchAPI.chat import ChatMessage
from twitchAPI.object.api import ChannelInformation,GetChattersResponse
import time
from datetime import datetime
import asyncio
import logging

def get_time():
    return int(time.time())

class title():
    def __init__(self, title, changetime):
        self.title = title
        self.event_time = changetime

class game():
    def __init__(self, game, changetime):
        self.game = game
        self.event_time = changetime

class follow():
    def __init__(self, user, followtime):
        self.user = user
        self.event_time = followtime
        
class sub():
    def __init__(self, user, subtime, sublevel, resub = False, submessage:str = None):
        self.user = user
        self.event_time = subtime
        self.submessage = submessage
        self.sublevel = sublevel
        self.resub = resub

class subgift():
    def __init__(self, user, subtime, sublevel, count, submessage:str = None):
        self.user = user
        self.event_time = subtime
        self.submessage = submessage
        self.sublevel = sublevel
        self.count = count

class raid():
    def __init__(self, user, raidtime, raiders):
        self.user = user
        self.event_time = raidtime
        self.numberofraiders = raiders

class cheer():
    def __init__(self, user, cheertime, bits, message:str = None):
        self.user = user
        self.event_time = cheertime
        self.bits = bits
        self.message = message

class shoutout():
    def __init__(self, user, shoutouttime):
        self.user = user
        self.event_time = shoutouttime
        

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
        logging.info(f"stream_instance.__init__: update time is {self.update_time}")
        self.veiwer_watchtime = {}
        self.active = True
        
        
        self.veiwer_total_watchtime = {}

        for user in self.owner.event_Handler.DBConn.get_all_user_watchtime():
            self.veiwer_total_watchtime[user[0]] = user[1]
        logging.info(self.veiwer_total_watchtime)

        
    
    async def check_for_chatters(self):
        logging.debug("stream_instance.check_for_chatters: checking for chatters")
        chattersresponse : GetChattersResponse = await self.owner.event_Handler.TwitchAPI.get_chat_users()
        chatters = chattersresponse.data
        logging.info(f"stream_instance.check_for_chatters: checking for chatters, time:{datetime.utcfromtimestamp(get_time()).strftime('%H:%M')}")
        for chatter in chatters:
            
            name = chatter.user_name.lower()
            
            logging.info(f"stream_instance.check_for_chatters: {name} was found")
            
            if name not in self.veiwer_total_watchtime:
                logging.info(f"stream_instance.check_for_chatters: new chatter {name} was found, added")
                self.veiwer_total_watchtime[name] = self.update_time
                self.owner.event_Handler.DBConn.addveiwer(name, self.veiwer_total_watchtime[name])
            else:

                self.veiwer_total_watchtime[name] += self.update_time
                logging.info(f"stream_instance.check_for_chatters: {name} was found, updated new points {self.veiwer_total_watchtime[name]}")
                self.owner.event_Handler.DBConn.updatetotalwatchtime(name, self.veiwer_total_watchtime[name])

            if name not in self.veiwer_watchtime:
                self.veiwer_watchtime[name] = 0
                logging.debug(f"stream_instance.check_for_chatters: new chatter {name} was found, added")                
            else:
                self.veiwer_watchtime[name] += self.update_time
                logging.debug(f"stream_instance.check_for_chatters: {name} was found, updated")
        
    # async def start_worker(self):
    #     while self.active:
    #         logging.info("loop2")
    #         await asyncio.gather(
    #         asyncio.sleep(self.update_time),
    #         self.check_for_chatters(),
    #         )    
        

    def updatewasrun(self):
        logging.info("stream_instance.updatewasrun: update was run")
        logging.info(f"stream_instance.updatewasrun: {self.stream_start_time} was start time")
        logging.info(f"stream_instance.updatewasrun: {self.num_of_messages_during_stream} messages were sent")
        logging.debug(f"stream_instance.updatewasrun: {len(self.active_chatter)} chatters were active")
        logging.debug(f"stream_instance.updatewasrun: {len(self.follows_during_stream)} follows were made")
        logging.debug(f"stream_instance.updatewasrun: {len(self.subs_during_stream)} subs were made")
        logging.debug(f"stream_instance.updatewasrun: {len(self.giftsubs_during_stream)} gift subs were made")
        logging.debug(f"stream_instance.updatewasrun: {len(self.raids_during_stream)} raids were made")
        logging.debug(f"stream_instance.updatewasrun: {len(self.cheers_during_stream)} cheers were made")
        logging.debug(f"stream_instance.updatewasrun: {len(self.shoutouts_during_stream)} shoutouts were made")
        if(self.stream_end_time != None):
            logging.debug(f"stream_instance.updatewasrun: {self.stream_end_time} was end time")
            logging.debug(f"stream_instance.updatewasrun: {self.stream_duration} was duration")
        
        

    def end_stream(self):
        self.stream_end_time = get_time()
        self.stream_duration = self.stream_end_time - self.stream_start_time
        self.active = False
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

