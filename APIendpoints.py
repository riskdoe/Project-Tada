from Databaseconn import Databaseconn
from ConfigHandler import ConfigHandler
from EventHandler import EventHandler
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_htmx import htmx, htmx_init
from pathlib import Path
import uvicorn
import logging

# endpoint routers

from ModuleChatLog import router as chatlog_router
from ModuleMiniGameSystem import router as minigamesystem_router
from ModuleCommandHandler import router as commandhandler_router
from ModulesStreamTracker import router as streamtracker_router
from ModuleGiveAwayMachine import router as giveaway_router
from Moduleraidtoshoutout import router as raidtoshoutout_router
from TadaLogger import router as tadalogger_router

# Create a new FastAPI application
app = FastAPI()
htmx_init(templates=Jinja2Templates(directory="templates"))

# Mount the static folder
app.mount("/static", StaticFiles(directory="static"), name="static")


databaseconn = None



# routers for API endpoints (make frontend work)

app.include_router(chatlog_router, prefix="/api/v1")
app.include_router(minigamesystem_router, prefix="/api/v1")
app.include_router(commandhandler_router, prefix="/api/v1")
app.include_router(streamtracker_router, prefix="/api/v1")
app.include_router(giveaway_router, prefix="/api/v1")
app.include_router(raidtoshoutout_router, prefix="/api/v1")
app.include_router(tadalogger_router, prefix="/api/v1")



def construct_root_page():
    return {
        "greeting": "Hello World",
    }
    
def construct_messages_test():
    messages = databaseconn.get_messages()
    return {"messages": messages}

# Define a route
@app.get("/", response_class=HTMLResponse)
@htmx("index", "index")
def read_root(request: Request):
    return construct_root_page()

@app.get("/messagestest", response_class=HTMLResponse)
@htmx("chat-messagesfromdb", "index", construct_messages_test)
async def get_messagestest(request: Request):
    pass

# Function to run FastAPI server
def start_fastapi():
    global databaseconn   
    logging.info(f'test {Path(".") / "templates"}')
    cpmfig_handler = ConfigHandler()
    cpmfig_handler.load_config('config.json')
    databaseconn = Databaseconn(None, cpmfig_handler.channel)
    
    #prevent circular import
    from TwitchAPIConn import router as twitch_api_router
    app.include_router(twitch_api_router, prefix="/api/v1")
    
    uvicorn.run(app, host="127.0.0.1", port=8080, access_log=False)
    
    try:
        input('enter to exit')
    except KeyboardInterrupt:
        pass
    finally:
        exit()