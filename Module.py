# Parent module for all other modules
# child classes will need to inherit the functions they need
# and override them with their own code

class Module():
    def __init__(self, name, handler):
        self.name = name
        self.__version__ = '0.0.1'
        self.__author__ = 'Author Name'
        self.__description__ = 'Module description'
        self.event_Handler = handler
        
    def on_load(self):
        pass
    
    def on_unload(self):
        pass
    
    # |> IRC Events <|
        
    # recv message
    def on_message(self, message):
        pass
    
    # send message
    #its likely we can use API to send messages so this will need to be looked at later
    #for now we will just send it to the irc
    def send_message(self, message):
        self.event_Handler.send_message(message)
    
    
    # |> Api Events <|
    # ||> Event Sub <||
    
    
    # on channel update
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_update_v2
    def on_channel_update(self, data):
        pass
    
    # on follow
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_follow_v2
    def on_follow(self, data):
        pass
    
    # on Subscribe
    # used when any subscribe comes though
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_subscribe
    def on_subscribe(self, data):
        pass
    
    # on Subscription Gift
    # used when gift subs come though
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_subscription_gift
    def on_subscription_gift(self, data):
        pass
    
    # on Subscription Message
    # used when a message is sent with a subscription
    # likely that on subscribe will be used as well.
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_subscription_message
    def on_subscription_message(self, data):
        pass
    
    # on cheer
    # used when a user cheers any amount
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_cheer
    def on_cheer(self, data):
        pass
    
    # on raid
    # used when a raid is sent
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_raid
    def on_raid(self, data):
        pass
    
    # on ban
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_ban
    def on_ban(self, data):
        pass
    
    # on unban
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_unban
    def on_unban(self, data):
        pass
    
    # on moderator add
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_moderator_add
    def on_moderator_add(self, data):
        pass
    
    # on moderator remove
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_moderator_remove
    def on_moderator_remove(self, data):
        pass
    
    # on channel points redeem reward add
    # used when a custom reward is added to the channel
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_points_custom_reward_add
    def on_channel_points_redeem_reward_add(self, data):
        pass
    
    # on channel points redeem reward update
    # used when a custom reward is updated on the channel
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_points_custom_reward_update
    def on_channel_points_redeem_reward_update(self, data):
        pass
    
    # on channel points redeem reward remove
    # used when a custom reward is removed from the channel
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_points_custom_reward_remove
    def on_channel_points_redeem_reward_remove(self, data):
        pass
    
    # on channel points redeem
    # used when a user redeems a custom reward
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_points_custom_reward_redemption_add
    def on_channel_points_redeem(self, data):
        pass
    
    # on channel points redeem update
    # used when a custom reward is updated on the channel
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_points_custom_reward_redemption_update
    def on_channel_points_redeem_update(self, data):
        pass
    
    # on channel poll begin
    # used when a poll is started on the channel
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_poll_begin
    def on_channel_poll_begin(self, data):
        pass
    
    # on channel poll progress
    # used when a poll is updated on the channel (votes)
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_poll_progress
    def on_channel_poll_progress(self, data):
        pass
    
    # on channel poll end
    # used when a poll is ended on the channel
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_poll_end
    def on_channel_poll_end(self, data):
        pass
    
    # on channel prediction begin
    # used when a prediction is started on the channel
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_prediction_begin
    def on_channel_prediction_begin(self, data):
        pass
    
    # on channel prediction progress(votes)
    # used when a prediction is updated on the channel (votes)
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_prediction_progress
    def on_channel_prediction_progress(self, data):
        pass
    
    # on channel prediction lock
    # used when a prediction is locked on the channel
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_prediction_lock
    def on_channel_prediction_lock(self, data):
        pass
    
    # on channel prediction end
    # used when a prediction is ended on the channel
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_prediction_end
    def on_channel_prediction_end(self, data):
        pass
        
    # on goal begin
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_goal_begin
    def on_goal_begin(self, data):
        pass
    
    
    # on goal progress
    # ref : https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_goal_progress
    def on_goal_progress(self, data):
        pass
    
    # on goal end
    # ref : https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_goal_end
    def on_goal_end(self, data):
        pass
    
    # on hype train begin
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_hype_train_begin
    def on_hype_train_begin(self, data):
        pass
    
    # on hype train progress
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_hype_train_progress
    def on_hype_train_progress(self, data):
        pass
    
    # on hype train end
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_hype_train_end
    def on_hype_train_end(self, data):
        pass
    
    # on stream online
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_stream_online
    def on_stream_online(self, data):
        pass
    
    # on stream offline
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_stream_offline
    def on_stream_offline(self, data):
        pass
    
    # on shoutout create
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_shoutout_create
    def on_shoutout_create(self, data):
        pass
    
    # on shoutout received
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_shoutout_receive
    
    # on channel chat clear
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_chat_clear
    def on_channel_chat_clear(self, data):
        pass
    
    # on user chat clear
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_chat_clear_user_messages
    def on_channel_chat_clear_user_messages(self, data):
        pass
    
    # on channel message delete
    # ref: https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.base.html#twitchAPI.eventsub.base.EventSubBase.listen_channel_chat_message_delete
    def on_channel_chat_message_delete(self, data):
        pass