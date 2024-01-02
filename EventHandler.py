from Module import Module
from twitchAPI.object.eventsub import ChannelFollowEvent, ChannelBanEvent
from twitchAPI.chat import ChatMessage

class EventHandler:
    TwitchAPI = None
    DBConn = None
    Modules: list = []
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

        
    # on_message
    def on_message(self, data: ChatMessage):
        # print(f'{msg.user.name}: {msg.text}')
        for Module in self.Modules:
            Module.on_message(data)
        
    # on_follow
    def on_follow(self, data: ChannelFollowEvent):
        #print(f'{data.event.user_name} followed, called from EventHandler')
        for Module in self.Modules:
            Module.on_follow(data)    
            
    # on_ban
    def on_ban(self, data: ChannelBanEvent):
        for Module in self.Modules:
            Module.on_ban(data)
            