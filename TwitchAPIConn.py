from collections.abc import Callable, Iterable, Mapping
from typing import Any
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator, UserAuthenticationStorageHelper
from twitchAPI.type import AuthScope, ChatEvent, TwitchAPIException
from twitchAPI.chat import Chat, EventData, ChatMessage
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from EventHandler import EventHandler
from pathlib import PurePath
import asyncio
import logging


#copy paste of imports from eventsub
from pathlib import PurePath
from twitchAPI.helper import first
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticationStorageHelper
from twitchAPI.object.eventsub import ChannelFollowEvent, ChannelBanEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from EventHandler import EventHandler
from twitchAPI.type import AuthScope


APP_ID = None
APP_SECRET = None
TARGET_CHANNEL = None
EVENT_HANDLER : EventHandler = None
TARGET_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT,AuthScope.MODERATOR_READ_FOLLOWERS, AuthScope.CHANNEL_MODERATE]


app = FastAPI()
twitch: Twitch
auth: UserAuthenticator

#assign self to Event handler #TODO: finish event handler

    
@app.route('/login')
def login(self):
    return RedirectResponse(auth.return_auth_url())


@app.route('/login/confirm')
async def login_confirm():
    state = Request.args.get('state')
    if state != auth.state:
        return 'Bad state', 401
    code = Request.args.get('code')
    if code is None:
        return 'Missing code', 400
    try:
        token, refresh = await auth.authenticate(user_token=code)
        await twitch.set_user_authentication(token, TARGET_SCOPE, refresh)
    except TwitchAPIException as e:
        return 'Failed to generate auth token', 400
    return 'Successfully authenticated!'

#will be called when the bot is ready so we can connect to target
async def on_ready(ready_event: EventData):
    # connect to channel
    await ready_event.chat.join_room(TARGET_CHANNEL)
    # inform the streamer we are connected
    #await ready_event.chat.send_message(TARGET_CHANNEL, f'Connected to {TARGET_CHANNEL}')
    
#will be called when ever a message is sent to target channel
async def on_message(msg: ChatMessage):
    # logging.info(f'{msg.user.name}: {msg.text}')
    #print(EVENT_HANDLER)
    EVENT_HANDLER.on_message(data = msg)
    pass

#on follow events
async def on_follow(data: ChannelFollowEvent):
    # our event happened, lets do things with the data we got!
    #print(f'{data.event.user_name} now follows {data.event.broadcaster_user_name}!')
    EVENT_HANDLER.on_follow(data)
    
#on ban events
async def on_ban(data: ChannelBanEvent):
    EVENT_HANDLER.on_ban(data)


async def twitch_setup():
    global twitch, auth
    global TARGET_CHANNEL
    #logging.info(APP_ID)
    
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, TARGET_SCOPE)
    helper = UserAuthenticationStorageHelper( twitch, TARGET_SCOPE, storage_path=PurePath('./oauth.json'))
    await helper.bind()
    
    #get target channel
    user = await first(twitch.get_users())
    TARGET_CHANNEL = user.login
    logging.info("target channel: " + TARGET_CHANNEL)
    
    # target channels
    chat = await Chat(twitch)
    
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    
    #start chat
    chat.start()
    
    #test to see if we can run the websocket here
    user = await first(twitch.get_users())
    
    # create eventsub websocket for all end points and send them to eventhandler
    eventsub = EventSubWebsocket(twitch)
    eventsub.start()
    
    #add events. these will be send over to event handler
    
    await eventsub.listen_channel_follow_v2(user.id, user.id, on_follow)
    await eventsub.listen_channel_ban(user.id, on_ban)
    
    
    try:
        input('enter to exit\n')
    except KeyboardInterrupt:
        pass
    finally:
        chat.stop()
        await twitch.close()
        logging.info("twitch connection closed")
        exit()
    
    
    
    
def run( clientID, clientSecret, EventHandler: EventHandler):
    global APP_ID, APP_SECRET, TARGET_CHANNEL, EVENT_HANDLER
    APP_ID = clientID
    APP_SECRET = clientSecret
    EVENT_HANDLER = EventHandler
    
    logging.info("starting twitch chat connection")
    #logging.info("app id: " + APP_ID)
    #logging.info("app secret: " + APP_SECRET)
    asyncio.run(twitch_setup())
