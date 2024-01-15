import json
import os
import logging

class ConfigHandler:
    def __init__(self):
        self.channel = None
        self.clientID = None
        self.clientSecret = None
        self.Super_moderators: list[str] = []
        
        #commands
        self.basic_command = False 
        self.chat_log = False
        self.ban_log = False
        self.unban_log = False
        
        
        #minigames
        self.minigames = False
        self.minigame_pointsPerWin = 1
        
        
        #auto shoutout
        self.auto_shoutout = False
        self.auto_shoutout_isSoft = False
        self.auto_shoutout_message = ""
        self.Shoutout_list: list[str] = []
        # Add more fields as needed

    def load_config(self, filepath):
        with open(filepath, 'r') as file:
            config_data = json.load(file)
            self.channel = config_data['channel']
            self.clientID = config_data['clientID']
            self.clientSecret = config_data['clientSecret']
            self.Super_moderators = config_data['Super_Moderators']
            
            #commands
            self.basic_command = config_data['Basic_Commands']
            self.chat_log = config_data['Chat_log']
            self.ban_log = config_data['Ban_log']
            self.unban_log = config_data['Unban_log']
            
            #minigames
            self.minigames = config_data['Mini_games']
            self.minigame_pointsPerWin = config_data['Mini_games_pointsperwin']
            
            #auto shoutout
            self.auto_shoutout = config_data['Shoutout_Auto']
            self.auto_shoutout_isSoft = config_data['Shoutout_Soft']
            self.auto_shoutout_message = config_data['Shoutout_Message']
            self.Shoutout_list = config_data['Shoutout_list']
