
from Module import Module
from EventHandler import EventHandler
from twitchAPI.chat import ChatMessage
from twitchAPI.twitch import Twitch
from twitchAPI.type import TwitchAPIException

class Shoutout(Module):
    def __init__(self, eventHandler: EventHandler):
        super().__init__("AutoShoutouts", eventHandler)
        self.shouted_out = []
        self.to_shoutout = eventHandler.config.Shoutout_list
        self.isSoft = eventHandler.config.auto_shoutout_isSoft
        self.message = eventHandler.config.auto_shoutout_message
        self.twitch: Twitch = eventHandler.TwitchAPI.TWITCH
        self.event_Handler.loginfo(self.name, " module loaded")
        self.event_Handler.loginfo(self.name, f"Shoutout list: {self.to_shoutout}")

    # on message check if user is in shout out list
    async def on_message(self, data: ChatMessage):
        if data.user.name in self.to_shoutout and data.user.name not in self.shouted_out:
            self.shouted_out.append(data.user.name)
            #if we doing soft shoutouts dont use send_a_shoutout
            if self.isSoft:
                await self.event_Handler.send_message(self.message.replace("{user}", data.user.name))
            #if we not doing soft shoutouts use send_a_shoutout
            else:
                
                #try except to catch if channel is not live
                try:
                    await self.twitch.send_a_shoutout(
                        self.event_Handler.config.channelID,
                        data.user.id,
                        self.event_Handler.config.channelID
                        )
                except TwitchAPIException as e:
                    self.event_Handler.logerror(self.name, f" {e}")
                
                await self.event_Handler.send_message(f"{self.message.replace('{user}', data.user.name)}")
            self.event_Handler.loginfo(self.name, f" {data.user.name} was shouted out")
