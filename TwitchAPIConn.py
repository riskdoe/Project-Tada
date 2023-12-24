from collections.abc import Callable, Iterable, Mapping
from typing import Any
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator, UserAuthenticationStorageHelper
from twitchAPI.type import AuthScope, ChatEvent, TwitchAPIException
from twitchAPI.chat import Chat, EventData, ChatMessage
from flask import Flask, redirect, request
from pathlib import PurePath
import asyncio



APP_ID = None
APP_SECRET = None
TARGET_CHANNEL = None
EVENT_HANDLER = None
TARGET_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]


app = Flask(__name__)
twitch: Twitch
auth: UserAuthenticator

#assign self to Event handler #TODO: finish event handler

    
@app.route('/login')
def login(self):
    return redirect(auth.return_auth_url())


@app.route('/login/confirm')
async def login_confirm():
    state = request.args.get('state')
    if state != auth.state:
        return 'Bad state', 401
    code = request.args.get('code')
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
    await ready_event.chat.send_message(TARGET_CHANNEL, 'alive and kicking!')
    
#will be called when ever a message is sent to target channel
async def on_message(msg: ChatMessage):
    # print(f'{msg.user.name}: {msg.text}')
    pass


async def twitch_setup():
    global twitch, auth
    print(APP_ID)

    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, TARGET_SCOPE)
    helper = UserAuthenticationStorageHelper(
        twitch,
        TARGET_SCOPE,
        storage_path=PurePath('./file.json'
    ))
    await helper.bind()
    # target channels
    chat = await Chat(twitch)
    
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    
    #start chat
    chat.start()
    try:
        input('press Enter to shut down...\n')
    except KeyboardInterrupt:
        pass
    finally:
        chat.stop()
        await twitch.close()
    
    
    
    
def run(channel, clientID, clientSecret):
    global APP_ID, APP_SECRET, TARGET_CHANNEL, EVENT_HANDLER
    APP_ID = clientID
    APP_SECRET = clientSecret
    TARGET_CHANNEL = channel
    print("app id: " + APP_ID)
    print("app secret: " + APP_SECRET)
    print("target channel: " + TARGET_CHANNEL)
    asyncio.run(twitch_setup())
