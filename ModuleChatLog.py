#chat log module
from Module import Module
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_htmx import htmx, htmx_init
from pathlib import Path
from EventHandler import EventHandler
from twitchAPI.chat import ChatMessage
import logging
import re as regex

class cmessage():
    def __init__(self,
                 ident: str,
                 user: str,
                 text: str,
                 timestamp: int):
        self.id = ident
        self.user = user
        self.text = text
        self.timestamp = timestamp
    
    def __str__(self):
        return f"{self.user}: {self.text}"


messages: list[cmessage] = []
router = APIRouter()

htmx_init(templates = Jinja2Templates(directory="templates"))

def construct_messages():
    out = []
    for message in messages:
        out.append([message.id, message.user, message.text])
    if out == []:
        return {"messages": [["", "", "No messages yet!"]]}
    tofrontend = out[::-1]
    
    if len(tofrontend) > 250:
        tofrontend = tofrontend[:250]
    logging.info(f"Sending {len(tofrontend)} messages to frontend")
    
    return {"messages": tofrontend}

@router.get("/messages", response_class=HTMLResponse)
@htmx("chat-messages", "index", construct_messages)
async def get_messages(request: Request):
    pass


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
    
    async def on_webfrontend_message(self, command):
        
        if "Send_message" in command:
            output = cmessage("0", "(tada)", command["Send_message"], 0)
            messages.append(output)


