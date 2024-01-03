#twitch auth
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.oauth import UserAuthenticator, UserAuthenticationStorageHelper
from pathlib import PurePath
from twitchAPI.type import AuthScope

#twitch chat imports
from twitchAPI.type import ChatEvent, TwitchAPIException
from twitchAPI.chat import Chat, EventData, ChatMessage

#twtich api imports
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.object.eventsub import *

#fast Api
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from EventHandler import EventHandler

#other imports
import asyncio
import logging

APP_ID = None
APP_SECRET = None
TARGET_CHANNEL = None
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
                AuthScope.CHANNEL_MODERATE]


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

#we place all the on events for the event sub here

#on channel update
async def on_channel_update(data: ChannelUpdateEvent):
    EVENT_HANDLER.on_channel_update(data)

#on follow events
async def on_follow(data: ChannelFollowEvent):
    # our event happened, lets do things with the data we got!
    #print(f'{data.event.user_name} now follows {data.event.broadcaster_user_name}!')
    EVENT_HANDLER.on_follow(data)

#on sub events
async def on_sub(data: ChannelSubscribeEvent):
    EVENT_HANDLER.on_subscribe(data)
    
#on sub gift
async def on_sub_gift(data: ChannelSubscriptionGiftEvent):
    EVENT_HANDLER.on_sub_gift(data)
    
#on sub message 
async def on_sub_message(data: ChannelSubscriptionMessageEvent):
    EVENT_HANDLER.on_sub_message(data)
    
#on cheer
async def on_cheer(data: ChannelCheerEvent):
    EVENT_HANDLER.on_cheer(data)

#on raid
async def on_raid(data: ChannelRaidEvent):
    EVENT_HANDLER.on_raid(data)

#on ban events
async def on_ban(data: ChannelBanEvent):
    EVENT_HANDLER.on_ban(data)

#on unban events
async def on_unban(data: ChannelUnbanEvent):
    EVENT_HANDLER.on_unban(data)

# on moderator add
async def on_moderator_add(data: ChannelModeratorAddEvent):
    EVENT_HANDLER.on_moderator_add(data)
    
# on moderator remove
async def on_moderator_remove(data: ChannelModeratorRemoveEvent):
    EVENT_HANDLER.on_moderator_remove(data)

#on channel points reward add
async def on_channel_points_reward_add(data: ChannelPointsCustomRewardAddEvent):
    EVENT_HANDLER.on_channel_points_reward_add(data)
    
#on channel points reward update
async def on_channel_points_reward_update(data: ChannelPointsCustomRewardUpdateEvent):
    EVENT_HANDLER.on_channel_points_reward_update(data)
    

#on channel points reward remove
async def on_channel_points_reward_remove(data: ChannelPointsCustomRewardRemoveEvent):
    EVENT_HANDLER.on_channel_points_reward_remove(data)

#on channel points reward redeem
async def on_channel_points_reward_redeem(data: ChannelPointsCustomRewardRedemptionAddEvent):
    EVENT_HANDLER.on_channel_points_reward_redeem(data)

#on channel points reward redeem update
async def on_channel_points_reward_redeem_update(data: ChannelPointsCustomRewardRedemptionUpdateEvent):
    EVENT_HANDLER.on_channel_points_reward_redeem_update(data)
    
#on poll begin
async def on_poll_begin(data: ChannelPollBeginEvent):
    EVENT_HANDLER.on_poll_begin(data)

#on poll progress
async def on_poll_progress(data: ChannelPollProgressEvent):
    EVENT_HANDLER.on_poll_progress(data)
    
#on poll end
async def on_poll_end(data: ChannelPollEndEvent):
    EVENT_HANDLER.on_poll_end(data)

#stream online
async def on_stream_online(data: StreamOnlineEvent):
    EVENT_HANDLER.on_stream_online(data)

#stream offline
async def on_stream_offline(data: StreamOfflineEvent):
    EVENT_HANDLER.on_stream_offline(data)

#on shoutout create
async def on_shoutout_create(data: ChannelShoutoutCreateEvent):
    EVENT_HANDLER.on_shoutout_create(data)
    
#on shoutout recieve
async def on_shoutout_recieve(data: ChannelShoutoutReceiveEvent):
    EVENT_HANDLER.on_shoutout_recieve(data)

#on ChatClear
async def on_chat_clear(data: ChannelChatClearEvent):
    EVENT_HANDLER.on_chat_clear(data)
    
#on ChatClear usermessages
async def on_chat_clear_user_messages(data: ChannelChatClearUserMessagesEvent):
    EVENT_HANDLER.on_chat_clear_user_messages(data)

#on chat delete messages
async def on_chat_delete_messages(data: ChannelChatMessageDeleteEvent):
    EVENT_HANDLER.on_chat_delete_messages(data)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=


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
