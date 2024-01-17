#chat log module
from Module import Module
from fastapi import APIRouter
from EventHandler import EventHandler
from twitchAPI.chat import ChatMessage
import logging
import re as regex

class cmessage():
    def __init__(self,
                 id: str,
                 user: str,
                 text: str,
                 timestamp: int):
        self.id = id
        self.user = user
        self.text = text
        self.timestamp = timestamp
    
    def __str__(self):
        return f"{self.user}: {self.text}"


messages: list[cmessage] = []
router = APIRouter()
@router.get("/messages")
def get_messages():
    
    return messages


class ChatLog(Module):
    def __init__(self, eventHandler: EventHandler):
        super().__init__("ChatLog" , eventHandler)
        logging.info("ChatLog module loaded")
        self.reg = "/[^a-z0-9]/gi"
#data: ChatMessage
    async def on_message(self, data: ChatMessage):
        text = regex.sub('[^0-9a-zA-Z:)(]+', ' ', data.text)
        message = cmessage(data.id, data.user.name, text, data.sent_timestamp)
        messages.append(message)
        logging.info(f'{self.name}: {data.user.name}: {text}')
        self.event_Handler.DBConn.AddMessage(message)


