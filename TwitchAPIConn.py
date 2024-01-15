#twitch auth
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.oauth import UserAuthenticator, UserAuthenticationStorageHelper
from pathlib import PurePath
from twitchAPI.type import AuthScope

#twitch chat imports
from twitchAPI.type import ChatEvent, TwitchAPIException
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatCommand


#twtich api imports
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.object.eventsub import *
from twitchAPI.object.api import GetChattersResponse
from twitchAPI.object.api import Chatter as twitchChatter

#fast Api
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from EventHandler import EventHandler

#other imports
import asyncio
import logging
from queue import Queue
from fastapi import APIRouter

#modules
from ModuleChatLog import ChatLog
from ModuleBanLog import BanLog
from ModuleCommandHandler import CommandHandler
from ModuleMiniGameSystem import MinigameSystem


TWITCH: Twitch
AUTH: UserAuthenticator
CHAT: Chat
PERMITTED_USERS:list[str] = []
COMMAND_QUEUE = Queue()

APP_ID = None
APP_SECRET = None
HOST_CHANNEL = None
HOST_CHANNEL_ID = None
EVENT_HANDLER : EventHandler = None
TARGET_SCOPE = [AuthScope.CHAT_READ,
                AuthScope.USER_READ_CHAT,
                AuthScope.CHAT_EDIT,
                AuthScope.CHANNEL_BOT,
                AuthScope.MODERATOR_READ_FOLLOWERS,
                AuthScope.CHANNEL_READ_SUBSCRIPTIONS,
                AuthScope.BITS_READ,
                AuthScope.CHANNEL_MANAGE_REDEMPTIONS,
                AuthScope.CHANNEL_MANAGE_POLLS,
                AuthScope.CHANNEL_MANAGE_PREDICTIONS,
                AuthScope.CHANNEL_READ_GOALS,
                AuthScope.MODERATOR_MANAGE_SHOUTOUTS,
                AuthScope.MODERATION_READ,
                AuthScope.CHANNEL_MODERATE,
                AuthScope.MODERATOR_MANAGE_BANNED_USERS,
                AuthScope.MODERATOR_READ_CHATTERS]

app = FastAPI()
    
@app.route('/login')
def login(self):
    return RedirectResponse(AUTH.return_auth_url())


@app.route('/login/confirm')
async def login_confirm():
    state = Request.args.get('state')
    if state != AUTH.state:
        return 'Bad state', 401
    code = Request.args.get('code')
    if code is None:
        return 'Missing code', 400
    try:
        token, refresh = await AUTH.authenticate(user_token=code)
        await TWITCH.set_user_authentication(token, TARGET_SCOPE, refresh)
    except TwitchAPIException as e:
        return 'Failed to generate auth token', 400
    return 'Successfully authenticated!'




#router for starting events in twitch thread
router = APIRouter()
@router.get("/start_trivia")
def start_event():
    global COMMAND_QUEUE
    COMMAND_QUEUE.put("start_trivia")
    return "event started"

#will be called when the bot is ready so we can connect to target
async def on_ready(ready_event: EventData):
    # connect to channel
    await ready_event.chat.join_room(HOST_CHANNEL)
    
#will be called when ever a message is sent to target channel
async def on_message(msg: ChatMessage):
    await EVENT_HANDLER.on_message(data = msg)
    pass

#we place all the on events for the event sub here

#on channel update
async def on_channel_update(data: ChannelUpdateEvent):
    await EVENT_HANDLER.on_channel_update(data)

#on follow events
async def on_follow(data: ChannelFollowEvent):
    await EVENT_HANDLER.on_follow(data)

#on sub events
async def on_sub(data: ChannelSubscribeEvent):
    await EVENT_HANDLER.on_subscribe(data)
    
#on sub gift
async def on_sub_gift(data: ChannelSubscriptionGiftEvent):
    await EVENT_HANDLER.on_sub_gift(data)
    
#on sub message 
async def on_sub_message(data: ChannelSubscriptionMessageEvent):
    await EVENT_HANDLER.on_sub_message(data)
    
#on cheer
async def on_cheer(data: ChannelCheerEvent):
    await EVENT_HANDLER.on_cheer(data)

#on raid
async def on_raid(data: ChannelRaidEvent):
    await EVENT_HANDLER.on_raid(data)

#on ban events
async def on_ban(data: ChannelBanEvent):
    await EVENT_HANDLER.on_ban(data)

#on unban events
async def on_unban(data: ChannelUnbanEvent):
    await EVENT_HANDLER.on_unban(data)

# on moderator add
async def on_moderator_add(data: ChannelModeratorAddEvent):
    await EVENT_HANDLER.on_moderator_add(data)
    
# on moderator remove
async def on_moderator_remove(data: ChannelModeratorRemoveEvent):
    await EVENT_HANDLER.on_moderator_remove(data)

