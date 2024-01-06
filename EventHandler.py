import asyncio
from Module import Module
from twitchAPI.object.eventsub import ChannelFollowEvent, ChannelBanEvent
from twitchAPI.chat import ChatMessage

class EventHandler:
    TwitchAPI = None
    DBConn = None
    commands = {}
    Modules: list[Module] = []
    counter = 1

    def __init__(self):
        super().__init__()
        
    #assign twitch api  
    def assign_to_twitch(self, TwitchAPI):
        self.TwitchAPI = TwitchAPI
    
    def assign_to_DBConn(self, DBConn):
        self.DBConn = DBConn
    
    #add module
    def AddModule(self, Module: Module):
        self.Modules.append(Module)
    

      
    #------- chat bot events -------  
        
    # on_message
    async def on_message(self, data: ChatMessage):
        # print(f'{msg.user.name}: {msg.text}')
        for Module in self.Modules:
            await Module.on_message(data)
            
    # send message
    async def send_message(self, message):
        await self.TwitchAPI.send_message(message)
        
    # send whisper
    async def send_whisper(self, user, message):
        await self.TwitchAPI.send_whisper(user, message)
        
    def Get_commands(self):
        return self.commands
        
    def Add_command(self, command, function):
        self.commands[command] = function
        
    #------- API events -------
    
    
    
    #------- event sub events -------   
    async def on_channel_update(self, data):
        for Module in self.Modules:
            await Module.on_channel_update(data)    
        
    # on_follow
    async def on_follow(self, data: ChannelFollowEvent):
        #print(f'{data.event.user_name} followed, called from EventHandler')
        for Module in self.Modules:
            await Module.on_follow(data)    
    
    async def on_subscribe(self, data):
        for Module in self.Modules:
            await Module.on_subscribe(data)    
    
    async def on_subscription_gift(self, data):
        for Module in self.Modules:
            await Module.on_subscription_gift(data)
    
    async def on_subscription_message(self, data):
        for Module in self.Modules:
            await Module.on_subscription_message(data)
    
    async def on_cheer(self, data):
        for Module in self.Modules:
            await Module.on_cheer(data)
    
    async def on_raid(self, data):
        for Module in self.Modules:
            await Module.on_raid(data)
    
    # on_ban
    async def on_ban(self, data: ChannelBanEvent):
        for Module in self.Modules:
            await Module.on_ban(data)
    
    async def on_unban(self, data):
        for Module in self.Modules:
            await Module.on_unban(data)
    
    async def on_moderator_add(self, data):
        for Module in self.Modules:
            await Module.on_moderator_add(data)
    
    async def on_moderator_remove(self, data):
        for Module in self.Modules:
            await Module.on_moderator_remove(data)
    
    async def on_channel_points_custom_reward_add(self, data):
        for Module in self.Modules:
            await Module.on_channel_points_redeem_reward_add(data)
    
    async def on_channel_points_custom_reward_update(self, data):
        for Module in self.Modules:
            await Module.on_channel_points_redeem_reward_update(data)
    
    async def on_channel_points_custom_reward_remove(self, data):
        for Module in self.Modules:
            await Module.on_channel_points_redeem_reward_remove(data)
    
    async def on_channel_points_reward_redeem(self, data):
        for Module in self.Modules:
            await Module.on_channel_points_redeem(data)
    
    async def on_channel_points_reward_redeem_update(self, data):
        for Module in self.Modules:
            await Module.on_channel_points_redeem_update(data)
    
    async def on_poll_begin(self, data):
        for Module in self.Modules:
            await Module.on_channel_poll_begin(data)
    
    async def on_poll_progress(self, data):
        for Module in self.Modules:
            await Module.on_channel_poll_progress(data)
    
    async def on_poll_end(self, data):
        for Module in self.Modules:
            await Module.on_channel_poll_end(data)
    
    async def on_stream_online(self, data):
        for Module in self.Modules:
            await Module.on_stream_online(data)
    
    async def on_stream_offline(self, data):
        for Module in self.Modules:
            await Module.on_stream_offline(data)
            
    async def on_shoutout_create(self, data):
        for Module in self.Modules:
            await Module.on_shoutout_create(data)
    
    async def on_shoutout_recieve(self, data):
        for Module in self.Modules:
            await Module.on_shoutout_received(data)
    
    async def on_chat_clear(self, data):
        for Module in self.Modules:
            await Module.on_channel_chat_clear(data)
    
    async def on_chat_clear_user_messages(self, data):
        for Module in self.Modules:
            await Module.on_channel_chat_clear_user_messages(data)
    
    async def on_chat_delete_messages(self, data):
        for Module in self.Modules:
            await Module.on_channel_chat_message_delete(data)
