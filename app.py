import json
import sys
from ConfigHandler import ConfigHandler
import os
import sqlite3
from Databaseconn import Databaseconn
from EventHandler import EventHandler

import TwitchAPIConn

from TadaLogger import tadaLogger




channel = ""
clientID = ""
clientSecret = ""

eventHandler: EventHandler = None

# Existing code...


def start_twitch():
        
    tadalogger = tadaLogger()       
    
    #check if config file exists
    if not os.path.exists("config.json"):
        tadalogger.logwarning("Config json file does not exist. please create and edit it.")
        exit()
    
    # Usage example
    config_handler = ConfigHandler()
    config_handler.load_config('config.json')
    
    tadalogger.loginfo("startup", "checking for database file...")
    # Check if database file exists
    if not os.path.exists(f"{config_handler.channel}.db"):
        tadalogger.logwarning("startup", "Database file not found. Creating new file...")
        # Create a new database file
        conn = sqlite3.connect(f"{config_handler.channel}.db")
        tadalogger.logwarning("startup", f"Database file created. as {config_handler.channel}.db")
    else:
        tadalogger.loginfo("startup", "Database file found.")
    
    # Create event handler
    
    eventHandler = EventHandler()
    eventHandler.assign_to_logger(tadalogger)
    dbconn = Databaseconn(eventHandler, config_handler.channel)
    eventHandler.assign_to_twitch(TwitchAPIConn)
    eventHandler.assign_to_DBConn(dbconn)
    eventHandler.assign_to_config(config_handler)
    
    
    # run app 
    # connect to twitch
    TwitchAPIConn.run(
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
        
        "worker_update_rate": 60,

        "Basic_Commands": True,
        "Chat_log": True,
        "Ban_log": True,
        "Unban_log": True,
        "Mini_games": True,
        "Mini_games_pointsperwin": 100,
        "Shoutout_Auto": True,
        "Shoutout_Soft": True,
        "Shoutout_Message": "Check out {user} at https://twitch.tv/{user} !",
        "Shoutout_list": [
            "target_user1"
        ],
        
        
        "faq": True,
        "faq_list": [
            "question1",
            "question2"
        ],
        
        "rules": True,
        "rules_list": [
            "rule1",
            "rule2"
        ],
        
        
        "lastwhereChannel": 3,
        "wherelocations": [
            "tech basement",
            "Avalon puris",
            "Tara Shadow Mission",
            "Tailteann Shadow Mission",
            "Ably Dungeon",
            "Ciar Dungeon",
            "Rundal Dungeon",
            "Glenn",
            "Crom Bas",
            "Tir Chonaill",
            "Dunbarton"
        ]
    }
        
    if not os.path.exists("config.json"):
        print("startup Config json file does not exist. creating config. please edit this file.")
        config_temp = json.dumps(defaultconfig, indent=4)
        with open("config.json", 'w') as file:
            file.write(config_temp)
        exit()
    
    # check config for channel name, id and secert
    with open("config.json", 'r') as file:
        config_data = json.load(file)
        exitapp = False
        if config_data['channel'] == "":
            print("startup channel name is empty. please edit config file.")
            exitapp = True
        if config_data['clientID'] == "":
            print("startup clientID is empty. please edit config file.")
            exitapp = True
        if config_data['clientSecret'] == "":
            print("startup clientSecret is empty. please edit config file.")
            exitapp = True
        if exitapp:
            exit()
    

    
    start_twitch()
    print("Close application and try again")
    sys.exit()
    
    
