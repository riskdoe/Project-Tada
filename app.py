import json
import os
import sqlite3
import TwitchAPIConn


if __name__ == "__main__":
    #grab channel details
    config = None
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
        
        
    TwitchAPIConn.run(channel, clientID, clientSecret)
    
    
    