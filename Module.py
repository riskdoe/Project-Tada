# Parent module for all other modules
# child classes will need to inherit the functions they need
# and override them with their own code

class Module():
    def __init__(self, name, eventHandler):
        self.name = name
        self.__version__ = '0.0.1'
        self.__author__ = 'Author Name'
        self.__description__ = 'Module description'
        self.event_Handler = eventHandler
        
    async def on_load(self):
        pass
    
    async def on_unload(self):
        pass
    
    # |> IRC Events <|
        
    # recv message
    async def on_message(self, data):
        pass
    
    # send message
    async def send_message(self, message):
        self.event_Handler.send_message(message)
    
    
    # |> Api Events <|
    # ||> Event Sub <||
    
    
    # on channel update
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_update_v2
    async def on_channel_update(self, data):
        pass
    
    # on follow
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_follow_v2
    async def on_follow(self, data):
        pass
    
    # on Subscribe
    # used when any subscribe comes though
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_subscribe
    async def on_subscribe(self, data):
        pass
    
    # on Subscription Gift
    # used when gift subs come though
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_subscription_gift
    async def on_subscription_gift(self, data):
        pass
    
    # on Subscription Message
    # used when a message is sent with a subscription
    # likely that on subscribe will be used as well.
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_subscription_message
    async def on_subscription_message(self, data):
        pass
    
    # on cheer
    # used when a user cheers any amount
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_cheer
    async def on_cheer(self, data):
        pass
    
    # on raid
    # used when a raid is sent
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_raid
    async def on_raid(self, data):
        pass
    
    # on ban
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_ban
    async def on_ban(self, data):
        pass
    
    # on unban
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_unban
    async def on_unban(self, data):
        pass
    
    # on moderator add
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_moderator_add
    async def on_moderator_add(self, data):
        pass
    
    # on moderator remove
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_moderator_remove
    async def on_moderator_remove(self, data):
        pass
    
    # on channel points redeem reward add
    # used when a custom reward is added to the channel
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_points_custom_reward_add
    async def on_channel_points_redeem_reward_add(self, data):
        pass
    
    # on channel points redeem reward update
    # used when a custom reward is updated on the channel
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_points_custom_reward_update
    async def on_channel_points_redeem_reward_update(self, data):
        pass
    
    # on channel points redeem reward remove
    # used when a custom reward is removed from the channel
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_points_custom_reward_remove
    async def on_channel_points_redeem_reward_remove(self, data):
        pass
    
    # on channel points redeem
    # used when a user redeems a custom reward
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_points_custom_reward_redemption_add
    async def on_channel_points_redeem(self, data):
        pass
    
    # on channel points redeem update
    # used when a custom reward is updated on the channel
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_points_custom_reward_redemption_update
    async def on_channel_points_redeem_update(self, data):
        pass
    
    # on channel poll begin
    # used when a poll is started on the channel
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_poll_begin
    async def on_channel_poll_begin(self, data):
        pass
    
    # on channel poll progress
    # used when a poll is updated on the channel (votes)
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_poll_progress
    async def on_channel_poll_progress(self, data):
        pass
    
    # on channel poll end
    # used when a poll is ended on the channel
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_poll_end
    async def on_channel_poll_end(self, data):
        pass
    
    # on stream online
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_stream_online
    async def on_stream_online(self, data):
        pass
    
    # on stream offline
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_stream_offline
    async def on_stream_offline(self, data):
        pass
    
    # on shoutout create
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_shoutout_create
    async def on_shoutout_create(self, data):
        pass
    
    # on shoutout received
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_shoutout_receive
    async def on_shoutout_received(self, data):
        pass
    
    # on channel chat clear
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_chat_clear
    async def on_channel_chat_clear(self, data):
        pass
    
    # on user chat clear
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_chat_clear_user_messages
    async def on_channel_chat_clear_user_messages(self, data):
        pass
    
    # on channel message delete
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_chat_message_delete
    async def on_channel_chat_message_delete(self, data):
        pass