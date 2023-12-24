from Module import Module

class EventHandler:
    TwitchAPI = None
    Modules: list = []
    counter = 1

    def __init__(self):
        super().__init__()
        
    #assign twitch api  
    def assign_to_twitch(self, TwitchAPI):
        self.TwitchAPI = TwitchAPI
        
    #add module
    def AddModule(self, Module: Module):
        self.Modules.append(Module)
        
    # on_message
    def on_message(self, data):
        # print(f'{msg.user.name}: {msg.text}')
        for Module in self.Modules:
            Module.on_message(data)