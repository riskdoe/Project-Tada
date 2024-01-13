from Module import Module
from EventHandler import EventHandler
from twitchAPI.chat import ChatMessage,ChatUser, ChatCommand
import logging
from twitchAPI.twitch import Twitch
from twitchAPI.chat import Chat
import json
import random
import os
from twitchAPI.chat.middleware import UserRestriction as UsrRestriction


class minigameplayer():
    def __init__(self, id: str, name: str, mod: bool, subscriber: bool, vip: bool, 
                 points: int = 0, total_wins: int = 0,
                 trivia_wins: int = 0,
                 hangman_Wins: int = 0):
        self.id = id
        self.name = name
        self.mod = mod
        self.subscriber = subscriber
        self.vip = vip
        self.points = points
        self.total_wins = total_wins
        
        #Trivia
        self.trivia_wins = trivia_wins
        
        #hangman
        self.hangman_Wins = hangman_Wins

    def __str__(self):
        return f"{self.name}: {self.points} points, {self.total_wins} wins"

class trivia_question():
    def __init__(self, question: str, answers: list[str], correctAnswerIndex: int, category: str):
        self.question = question
        self.answers = answers
        self.correctAnswerIndex = correctAnswerIndex
        self.category = category

    def __str__(self):
        return f"{self.question} || {self.answers} || {self.correctAnswerIndex} || {self.category}"

class minigame_trivia():
    #run when user asks for help
    async def trivia_help(self, cmd: ChatCommand):
        await self.Event_Handler.send_message(f"!a, !b, !c, !d to answer")
        await self.Event_Handler.send_message(f"!question to see the question")
        await self.Event_Handler.send_message(f"!answers to see the answers") 

    #run when user guesses answer
    async def user_answer(self, cmd: ChatCommand):
        #check if user is signed up
        if not any(x.name == cmd.user.name for x in self.Creator.get_players()):
            await self.Event_Handler.send_message(f"{cmd.user.name} is not signed up for the minigame system")
            return
        #if signed up check if their anwser is correct
        attempt : bool = False
        if cmd.name == "a":
            attempt = self.attempt_answer("0")
        elif cmd.name == "b":
            attempt = self.attempt_answer("1")
        elif cmd.name == "c":
            attempt = self.attempt_answer("2")
        elif cmd.name == "d":
            attempt = self.attempt_answer("3")
        
        #if correct end round and assign points
        if attempt:
        
            self.RoundOver = attempt
            self.Winner = cmd.user.name
            
            self.Event_Handler.TwitchAPI.remove_command("a")
            self.Event_Handler.TwitchAPI.remove_command("b")
            self.Event_Handler.TwitchAPI.remove_command("c")
            self.Event_Handler.TwitchAPI.remove_command("d")
            self.Event_Handler.TwitchAPI.remove_command("question")
            self.Event_Handler.TwitchAPI.remove_command("answers")
            self.Event_Handler.TwitchAPI.remove_command("triviahelp")
            self.Event_Handler.TwitchAPI.remove_command("thelp")
            
            
            #TODO: update database
            self.Creator.get_player(cmd.user.name).trivia_wins += 1
            self.Creator.get_player(cmd.user.name).total_wins += 1
            self.Creator.get_player(cmd.user.name).points += 100
            
            await self.Event_Handler.send_message(f"{cmd.user.name} answered correctly and gained 100 points")
            await self.Event_Handler.send_message(f"{cmd.user.name} won the round, Round over.")
            
            self.Creator.current_game = None

    #send out questions
    async def aGetQuestion(self, cmd: ChatCommand):
        await self.Event_Handler.send_message(f"{self.get_question()}")

    #send out answers
    async def aGetAnswers(self, cmd: ChatCommand):
        await self.Event_Handler.send_message(f"!a: {self.get_answer(0)}")
        await self.Event_Handler.send_message(f"!b: {self.get_answer(1)}")
        await self.Event_Handler.send_message(f"!c: {self.get_answer(2)}")
        await self.Event_Handler.send_message(f"!d: {self.get_answer(3)}")

    #create game
    def __init__(self, Creator, Eventhandler: EventHandler, Chat: Chat):
        self.Event_Handler = Eventhandler
        self.Chat = Chat
        self.Creator = Creator
        f = open("Triva_Questions.json", "r")
        data = json.load(f)
        Catagories = data["Categories"]
        Example_Category = Catagories["Example"]
        RoundQuestionJson = Example_Category[random.randint(0,len(Example_Category)-1)]
        self.RoundQuestion = trivia_question(RoundQuestionJson["question"], RoundQuestionJson["correctAnswerChoices"], RoundQuestionJson["correctAnswerIndex"], "Example")
        self.RoundOver = False
        self.Winner = ""
        #create commands for minigame

    #return question
    def get_question(self):
        return self.RoundQuestion.question

    #return list of answers
    def get_answers(self):
        return self.RoundQuestion.answers

    #get answer by index
    def get_answer(self, index: int = None):
        return self.RoundQuestion.answers[index]

    #check if answer is correct
    def attempt_answer(self, answer: str):
        if answer == self.RoundQuestion.correctAnswerIndex:
            self.RoundOver = True
        return self.RoundOver

    #get correct answer index (debug only)
    def get_correct_answer_index(self):
        '''debug only'''
        return self.RoundQuestion.correctAnswerIndex

    #start game   
    def start(self):
        self.Event_Handler.TwitchAPI.add_command("a", self.user_answer)
        self.Event_Handler.TwitchAPI.add_command("b", self.user_answer)
        self.Event_Handler.TwitchAPI.add_command("c", self.user_answer)
        self.Event_Handler.TwitchAPI.add_command("d", self.user_answer)
        self.Event_Handler.TwitchAPI.add_command("question", self.aGetQuestion)
        self.Event_Handler.TwitchAPI.add_command("answers", self.aGetAnswers)
        self.Event_Handler.TwitchAPI.add_command("gamehelp", self.trivia_help)


