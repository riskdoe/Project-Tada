import json
import os
import sqlite3
from EventHandler import EventHandler
from ModuleChatLog import ChatLog
import TwitchAPIConn
import asyncio
import logging

from fastapi import FastAPI
import uvicorn
from threading import Thread
from ModuleChatLog import router as chat_log_router

channel = ""
clientID = ""
clientSecret = ""

eventHandler = None

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
    
    channel = config["channel"]
    clientID = config["clientID"]
    clientSecret = config["clientSecret"]
    
    logging.info ("checking for database file...")
    # Check if database file exists
    if not os.path.exists("database.db"):
        logging.warning("Database file not found. Creating new file...")
        # Create a new database file
        conn = sqlite3.connect("database.db")
        conn.close()
        logging.warning("Database file created. as database.db")
    else:
        logging.info("Database file found.")
    
    # Create event handler
    
    eventHandler = EventHandler()
    # run app
    # create chat log module
    chatLog = ChatLog(eventHandler)
    eventHandler.AddModule(chatLog)
    
    # connect to twitch
    TwitchAPIConn.run(channel, clientID, clientSecret, eventHandler)
if __name__ == "__main__":
    
    # Run FastAPI server in a separate thread
    fastapi_thread = Thread(target=start_fastapi)
    fastapi_thread.start()
    
    # run twitch bot in separate thread
    twitch_thread = Thread(target=start_twitch)
    twitch_thread.start()
    
    twitch_thread.join()
    fastapi_thread.join()
    