#on channel points reward add
async def on_channel_points_reward_add(data: ChannelPointsCustomRewardAddEvent):
    await EVENT_HANDLER.on_channel_points_reward_add(data)
    
#on channel points reward update
async def on_channel_points_reward_update(data: ChannelPointsCustomRewardUpdateEvent):
    await EVENT_HANDLER.on_channel_points_reward_update(data)
    

#on channel points reward remove
async def on_channel_points_reward_remove(data: ChannelPointsCustomRewardRemoveEvent):
    await EVENT_HANDLER.on_channel_points_reward_remove(data)

#on channel points reward redeem
async def on_channel_points_reward_redeem(data: ChannelPointsCustomRewardRedemptionAddEvent):
    await EVENT_HANDLER.on_channel_points_reward_redeem(data)

#on channel points reward redeem update
async def on_channel_points_reward_redeem_update(data: ChannelPointsCustomRewardRedemptionUpdateEvent):
    await EVENT_HANDLER.on_channel_points_reward_redeem_update(data)
    
#on poll begin
async def on_poll_begin(data: ChannelPollBeginEvent):
    await EVENT_HANDLER.on_poll_begin(data)

#on poll progress
async def on_poll_progress(data: ChannelPollProgressEvent):
    await EVENT_HANDLER.on_poll_progress(data)
    
#on poll end
async def on_poll_end(data: ChannelPollEndEvent):
    await EVENT_HANDLER.on_poll_end(data)

#stream online
async def on_stream_online(data: StreamOnlineEvent):
    await EVENT_HANDLER.on_stream_online(data)

#stream offline
async def on_stream_offline(data: StreamOfflineEvent):
    await EVENT_HANDLER.on_stream_offline(data)

#on shoutout create
async def on_shoutout_create(data: ChannelShoutoutCreateEvent):
    await EVENT_HANDLER.on_shoutout_create(data)
    
#on shoutout recieve
async def on_shoutout_recieve(data: ChannelShoutoutReceiveEvent):
    await EVENT_HANDLER.on_shoutout_recieve(data)

#on ChatClear
async def on_chat_clear(data: ChannelChatClearEvent):
    await EVENT_HANDLER.on_chat_clear(data)
    
#on ChatClear usermessages
async def on_chat_clear_user_messages(data: ChannelChatClearUserMessagesEvent):
    await EVENT_HANDLER.on_chat_clear_user_messages(data)

#on chat delete messages
async def on_chat_delete_messages(data: ChannelChatMessageDeleteEvent):
    await EVENT_HANDLER.on_chat_delete_messages(data)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
#events to be called

#twitch
async def create_stream_maker(description: str):
    await TWITCH.create_stream_marker(HOST_CHANNEL_ID, description)

async def get_channel_info():
    return await TWITCH.get_channel_information(HOST_CHANNEL_ID)


async def start_ad(length: int):
    return await TWITCH.start_commercial(HOST_CHANNEL_ID, length)

async def start_raid(user: str):
    await TWITCH.start_raid(HOST_CHANNEL_ID, user)

async def cancel_raid():
    await TWITCH.cancel_raid(HOST_CHANNEL_ID)

async def shoutout(user: str):
    target = await first(TWITCH.get_users(logins=[user]))
    TWITCH.send_a_shoutout(HOST_CHANNEL_ID, target.id, HOST_CHANNEL_ID)
    
async def get_chat_users():
    return await TWITCH.get_chatters(HOST_CHANNEL_ID,HOST_CHANNEL_ID)


#chat
async def send_message(message: str):
    await CHAT.send_message(HOST_CHANNEL, message)

async def send_whisper(user: str, message: str):
    target = await first(TWITCH.get_users(logins=[user]))
    await CHAT.send_whisper(HOST_CHANNEL_ID,target.id, message)
    
async def ban_user(user: str, reason: str):
    target = await first(TWITCH.get_users(logins=[user]))
    logging.info(f"banning user: {target}")
    await TWITCH.ban_user(HOST_CHANNEL_ID, HOST_CHANNEL_ID, target.id, reason)

async def unban_user(user: str):
    target = await first(TWITCH.get_users(logins=[user]))
    await TWITCH.unban_user(HOST_CHANNEL_ID, HOST_CHANNEL_ID, target.id)
    
    
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

#create command
def add_command(command: str, handler):
        #commands
    CHAT.register_command(command, handler)
    
def remove_command(command: str):
    CHAT.unregister_command(command)
    

async def handle_command_blocked( cmd: ChatCommand):
    await cmd.reply(f'You are not allowed to use {cmd.name}!')

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

