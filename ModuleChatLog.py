#chat log module
from Module import Module
from fastapi import APIRouter
from EventHandler import EventHandler
from twitchAPI.chat import ChatMessage
import logging

messages = []
router = APIRouter()
@router.get("/messages")
def get_messages():
    return messages


class ChatLog(Module):
    def __init__(self, eventHandler: EventHandler):
        super().__init__("ChatLog" , eventHandler)
#data: ChatMessage
    def on_message(self, data):
        messages.append(f"{data.user.name}: {data.text}")
        logging.info(f'{self.name}: {data.user.name}: {data.text}')
        

