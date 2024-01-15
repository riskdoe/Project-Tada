import json
from ConfigHandler import ConfigHandler
import os
import sqlite3
from Databaseconn import Databaseconn
from EventHandler import EventHandler

import TwitchApiConn
from TwitchApiConn import router as twitch_api_router
import logging

from fastapi import FastAPI
import uvicorn
from threading import Thread
from ModuleChatLog import router as chat_log_router



channel = ""
clientID = ""
clientSecret = ""

eventHandler: EventHandler = None

# Existing code...

# Create a new FastAPI application
app = FastAPI()
app.include_router(chat_log_router, prefix="/api/v1")
app.include_router(twitch_api_router, prefix="/api/v1")

# Define a route
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Function to run FastAPI server
def start_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8080)
    try:
        input('enter to exit')
    except KeyboardInterrupt:
        pass
    finally:
        exit()

def start_twitch():
        
    #set up logging
    logFormatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logging.basicConfig(filename='output.log'
                        ,filemode='w'
                        ,format='%(asctime)s - %(levelname)s - %(message)s'
                        ,encoding='utf-8'
                        ,level= logging.INFO)
    rootlogger = logging.getLogger()
    consolehandler = logging.StreamHandler()
    consolehandler.setFormatter(logFormatter)
    rootlogger.addHandler(consolehandler)
    
    #grab channel details
    config = None
    
    #check if config file exists
    if not os.path.exists("config.json"):
        logging.warning("Config json file does not exist. please create and edit it.")
        exit()
    
    # Usage example
    config_handler = ConfigHandler()
    config_handler.load_config('config.json')
    
    logging.info ("checking for database file...")
    # Check if database file exists
    if not os.path.exists(f"{config_handler.channel}.db"):
        logging.warning("Database file not found. Creating new file...")
        # Create a new database file
        conn = sqlite3.connect(f"{config_handler.channel}.db")
        conn.close()
        logging.warning(f"Database file created. as {config_handler.channel}.db")
    else:
        logging.info("Database file found.")
    
    # Create event handler
    
    eventHandler = EventHandler()
    dbconn = Databaseconn(eventHandler, config_handler.channel)
    eventHandler.assign_to_twitch(TwitchApiConn)
    eventHandler.assign_to_DBConn(dbconn)
    eventHandler.assign_to_config(config_handler)
    
    # run app 
    # connect to twitch
    TwitchApiConn.run(
        config_handler.clientID,
        config_handler.clientSecret,
        eventHandler)


if __name__ == "__main__":
    
    defaultconfig = {
        "channel": "",
        "clientID": "",
        "clientSecret": "",
        "Super_Moderators": [
            "channel_owner"
        ],

        "Basic_Commands": "true",
        "Chat_log": "true",
        "Ban_log": "true",
        "Unban_log": "true",
        "Mini_games": "true",
        "Mini_games_pointsperwin": 100,
        "Shoutout_Auto": "true",
        "Shoutout_Soft": "true",
        "Shoutout_Message": "Check out {user} at https://twitch.tv/{user}!",
        "Shoutout_list": [
            "target_user1"
        ]  
    }
        
    if not os.path.exists("config.json"):
        logging.warning("Config json file does not exist. creating config. please edit this file.")
        config_temp = json.dumps(defaultconfig, indent=4)
        logging.info(config_temp)
        with open("config.json", 'w') as file:
            file.write(config_temp)
        exit()
    
    # check config for channel name, id and secert
    with open("config.json", 'r') as file:
        config_data = json.load(file)
        exitapp = False
        if config_data['channel'] == "":
            logging.warning("channel name is empty. please edit config file.")
            exitapp = True
        if config_data['clientID'] == "":
            logging.warning("clientID is empty. please edit config file.")
            exitapp = True
        if config_data['clientSecret'] == "":
            logging.warning("clientSecret is empty. please edit config file.")
            exitapp = True
        if exitapp:
            exit()
    
    # Run FastAPI server in a separate thread
    fastapi_thread = Thread(target=start_fastapi)
    fastapi_thread.start()
    
    start_twitch()
    
    
