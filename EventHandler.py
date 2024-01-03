from Module import Module
from twitchAPI.object.eventsub import ChannelFollowEvent, ChannelBanEvent
from twitchAPI.chat import ChatMessage

class EventHandler:
    TwitchAPI = None
    DBConn = None
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
    def on_message(self, data: ChatMessage):
        # print(f'{msg.user.name}: {msg.text}')
        for Module in self.Modules:
            Module.on_message(data)
        
    
    
    #------- event sub events -------   
    def on_channel_update(self, data):
        for Module in self.Modules:
            Module.on_channel_update(data)    
        
    # on_follow
    def on_follow(self, data: ChannelFollowEvent):
        #print(f'{data.event.user_name} followed, called from EventHandler')
        for Module in self.Modules:
            Module.on_follow(data)    
    
    def on_subscribe(self, data):
        for Module in self.Modules:
            Module.on_subscribe(data)    
    
    def on_subscription_gift(self, data):
        for Module in self.Modules:
            Module.on_subscription_gift(data)
    
    def on_subscription_message(self, data):
        for Module in self.Modules:
            Module.on_subscription_message(data)
    
    def on_cheer(self, data):
        for Module in self.Modules:
            Module.on_cheer(data)
    
    def on_raid(self, data):
        for Module in self.Modules:
            Module.on_raid(data)
    
    # on_ban
    def on_ban(self, data: ChannelBanEvent):
        for Module in self.Modules:
            Module.on_ban(data)
    
    def on_unban(self, data):
        for Module in self.Modules:
            Module.on_unban(data)
    
    def on_moderator_add(self, data):
        for Module in self.Modules:
            Module.on_moderator_add(data)
    
    def on_moderator_remove(self, data):
        for Module in self.Modules:
            Module.on_moderator_remove(data)
    
    def on_channel_points_custom_reward_add(self, data):
        for Module in self.Modules:
            Module.on_channel_points_redeem_reward_add(data)
    
    def on_channel_points_custom_reward_update(self, data):
        for Module in self.Modules:
            Module.on_channel_points_redeem_reward_update(data)
    
    def on_channel_points_custom_reward_remove(self, data):
        for Module in self.Modules:
            Module.on_channel_points_redeem_reward_remove(data)
    
    def on_channel_points_reward_redeem(self, data):
        for Module in self.Modules:
            Module.on_channel_points_redeem(data)
    
    def on_channel_points_reward_redeem_update(self, data):
        for Module in self.Modules:
            Module.on_channel_points_redeem_update(data)
    
    def on_poll_begin(self, data):
        for Module in self.Modules:
            Module.on_channel_poll_begin(data)
    
    def on_poll_progress(self, data):
        for Module in self.Modules:
            Module.on_channel_poll_progress(data)
    
    def on_poll_end(self, data):
        for Module in self.Modules:
            Module.on_channel_poll_end(data)
    
    def on_stream_online(self, data):
        for Module in self.Modules:
            Module.on_stream_online(data)
    
    def on_stream_offline(self, data):
        for Module in self.Modules:
            Module.on_stream_offline(data)
            
    def on_shoutout_create(self, data):
        for Module in self.Modules:
            Module.on_shoutout_create(data)
    
    def on_shoutout_recieve(self, data):
        for Module in self.Modules:
            Module.on_shoutout_received(data)
    
    def on_chat_clear(self, data):
        for Module in self.Modules:
            Module.on_channel_chat_clear(data)
    
    def on_chat_clear_user_messages(self, data):
        for Module in self.Modules:
            Module.on_channel_chat_clear_user_messages(data)
    
    def on_chat_delete_messages(self, data):
        for Module in self.Modules:
            Module.on_channel_chat_message_delete(data)
