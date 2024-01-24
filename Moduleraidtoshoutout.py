from Module import Module
from EventHandler import EventHandler
from twitchAPI.object.eventsub import ChannelRaidEvent

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_htmx import htmx, htmx_init
from twitchAPI.type import TwitchAPIException


class raider:
    def __init__(self, name, id, raidsize, pfp):
        self.name = name
        self.id = id
        self.raidsize = raidsize
        self.pfp = pfp

raiders: list[raider] = []
raiderscount = 0
router = APIRouter()

htmx_init(templates = Jinja2Templates(directory="templates"))

def construct_raidlist():
    raidstring = f"{raiderscount}"
    return {"raiders": raiders,
            "raiderscount": raidstring}

@router.get("/raidtoshoutout", response_class=HTMLResponse)
@htmx("raidtoshoutout","index", construct_raidlist)
def get_raidlist(request: Request):
    pass



class raidtoshoutout(Module):
    def __init__(self, eventHandler):
        global raiders
        super().__init__("raid_to_shoutout", eventHandler)
        # testraider = raider("test", "test", "0", "https://static-cdn.jtvnw.net/jtv_user_pictures/6eec0c89-0213-4f11-8bd0-91da1e0d75e2-profile_image-300x300.png")
        # raiders.append(testraider)
        self.twitch = eventHandler.TwitchAPI.TWITCH    
        self.event_Handler.loginfo(self.name, " module loaded")
    
    async def on_raid(self, data: ChannelRaidEvent):
        global raiders, raiderscount
        
        raidername = data.event.from_broadcaster_user_name
        raiderid = data.event.from_broadcaster_user_id
        raiderchatcount = data.event.viewers
        raiderpfp = await self.event_Handler.get_pfp(raidername)
        raider = raider(raidername, raiderid, raiderchatcount, raiderpfp)
        raiders.append(raider)
        self.event_Handler.loginfo(self.name, f"{raidername} was added to the raiders list")
        self.event_Handler.eventtofrontend(self.name, f"{raidername} was added to the raiders list")
        raiderscount = len(raiders)
    
    async def loud_shoutout(self, personname):
        await self.event_Handler.send_message(f"!so {personname}")
    
    async def soft_shoutout(self, personid):
        try:
            await self.twitch.send_a_shoutout(
                self.event_Handler.config.channelID,
                personid,
                self.event_Handler.config.channelID
                )
        except TwitchAPIException as e:
            self.event_Handler.logerror(self.name, f"{self.name}: {e}")
            self.event_Handler.eventtofrontend(self.name, f"{self.name}: {e}")
        
    async def on_webfrontend_message(self, command):
        global raiders, raiderscount
        if type(command) is not dict:
            return
        if list(command.keys())[0] == "clear_raiders":
            raiders.clear()
        if list(command.keys())[0] == "remove_raider":
            personid = command["remove_raider"]
            raiders = [item for item in raiders if item.id != personid]
        if list(command.keys())[0] == "soft_shoutout":
            personid = command["soft_shoutout"]
            await self.soft_shoutout(personid)
            #shoutout person softly
            raiders = [item for item in raiders if item.id != personid]
            raiderscount = len(raiders)
        if list(command.keys())[0] == "loud_shoutout":
            personname = command["loud_shoutout"]
            await self.loud_shoutout(personname)
            #shoutout person loudly
            raiders = [item for item in raiders if item.name != personname]
            raiderscount = len(raiders)