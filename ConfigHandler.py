import json
import os
import logging

class ConfigHandler:
    def __init__(self):
        self.channel = None
        self.channelID = None
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
        
        #faq and rules
        self.faq = False
        self.faq_list: list[str] = []
        self.rules = False
        self.rules_list: list[str] = []
        
        # Add more fields as needed


    def load_config(self, filepath):
        with open(filepath, 'r') as file:
            config_data = json.load(file)
            self.channel = config_data['channel']
            self.clientID = config_data['clientID']
            self.clientSecret = config_data['clientSecret']
            self.Super_moderators = config_data['Super_Moderators']
            
            self.worker_update_rate = config_data['worker_update_rate']
            
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
            tempShoutout_list = config_data['Shoutout_list']
            for user in tempShoutout_list:
                self.Shoutout_list.append(user.lower())
            
            #faq and rules
            self.faq = config_data['faq']
            self.faq_list = config_data['faq_list']
            self.rules = config_data['rules']
            self.rules_list = config_data['rules_list']
            
            self.defaultwherechannel = config_data['defaultwherechannel']
            self.wherelocations = config_data['wherelocations']
            
            
            
            
            logging.info("Config loaded")
            logging.info(f"Channel: {self.channel}")
            # logging.info(f"ClientID: {self.clientID}")
            # logging.info(f"ClientSecret: {self.clientSecret}")
            logging.info(f"Super Moderators: {self.Super_moderators}")
            logging.info(f"Basic Commands: {self.basic_command}")
            logging.info(f"Chat log: {self.chat_log}")
            logging.info(f"Ban log: {self.ban_log}")
            logging.info(f"Unban log: {self.unban_log}")
            logging.info(f"Minigames: {self.minigames}")
            logging.info(f"Minigame points per win: {self.minigame_pointsPerWin}")
            logging.info(f"Auto shoutout: {self.auto_shoutout}")
            logging.info(f"Auto shoutout is soft: {self.auto_shoutout_isSoft}")
            logging.info(f"Auto shoutout message: {self.auto_shoutout_message}")
            logging.info(f"Auto shoutout list: {self.Shoutout_list}")
            
