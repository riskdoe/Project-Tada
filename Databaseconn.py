import sqlite3
import logging
from twitchAPI.chat import ChatMessage
from twitchAPI.object.eventsub import ChannelBanEvent
import datetime

class cmessage():
    def __init__(self, id: str, user: str, text: str, timestamp: int):
        self.id = id
        self.user = user
        self.text = text
        self.timestamp = timestamp
    
    def __str__(self):
        return f"{self.user}: {self.text}"
    
class Bandata():
    def __init__(self,
                 userID: str,
                 userName: str,
                 moderatorID: str,
                 moderatorName: str,
                 reason: str,
                 bantime: int,
                 endtime: int,
                 permanent: int):
        self.userID = userID
        self.userName = userName
        self.moderatorID = moderatorID
        self.moderatorName = moderatorName
        self.reason = reason
        self.bantime = bantime
        if endtime == None:
            self.endtime = 0
        else:
            self.endtime = endtime
        if permanent == True:
            self.permanent = 1
        else:
            self.permanent = 0        
        
    def __str__(self):
        return f"{self.userName} was banned by {self.moderatorName} for {self.reason}"

class Databaseconn():
    def __init__(self, eventHandler, dbname: str):
        self.eventHandler = eventHandler
        self.db = sqlite3.connect(f"{dbname}.db", check_same_thread=False)
        logging.info(f"Connected to database {dbname}.db")
        self.cursor = self.db.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS "Messages" ("ID" INTEGER NOT NULL, "TwitchID" TEXT NOT NULL, "UserName" TEXT NOT NULL,"Message" TEXT NOT NULL,"UnixTimeStamp" INTEGER NOT NULL,PRIMARY KEY("ID" AUTOINCREMENT))')
        self.db.commit()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS "BanLog" ("ID" INTEGER NOT NULL, "BannedUserID" TEXT NOT NULL, "BannedUserName" TEXT NOT NULL, "ModeratorID" TEXT NOT NULL, "ModeratorUser" TEXT NOT NULL,"BanReason" TEXT NOT NULL, "BanTime" INTEGER NOT NULL,"IsPermanent" INTEGER NOT NULL DEFAULT 0, PRIMARY KEY("ID" AUTOINCREMENT))')
        self.db.commit()
        #TODO: add basic command storeage
        
    def AddMessage(self, data):
        message = cmessage(data.id, data.user.name, data.text, data.sent_timestamp)
        self.cursor.execute(f'INSERT INTO "main"."Messages" ("TwitchID", "UserName", "Message", "UnixTimeStamp") VALUES ("{data.id}", "{data.user.name}", "{data.text}", "{data.sent_timestamp}")')
        self.db.commit()
        logging.debug(f'attempted to insert message into database: {message}')

    def AddBan(self, data: ChannelBanEvent):
        ban = Bandata(data.event.user_id, data.event.user_name, data.event.moderator_user_id, data.event.moderator_user_name, data.event.reason, data.event.banned_at, data.event.ends_at, data.event.is_permanent)
        #TODO: This is gonna fucking crash 100%
        self.cursor.execute(f'INSERT INTO "BanLog" ("BannedUserID", "BannedUserName", "ModeratorID", "ModeratorUser", "BanReason", "BanTime", "IsPermanent") VALUES ("{ban.userID}", "{ban.userName}", "{ban.moderatorID}", "{ban.moderatorName}", "{ban.reason}", "{ban.bantime}", "{ban.permanent}")')
        logging.debug(f"attempted to insert ban into database: {ban}")
        self.db.commit()
        
    #TODO: add "add to basic commands"
    #TODO: add "remove from basic commands"
    #TODO: add "edit basic commands"