async def twitch_setup():
    global TWITCH, AUTH
    global HOST_CHANNEL, HOST_CHANNEL_ID
    global CHAT
    global PERMITTED_USERS
    
    TWITCH = await Twitch(APP_ID, APP_SECRET)
    AUTH = UserAuthenticator(TWITCH, TARGET_SCOPE)
    helper = UserAuthenticationStorageHelper( TWITCH, TARGET_SCOPE, storage_path=PurePath('./oauth.json'))
    await helper.bind()
    
    #get target channel
    user = await first(TWITCH.get_users())
    HOST_CHANNEL = user.login
    HOST_CHANNEL_ID = user.id
    logging.info("target channel: " + HOST_CHANNEL)
    
    # target channels
    CHAT = await Chat(TWITCH)
    
    CHAT.register_event(ChatEvent.READY, on_ready)
    CHAT.register_event(ChatEvent.MESSAGE, on_message)
    
    #start chat
    CHAT.start()
    CHAT.default_command_execution_blocked_handler = handle_command_blocked
    
    #test to see if we can run the websocket here
    user = await first(TWITCH.get_users())
    
    # create eventsub websocket for all end points and send them to eventhandler
    eventsub = EventSubWebsocket(TWITCH)
    eventsub.start()
    
    # add modules
    
    if(EVENT_HANDLER.config.chat_log):
        logging.info("adding chat log")
        chatLog = ChatLog(EVENT_HANDLER)
    if(EVENT_HANDLER.config.ban_log):
        logging.info("adding ban log")
        banLog = BanLog(EVENT_HANDLER)
    if(EVENT_HANDLER.config.basic_command):
        logging.info("adding command handler")
        commandHandler = CommandHandler(EVENT_HANDLER)
    if(EVENT_HANDLER.config.minigames):
        logging.info("adding minigame handler")
        miniGameHost = MinigameSystem(EVENT_HANDLER)
    
    EVENT_HANDLER.AddModule(chatLog)
    EVENT_HANDLER.AddModule(banLog)
    EVENT_HANDLER.AddModule(commandHandler)
    EVENT_HANDLER.AddModule(miniGameHost)
    
    #add all the commands
    commands = EVENT_HANDLER.Get_commands()
    
    for command in commands:
        add_command(command, commands[command])
    
    #add events. these will be send over to event handler
    await eventsub.listen_channel_update_v2(user.id, on_channel_update)
    await eventsub.listen_channel_follow_v2(user.id, user.id, on_follow)
    await eventsub.listen_channel_subscribe(user.id, on_sub)
    await eventsub.listen_channel_subscription_gift(user.id, on_sub_gift)
    await eventsub.listen_channel_subscription_message(user.id, on_sub_message)
    await eventsub.listen_channel_cheer(user.id, on_cheer)
    await eventsub.listen_channel_raid(on_raid, user.id)
    await eventsub.listen_channel_ban(user.id, on_ban)
    await eventsub.listen_channel_unban(user.id, on_unban)
    await eventsub.listen_channel_moderator_add(user.id, on_moderator_add)
    await eventsub.listen_channel_moderator_remove(user.id, on_moderator_remove)
    await eventsub.listen_channel_points_custom_reward_add(user.id, on_channel_points_reward_add)
    await eventsub.listen_channel_points_custom_reward_update(user.id, on_channel_points_reward_update)
    await eventsub.listen_channel_points_custom_reward_remove(user.id, on_channel_points_reward_remove)
    await eventsub.listen_channel_points_custom_reward_redemption_add(user.id, on_channel_points_reward_redeem)
    await eventsub.listen_channel_points_custom_reward_redemption_update(user.id, on_channel_points_reward_redeem_update)
    await eventsub.listen_channel_poll_begin(user.id, on_poll_begin)
    await eventsub.listen_channel_poll_progress(user.id, on_poll_progress)
    await eventsub.listen_channel_poll_end(user.id, on_poll_end)
    await eventsub.listen_stream_online(user.id, on_stream_online)
    await eventsub.listen_stream_offline(user.id, on_stream_offline)
    await eventsub.listen_channel_shoutout_create(user.id,user.id, on_shoutout_create)
    await eventsub.listen_channel_shoutout_receive(user.id,user.id, on_shoutout_recieve)
    await eventsub.listen_channel_chat_clear(user.id, user.id, on_chat_clear)
    await eventsub.listen_channel_chat_clear_user_messages(user.id, user.id, on_chat_clear_user_messages)
    await eventsub.listen_channel_chat_message_delete(user.id,user.id, on_chat_delete_messages)

    logging.info("twitch setup complete")
    while True:
        if not COMMAND_QUEUE.empty():
            command = COMMAND_QUEUE.get()
            logging.info(command)
            if command == "start_trivia":
                await EVENT_HANDLER.on_webfrontend_message(command)

def run( clientID, clientSecret, EventHandler: EventHandler):
    global APP_ID, APP_SECRET, HOST_CHANNEL, EVENT_HANDLER,PERMITTED_USERS
    APP_ID = clientID
    APP_SECRET = clientSecret
    EVENT_HANDLER = EventHandler
    PERMITTED_USERS = EventHandler.config.Super_moderators
    
    logging.info("starting twitch chat connection")
    asyncio.run(twitch_setup())
