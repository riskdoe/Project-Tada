import sqlite3
import logging
from twitchAPI.chat import ChatMessage
from twitchAPI.object.eventsub import ChannelBanEvent,ChannelUnbanEvent
import datetime
from StreamClasses import *

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
        self.cursor.execute('CREATE TABLE IF NOT EXISTS "Messages" ("ID" INTEGER NOT NULL, "TwitchID" TEXT NOT NULL, "UserName" TEXT NOT NULL,"Message" TEXT NOT NULL,"UnixTimeStamp" INTEGER NOT NULL, "Stream_ID" INTEGER NOT NULL,PRIMARY KEY("ID" AUTOINCREMENT))')
        self.db.commit()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS "BanLog" ("ID" INTEGER NOT NULL, "BannedUserID" TEXT NOT NULL, "BannedUserName" TEXT NOT NULL, "ModeratorID" TEXT NOT NULL, "ModeratorUser" TEXT NOT NULL,"BanReason" TEXT NOT NULL, "BanTime" INTEGER NOT NULL,"IsPermanent" INTEGER NOT NULL DEFAULT 0, PRIMARY KEY("ID" AUTOINCREMENT))')
        self.db.commit()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS "UnBanLog" ("ID" INTEGER NOT NULL, "BannedUserID" TEXT NOT NULL, "BannedUserName" TEXT NOT NULL, "ModeratorID" TEXT NOT NULL, "ModeratorUser" TEXT NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT))')
        self.db.commit()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS "BasicCommands" ("ID" INTEGER NOT NULL, "Alias" TEXT NOT NULL, "Return" TEXT NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT))')
        self.db.commit()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS "MiniGamePlayers" ("ID" INTEGER NOT NULL, "TwitchID" TEXT NOT NULL , "Name" TEXT NOT NULL,"Points" INTEGER NOT NULL,"TotalWins" INTEGER NOT NULL,"TriviaWins" INTEGER NOT NULL,"HangmanWins" INTEGER NOT NULL,PRIMARY KEY("ID" AUTOINCREMENT))')
        self.db.commit()
        #stat tracking databases
        self.cursor.execute('CREATE TABLE IF NOT EXISTS "Stream_Stat" ("ID" INTEGER NOT NULL, "StreamStart" INTEGER NOT NULL , "StreamEnd" INTEGER NOT NULL,"Duration" INTEGER NOT NULL, "NumberofChatters" INTEGER NOT NULL,"NumberofMessages" INTEGER NOT NULL,PRIMARY KEY("ID" AUTOINCREMENT))')
        self.db.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS 'stat_title'('ID' INTEGER NOT NULL,'stream_ID' INTEGER, 'title' TEXT NOT NULL , 'event_time' INTEGER NOT NULL, PRIMARY KEY('ID' AUTOINCREMENT), FOREIGN KEY('stream_ID') REFERENCES 'Stream_Stat'('ID'))")
        self.db.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS 'stat_game' ('ID' INTEGER NOT NULL, 'stream_ID' INTEGER, 'gametitle' TEXT NOT NULL , 'event_time' INTEGER NOT NULL, PRIMARY KEY('ID' AUTOINCREMENT), FOREIGN KEY('stream_ID') REFERENCES 'Stream_Stat'('ID'))")
        self.db.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS 'stat_follow' ('ID' INTEGER NOT NULL, 'stream_ID' INTEGER, 'follower_name' TEXT NOT NULL, 'event_time' INTEGER NOT NULL, PRIMARY KEY('ID' AUTOINCREMENT), FOREIGN KEY('stream_ID') REFERENCES 'Stream_Stat'('ID'))")
        self.db.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS 'stat_sub' ('ID' INTEGER NOT NULL, 'stream_ID' INTEGER, 'sub_name' TEXT NOT NULL, 'event_time' INTEGER NOT NULL, 'sub_message' TEXT NOT NULL, 'sub_tier' TEXT NOT NULL, 'is_resub' INTEGER NOT NULL, PRIMARY KEY('ID' AUTOINCREMENT), FOREIGN KEY('stream_ID') REFERENCES 'Stream_Stat'('ID'))")
        self.db.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS 'stat_sub_gift' ('ID' INTEGER NOT NULL, 'stream_ID' INTEGER, 'sub_name' TEXT NOT NULL, 'event_time' INTEGER NOT NULL, 'sub_message' TEXT NOT NULL, 'sub_tier' TEXT NOT NULL, PRIMARY KEY('ID' AUTOINCREMENT), FOREIGN KEY('stream_ID') REFERENCES 'Stream_Stat'('ID'))")
        self.db.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS 'stat_raid' ('ID' INTEGER NOT NULL, 'stream_ID' INTEGER, 'raid_user' TEXT NOT NULL, 'event_time' INTEGER NOT NULL, 'raid_viewers' INTEGER NOT NULL, PRIMARY KEY('ID' AUTOINCREMENT), FOREIGN KEY('stream_ID') REFERENCES 'Stream_Stat'('ID'))")
        self.db.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS 'stat_cheer' ('ID' INTEGER NOT NULL, 'stream_ID' INTEGER, 'Cheer_user' TEXT NOT NULL, 'event_time' INTEGER NOT NULL, 'cheer_amount' INTEGER NOT NULL, PRIMARY KEY('ID' AUTOINCREMENT), FOREIGN KEY('stream_ID') REFERENCES 'Stream_Stat'('ID'))")
        self.db.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS 'stat_shoutout' ('ID' INTEGER NOT NULL, 'stream_ID' INTEGER, 'shoutout_user' TEXT NOT NULL, 'event_time' INTEGER NOT NULL, PRIMARY KEY('ID' AUTOINCREMENT), FOREIGN KEY('stream_ID') REFERENCES 'Stream_Stat'('ID'))")
        self.db.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS 'stat_watchtime' ('ID' INTEGER NOT NULL, 'stream_ID' INTEGER, 'User' TEXT NOT NULL, 'WatchTime' INTEGER NOT NULL, PRIMARY KEY('ID' AUTOINCREMENT), FOREIGN KEY('stream_ID') REFERENCES 'Stream_Stat'('ID'))")
        self.db.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS 'stat_total_watchtime' ('ID' INTEGER NOT NULL, 'User' TEXT NOT NULL, 'WatchTime' INTEGER NOT NULL, PRIMARY KEY('ID' AUTOINCREMENT))")
        self.db.commit()
        
        if self.getnextStreamID() == 1:
            self.cursor.execute('INSERT INTO "Stream_Stat" ("ID", "StreamStart", "StreamEnd", "Duration", "NumberofChatters", "NumberofMessages") VALUES ("1", "0", "0", "0", "0", "0")')
            self.db.commit()
        
        self.getnextStreamID()
        
        
        

    def AddMessage(self, data: cmessage):
        message = data
        self.cursor.execute(f'INSERT INTO "main"."Messages" ("TwitchID", "UserName", "Message", "UnixTimeStamp", "Stream_ID") VALUES ("{message.id}", "{message.user}", "{message.text}", "{message.timestamp}", "{self.eventHandler.streamID}")')
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


    def getnextStreamID(self):
        self.cursor.execute('SELECT MAX(ID) FROM "Stream_Stat"')
        out = self.cursor.fetchall()
        if out[0][0] == None:
            return 1
        else:
            return out[0][0] + 1
        
    def get_all_user_watchtime(self):
        self.cursor.execute(f'SELECT "User", "WatchTime" FROM "stat_total_watchtime"')
        out = self.cursor.fetchall()
        return out

    def updatetotalwatchtime(self, user:str, watchtime:int):
        logging.info(f"Databaseconn.updatetotalwatchtime: user: {user} || watchtime: {watchtime}")
        self.cursor.execute(f"UPDATE 'stat_total_watchtime' SET 'WatchTime'='{watchtime}' WHERE User='{user}'")
        self.db.commit()
        
    def addveiwer(self, user:str, watchtime:int):
        self.cursor.execute(f"INSERT INTO 'stat_total_watchtime' ('User', 'WatchTime') VALUES ('{user}', '{watchtime}')")
        self.db.commit()

    def add_stream(self, instance:stream_instance):
        logging.info("Databaseconn.dumpstreamdetails: dumping stream details")
        self.cursor.execute(f'INSERT INTO "Stream_Stat"("StreamStart", "StreamEnd", "Duration", "NumberofChatters", "NumberofMessages") VALUES ("{instance.stream_start_time}", "{instance.stream_end_time}", "{instance.stream_duration}", "{len(instance.active_chatter)}", "{instance.num_of_messages_during_stream}")')
        self.db.commit()
        streamid = instance.stream_id
        logging.info(f"Databaseconn.dumpstreamdetails: streamid: {streamid}")
        for title in instance.stream_title:
            self.cursor.execute(f'INSERT INTO "stat_title"("stream_ID", "title", "event_time") VALUES ("{streamid}", "{title.title}", "{title.event_time}")')
            self.db.commit()
        for game in instance.stream_game:
            self.cursor.execute(f'INSERT INTO "stat_game"("stream_ID", "gametitle", "event_time") VALUES ("{streamid}", "{game.game}", "{game.event_time}")')
            self.db.commit()
        for follow in instance.follows_during_stream:
            self.cursor.execute(f'INSERT INTO "stat_follow"("stream_ID", "follower_name", "event_time") VALUES ("{streamid}", "{follow.user}", "{follow.event_time}")')
            self.db.commit()
        for sub in instance.subs_during_stream:
            self.cursor.execute(f'INSERT INTO "stat_sub"("stream_ID", "sub_name", "event_time", "sub_message", "sub_tier", "is_resub") VALUES ("{streamid}", "{sub.user}", "{sub.event_time}", "{sub.submessage}", "{sub.sublevel}", "{sub.resub}")')
            self.db.commit()
        for giftsub in instance.giftsubs_during_stream:
            self.cursor.execute(f'INSERT INTO "stat_sub_gift"("stream_ID", "sub_name", "event_time", "sub_message", "sub_tier") VALUES ("{streamid}", "{giftsub.user}", "{giftsub.event_time}", "{giftsub.submessage}", "{giftsub.sublevel}")')
            self.db.commit()
        for raid in instance.raids_during_stream:
            self.cursor.execute(f'INSERT INTO "stat_raid"("stream_ID", "raid_user", "event_time", "raid_viewers") VALUES ("{streamid}", "{raid.user}", "{raid.event_time}", "{raid.numberofraiders}")')
            self.db.commit()
        for cheer in instance.cheers_during_stream:
            self.cursor.execute(f'INSERT INTO "stat_cheer"("stream_ID", "Cheer_user", "event_time", "cheer_amount") VALUES ("{streamid}", "{cheer.user}", "{cheer.event_time}", "{cheer.bits}")')
            self.db.commit()
        for shoutout in instance.shoutouts_during_stream:
            self.cursor.execute(f'INSERT INTO "stat_shoutout"("stream_ID", "shoutout_user", "event_time") VALUES ("{streamid}", "{shoutout.user}", "{shoutout.event_time}")')
            self.db.commit()
        
        for user in instance.veiwer_watchtime:
            self.cursor.execute(f'INSERT INTO "stat_watchtime"("stream_ID", "User", "WatchTime") VALUES ("{streamid}", "{user}", "{instance.veiwer_watchtime[user]}")')
            self.db.commit()



    def get_user_stats(self, user:str):
        user = user.lower()
        #count number of streams
        #count total watch time
        #count total messages sent
        totalstreamsveiwed = 0
        totalwatchtime = 0
        totalmessages = 0
        
        self.cursor.execute(f"SELECT COUNT(*) FROM 'stat_watchtime' WHERE User='{user}'")
        out = self.cursor.fetchall()
        totalstreamsveiwed = out[0][0]
        
        self.cursor.execute(f"SELECT WatchTime FROM 'stat_total_watchtime' WHERE User='{user}'")
        out = self.cursor.fetchall()
        if len(out) == 0:
            return None
        totalwatchtime = out[0][0]

        
        self.cursor.execute(f"SELECT COUNT(*) FROM 'Messages' WHERE UserName='{user}'")
        out = self.cursor.fetchall()
        totalmessages = out[0][0]
        
        stats = {
            "totalstreamsveiwed": totalstreamsveiwed,
            "totalwatchtime": totalwatchtime,
            "totalmessages": totalmessages
            }
        return stats
