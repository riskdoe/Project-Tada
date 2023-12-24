import json
import os
import sqlite3
from EventHandler import EventHandler
from ModuleChatLog import ChatLog
import TwitchAPIConn


if __name__ == "__main__":
    #grab channel details
    config = None
    
    #check if config file exists
    if not os.path.exists("config.json"):
        print("Config json file does not exist. please create and edit it.")
        exit()
    
    #load config file
    with open("config.json", "r") as f:
        config = json.load(f)
    
    channel = config["channel"]
    clientID = config["clientID"]
    clientSecret = config["clientSecret"]
    
    # print (f"Channel: {channel}")
    # print (f"Bot name: {botname}")
    # print (f"Client ID: {clientID}")
    # print (f"Client Secret: {clientSecret}")
    
    print ("checking for database file...")
    # Check if database file exists
    if not os.path.exists("database.db"):
        print("Database file not found. Creating new file...")
        # Create a new database file
        conn = sqlite3.connect("database.db")
        conn.close()
        print("Database file created. as database.db")
    else:
        print("Database file found.")
        
    # Create event handler
    eventHandler = EventHandler()
    # create chat log module
    chatLog = ChatLog(eventHandler)
    eventHandler.AddModule(chatLog)
    
    # connect to twitch
    TwitchAPIConn.run(channel, clientID, clientSecret, eventHandler)
    
    
    