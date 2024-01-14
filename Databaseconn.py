import sqlite3
import logging
from twitchAPI.chat import ChatMessage
from twitchAPI.object.eventsub import ChannelBanEvent,ChannelUnbanEvent
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
    
class Unbandata():
    def __init__(self,
                 userID: str,
                 userName: str,
                 moderatorID: str,
                 moderatorName: str,
                ):
        self.userID = userID
        self.userName = userName
        self.moderatorID = moderatorID 
        self.moderatorName = moderatorName
        
    def __str__(self):
        return f"{self.userName} was unbanned by {self.moderatorName}"

class minigameplayer():
    def __init__(self, id: str, name: str, 
                 points: int = 0, total_wins: int = 0,
                 trivia_wins: int = 0,
                 hangman_Wins: int = 0):
        self.id = id
        self.name = name
        self.points = points
        self.total_wins = total_wins
        
        #Trivia
        self.trivia_wins = trivia_wins
        
        #hangman
        self.hangman_Wins = hangman_Wins

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
        self.cursor.execute('CREATE TABLE IF NOT EXISTS "UnBanLog" ("ID" INTEGER NOT NULL, "BannedUserID" TEXT NOT NULL, "BannedUserName" TEXT NOT NULL, "ModeratorID" TEXT NOT NULL, "ModeratorUser" TEXT NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT))')
        self.db.commit()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS "BasicCommands" ("ID" INTEGER NOT NULL, "Alias" TEXT NOT NULL, "Return" TEXT NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT))')
        self.db.commit()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS "MiniGamePlayers" ("ID" INTEGER NOT NULL, "TwitchID" TEXT NOT NULL , "Name" TEXT NOT NULL,"Points" INTEGER NOT NULL,"TotalWins" INTEGER NOT NULL,"TriviaWins" INTEGER NOT NULL,"HangmanWins" INTEGER NOT NULL,PRIMARY KEY("ID" AUTOINCREMENT))')
        self.db.commit()

    def AddMessage(self, data: ChatMessage):
        message = cmessage(data.id, data.user.name, data.text, data.sent_timestamp)
        self.cursor.execute(f'INSERT INTO "main"."Messages" ("TwitchID", "UserName", "Message", "UnixTimeStamp") VALUES ("{data.id}", "{data.user.name}", "{data.text}", "{data.sent_timestamp}")')
        self.db.commit()
        logging.debug(f'attempted to insert message into database: {message}')

    def AddBan(self, data: ChannelBanEvent):
        ban = Bandata(data.event.user_id, data.event.user_name, data.event.moderator_user_id, data.event.moderator_user_name, data.event.reason, data.event.banned_at, data.event.ends_at, data.event.is_permanent)
        self.cursor.execute(f'INSERT INTO "BanLog" ("BannedUserID", "BannedUserName", "ModeratorID", "ModeratorUser", "BanReason", "BanTime", "IsPermanent") VALUES ("{ban.userID}", "{ban.userName}", "{ban.moderatorID}", "{ban.moderatorName}", "{ban.reason}", "{ban.bantime}", "{ban.permanent}")')
        logging.debug(f"attempted to insert ban into database: {ban}")
        self.db.commit()

    def AddUnBan(self, data: ChannelUnbanEvent):
        unban = Unbandata(data.event.user_id,data.event.user_name,data.event.moderator_user_id,data.event.moderator_user_name)
        self.cursor.execute(f'INSERT INTO "UnBanLog" ("BannedUserID", "BannedUserName", "ModeratorID", "ModeratorUser") VALUES ("{unban.userID}", "{unban.userName}", "{unban.moderatorID}", "{unban.moderatorName}")')
        logging.debug(f"attempted to insert unban into database: {unban}")
        self.db.commit()

    def GetBasicCommands(self):
        commands = []
        self.cursor.execute('SELECT "Alias", "Return" FROM "BasicCommands"')
        commands = self.cursor.fetchall()
        return commands

    def AddBasicCommand(self, Alias:str, Output:str):
        self.cursor.execute(f'INSERT INTO "BasicCommands" ("Alias", "Return") VALUES ("{Alias}", "{Output}")')
        self.db.commit()

    def RemoveBasicCommand(self, Alias:str):
        self.cursor.execute(f'DELETE FROM "BasicCommands" WHERE Alias="{Alias}"')
        self.db.commit()

    def EditBasicCommand(self, Alias:str, Output:str):
        logging.info(f"Databaseconn.EditBasicCommand: Alias: {Alias} || Output: {Output}")
        self.cursor.execute(f'UPDATE "BasicCommands" SET "Return"="{Output}" WHERE Alias="{Alias}"')
        self.db.commit()


###minigame stuff

    def GetMiniGamePlayers(self):
        players: list[minigameplayer] = []
        logging.info(f"Databaseconn.GetMiniGamePlayers: returning players")
        self.cursor.execute('SELECT "TwitchID", "Name", "Points", "TotalWins", "TriviaWins", "HangmanWins" FROM "MiniGamePlayers"')
        out = self.cursor.fetchall()
        #logging.info(f"Databaseconn.GetMiniGamePlayers: out: {out}")
        return out

    def AddMiniGamePlayer(self, player:minigameplayer):
        logging.info(f"Databaseconn.AddMiniGamePlayer: player: {player}")
        self.cursor.execute(f'INSERT INTO "MiniGamePlayers"("TwitchID", "Name", "Points", "TotalWins", "TriviaWins", "HangmanWins") VALUES ("{player.id}","{player.name}", "{player.points}", "{player.total_wins}", "{player.trivia_wins}", "{player.hangman_Wins}")')
        self.db.commit()

    def UpdateMiniGamePlayer(self, player:minigameplayer):
        logging.info(f"Databaseconn.update_user: player: {player}")
        self.cursor.execute(f'UPDATE "MiniGamePlayers" SET "Points"="{player.points}", "TotalWins"="{player.total_wins}", "TriviaWins"="{player.trivia_wins}", "HangmanWins"="{player.hangman_Wins}" WHERE "TwitchID"="{player.id}"')
        self.db.commit()