#TODO: make hangman game
class minigame_hangman():
    def __init__(self):
        pass



class MinigameSystem(Module):
    #run when user signs up
    async def on_signup(self, cmd: ChatCommand):
        #check if user already signed up. if so tell them
        if any(x.name == cmd.user.name for x in self.players):
            await cmd.reply(f"you are already signed up")
            pass
        #if they are not sign them up
        else:
            player = minigameplayer(
                    cmd.user.id, 
                    cmd.user.name, 
                    cmd.user.mod, 
                    cmd.user.subscriber, 
                    cmd.user.vip)
            self.players.append(player)
            logging.info(f'{self.name}: {cmd.user.name} added to minigame system')
            logging.info(player)
            await cmd.reply(f"you have been added to the minigame system")
            #TODO: record the user in DATABASE

    async def user_get_points(self, cmd: ChatCommand):
        if not any(x.name == cmd.user.name for x in self.players):
            await cmd.reply(f"you are not signed up for the minigame system")
            pass
        else:
            player = self.get_player(cmd.user.name)
            await cmd.reply(f"{player.name}: {player.points} points")

    async def user_get_stats(self, cmd: ChatCommand):
        if not any(x.name == cmd.user.name for x in self.players):
            await cmd.reply(f"you are not signed up for the minigame system")
            pass
        else:
            player = self.get_player(cmd.user.name)
            await cmd.reply(f"{player.name}: {player.points} points, {player.total_wins} wins({player.trivia_wins} trivia wins, {player.hangman_Wins} hangman wins)")

    #run when user asks for help
    async def minigame_help(self, cmd: ChatCommand):
        await self.event_Handler.send_message(f"!signup to join the minigame system (only ever needs to be run once)")
        await self.event_Handler.send_message(f"!points to see your points")
        await self.event_Handler.send_message(f"!stats to see your overall stats")
        await self.event_Handler.send_message(f"!gamehelp to see game specific commands for currently running game") 

    #start trivia game
    async def start_triva(self, cmd: ChatCommand):
        self.current_game = minigame_trivia(self,self.event_Handler, self.event_Handler.TwitchAPI.CHAT)
        await self.event_Handler.send_message(f"{self.current_game.get_question()}")
        await self.event_Handler.send_message(f"Answers")
        await self.event_Handler.send_message(f"!a: {self.current_game.get_answer(0)}")
        await self.event_Handler.send_message(f"!b: {self.current_game.get_answer(1)}")
        await self.event_Handler.send_message(f"!c: {self.current_game.get_answer(2)}")
        await self.event_Handler.send_message(f"!d: {self.current_game.get_answer(3)}")
        await self.event_Handler.send_message(f"!gamehelp to see commands")
        self.current_game.start()

    #create minigame class
    def __init__(self, eventHandler: EventHandler):
        super().__init__("MiniGameSystem", eventHandler)
        self.players = []
        self.current_game = None
        #create minigame commands
        self.event_Handler.TwitchAPI.add_command("signup", self.on_signup)
        self.event_Handler.TwitchAPI.add_command("minigamehelp",self.minigame_help)
        self.event_Handler.TwitchAPI.add_command("mghelp", self.minigame_help)
        self.event_Handler.TwitchAPI.CHAT.register_command("starttrivia", self.start_triva,command_middleware=[UsrRestriction(allowed_users=self.event_Handler.TwitchAPI.PERMITTED_USERS)])
        
    #get list of players
    def get_players(self):
        return self.players

    #get player by name
    def get_player(self, name: str):
        for player in self.players:
            if player.name == name:
                return player
        return None

