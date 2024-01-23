from Module import Module
from EventHandler import EventHandler
from twitchAPI.chat import ChatCommand
import logging
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_htmx import htmx, htmx_init
from twitchAPI.object.api import ChannelFollowersResult
import random



class entrygiveaway:
    def __init__(self, name, pid, isusersub, isfollower, pfp):
        self.name = name
        self.id = pid
        self.isusersub = isusersub
        self.isfollower = isfollower 
        self.pfp = pfp


entrylist : list[entrygiveaway] = []

entrycount = 0

currentgiveawaycommand = ""

winner: list[entrygiveaway] = []

giveawayrunning = "False"

error = ""

togglepause = "False"


router = APIRouter()

htmx_init(templates = Jinja2Templates(directory="templates"))

def construct_entrylist():
    numberofentries = len(entrylist)
    haswinner = "False"
    if len(winner) != 0:
        haswinner = "True"
    if numberofentries == 0:
        return {"currentgiveawaycommand": currentgiveawaycommand,
                "unqiueentrycount": "None",
                "numberofentries": "NONE",
                "giveawayrunning": giveawayrunning,
                "haswinner": haswinner,
                "winner": winner,
                "togglepause": togglepause,
                "error": error}

    return {"currentgiveawaycommand": currentgiveawaycommand,
            "unqiueentrycount": entrycount,
            "numberofentries": numberofentries,
            "giveawayrunning": giveawayrunning,
            "haswinner": haswinner,
            "winner": winner,
            "togglepause": togglepause,
            "error": error}


@router.get("/giveaway", response_class=HTMLResponse)
@htmx("giveaway","index", construct_entrylist)
def get_entrylist(request: Request):
    pass

class giveAwayMachine(Module):
    def __init__(self, eventHandler):
        super().__init__("give_away_machine", eventHandler)

    async def add_entry(self, cmd: ChatCommand):
        if togglepause == "True":
            return
        
        logging.info(f"{self.name}: {cmd.user.name} entered the giveaway")   
        global entrylist, entrycount
        username = cmd.user.name
        userid = cmd.user.id
        issub = cmd.user.subscriber
        isfollower = ""
        followertest: ChannelFollowersResult = await self.event_Handler.TwitchAPI.get_if_follower(username)
        if len(followertest.data) > 0:
            isfollower = True
        else:
            isfollower = False

        userpfp = await self.event_Handler.get_pfp(username)
        
        logging.info(f"{self.name}: {username} issub: {issub} isfollower: {isfollower}, pfp: {userpfp}")
        
        playerentry = entrygiveaway(username, userid, issub, isfollower, userpfp)
        #check if user is in list
        for entry in entrylist:
            if entry.id == userid:
                logging.info(f"{self.name}: {username} is already in the list")
                await self.event_Handler.send_message(f"{username} is already in the list!")
                return
        for entry in winner:
            if entry.id == userid:
                logging.info(f"{self.name}: {username} is already in the winner list")
                return
        isusersub = False
        #check if user is sub (subs get x2)
        if cmd.user.subscriber == True:
            #add user to list twice
            entrylist.append(playerentry)
            isusersub = True
            
        entrylist.append(playerentry)
        entrycount += 1
        
        if isusersub == True:
            logging.info(f"{self.name}: {username} was added to the list twice (sub)")
        else:
            logging.info(f"{self.name}: {username} was added to the list")
        
        await self.event_Handler.send_message(f"{username} entered the giveaway!")


    async def startgiveaway(self, command):
        self.event_Handler.TwitchAPI.CHAT.register_command(command, self.add_entry)
        global currentgiveawaycommand, giveawayrunning, entrylist, entrycount, winner
        entrylist.clear()
        winner.clear()
        entrycount = 0
        giveawayrunning = "True"
        currentgiveawaycommand = command
        logging.info(f"{self.name}: giveaway started with command {command}")
        
        await self.event_Handler.send_message(f"Giveaway started! Type {command} to enter!")

    async def endgiveaway(self):
        global currentgiveawaycommand, giveawayrunning, entrylist, entrycount, winner
        entrylist.clear()
        winner.clear()
        entrycount = 0
        giveawayrunning = "False"
        self.event_Handler.TwitchAPI.CHAT.unregister_command(currentgiveawaycommand)
        logging.info(f"{self.name}: giveaway ended")
        await self.event_Handler.send_message(f"Giveaway ended!")
        
        currentgiveawaycommand = ""
        #pick winner

    async def pickwinner(self):
        global entrylist, winner, entrycount, error
        logging.info(f"{self.name}: picking winner")
        
        if len(entrylist) == 0:
            error = "Error: no entries!"
            logging.info(f"{self.name}: {error}")
            return
        else:
            error = ""
        
        #shuffle 3 times
        random.shuffle(entrylist)
        random.shuffle(entrylist)
        random.shuffle(entrylist)
        winnerthisround = random.choice(entrylist)
        for per in winner:
            if per.id == winnerthisround.id:
                error = "Error: this Winner was already picked!"
                logging.info(f"{self.name}: {error}")
                return
            
        winner.append(winnerthisround)
        error = ""
        entrycount = entrycount - 1
        
        entrylist = [item for item in entrylist if item.id != winnerthisround.id]
        
        #await self.event_Handler.send_message(f"The winner is {winnerthisround.name}!")
        #entrylist.clear()
        logging.info(f"{self.name}: winner picked and announced {winnerthisround.name}")

    async def on_webfrontend_message(self, command):
        global winner, togglepause
        if type(command) == dict:
            if list(command.keys())[0] == "start_giveaway":
                logging.info(f"{self.name}: start giveaway command received")
                logging.info(f"{self.name}: {command['start_giveaway']}")
                await self.startgiveaway(command["start_giveaway"])
            if list(command.keys())[0] == "end_giveaway":
                await self.endgiveaway()
            if list(command.keys())[0] == "pick_winner":
                await self.pickwinner()
            if list(command.keys())[0] == "toggle_pause":
                global togglepause
                if togglepause == "False":
                    togglepause = "True"
                else:
                    togglepause = "False"
            if list(command.keys())[0] == "winner_announce":
                personid = command["winner_announce"]
                logging.info(f"{self.name}: winner announce command received")
                for person in winner:
                    if person.id == personid:
                        await self.event_Handler.send_message(f"The winner is @{person.name}!")
                        logging.info(f"{self.name}: winner announced {person.name}")
            if list(command.keys())[0] == "winner_remove":
                personid = command["winner_remove"]
                logging.info(f"{self.name}: winner remove command received")
                winner = [item for item in winner if item.id != personid]

