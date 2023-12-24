#chat log module
from Module import Module
from EventHandler import EventHandler
from twitchAPI.chat import ChatMessage


class ChatLog(Module):
    def __init__(self, eventHandler: EventHandler):
        super().__init__("ChatLog" , eventHandler)
#data: ChatMessage
    def on_message(self, data):
        print(f'{data.user.name}: {data.text}')