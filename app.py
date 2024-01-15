import json
import os
import sqlite3
from Databaseconn import Databaseconn
from EventHandler import EventHandler

import TwitchApiConn
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
    
    #load config file
    with open("config.json", "r") as f:
        config = json.load(f)
        
    clientID = config["clientID"]
    clientSecret = config["clientSecret"]
    channel = config["channel"]
    
    logging.info ("checking for database file...")
    # Check if database file exists
    if not os.path.exists(f"{channel}.db"):
        logging.warning("Database file not found. Creating new file...")
        # Create a new database file
        conn = sqlite3.connect(f"{channel}.db")
        conn.close()
        logging.warning(f"Database file created. as {channel}.db")
    else:
        logging.info("Database file found.")
    
    # Create event handler
    
    eventHandler = EventHandler()
    dbconn = Databaseconn(eventHandler, channel)
    eventHandler.assign_to_twitch(TwitchApiConn)
    eventHandler.assign_to_DBConn(dbconn)
    
    # run app 
    # connect to twitch
    TwitchApiConn.run(
        clientID,
        clientSecret,
        eventHandler)
    
    
    #TwitchEventSubConn.run(clientID, clientSecret, eventHandler)


if __name__ == "__main__":
    
    # Run FastAPI server in a separate thread
    fastapi_thread = Thread(target=start_fastapi)
    fastapi_thread.start()
    
    start_twitch()
    
    
