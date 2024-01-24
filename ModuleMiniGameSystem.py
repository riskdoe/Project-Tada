from Module import Module
from EventHandler import EventHandler
from twitchAPI.chat import ChatCommand
from twitchAPI.chat import Chat
import json
import random
from twitchAPI.chat.middleware import UserRestriction as UsrRestriction
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_htmx import htmx, htmx_init


router = APIRouter()

htmx_init(templates = Jinja2Templates(directory="templates"))

game = "none"
roundOver = "false"
roundcorrectanswer = ""
roundwinner = ""
roundquestion = ""
roundanswers = ""
roundcategory = ""
roundguessedletters = []
roundwrongletters = []
roundcorrectletters = []
roundmisplacedletters = []
numberofguesses = 0


def construct_minigamebox():
    if game == "trivia":
        return {"game": game,
                "roundover": roundOver,
                "winner": roundwinner,
                "question": roundquestion,
                "answers": roundanswers,
                "correctanswer": roundcorrectanswer,
                "category": roundcategory,
                "number_of_attempts": numberofguesses}
    elif game == "wordle":
        return {"game": game,
                "roundover": roundOver,
                "winner": roundwinner,
                "roundword": roundcorrectanswer,
                "guessedletters": roundguessedletters, 
                "wrongletters": roundwrongletters,
                "misplacedletters": roundmisplacedletters,
                "correctletters": roundcorrectletters,
                "number_of_attempts": numberofguesses}
    else:
        return {"game": game}

@router.get("/minigamebox", response_class=HTMLResponse)
@htmx("minigamebox", "index", construct_minigamebox)
def get_minigamebox(request: Request):
    pass




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
        global roundOver, roundwinner, numberofguesses
        numberofguesses += 1
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
            
            roundOver = "true"
            roundwinner = cmd.user.name
            
        
            self.RoundOver = attempt
            self.Winner = cmd.user.name
            
            self.Event_Handler.TwitchAPI.remove_command("a")
            self.Event_Handler.TwitchAPI.remove_command("b")
            self.Event_Handler.TwitchAPI.remove_command("c")
            self.Event_Handler.TwitchAPI.remove_command("d")
            self.Event_Handler.TwitchAPI.remove_command("question")
            self.Event_Handler.TwitchAPI.remove_command("answers")
            self.Event_Handler.TwitchAPI.remove_command("gamehelp")
            
            
            #TODO: update database
            self.Creator.get_player(cmd.user.name).trivia_wins += 1
            self.Creator.get_player(cmd.user.name).total_wins += 1
            self.Creator.get_player(cmd.user.name).points += 100
            
            self.Event_Handler.DBConn.UpdateMiniGamePlayer(self.Creator.get_player(cmd.user.name))
            
            await self.Event_Handler.send_message(f"{cmd.user.name} answered correctly and gained 100 points")
            await self.Event_Handler.send_message(f"{cmd.user.name} won the round and gained 100 points, Round over.")
            
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
        self.type = "trivia"
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
        #assign data for webfrontend
        global game, roundOver, roundwinner, roundquestion, roundanswers, roundcorrectanswer, roundcategory, numberofguesses
        game = "trivia"
        roundOver = "false"
        roundcorrectanswer = self.RoundQuestion.answers[int(self.RoundQuestion.correctAnswerIndex)]
        roundwinner = "no one yet"
        roundquestion = self.RoundQuestion.question
        roundanswers = self.RoundQuestion.answers
        roundcategory = self.RoundQuestion.category
        numberofguesses = 0
        self.Event_Handler.loginfo("minigame_trivia", f"trivia started. question is: {self.RoundQuestion}")
        self.Event_Handler.loginfo("minigame_trivia", f"trivia started. answer is: {self.RoundQuestion.answers[int(self.RoundQuestion.correctAnswerIndex)]}")
        self.Event_Handler.eventtofrontend("minigame_trivia", f"trivia started. question is: {self.RoundQuestion}")
        self.Event_Handler.eventtofrontend("minigame_trivia", f"trivia started. answer is: {self.RoundQuestion.answers[int(self.RoundQuestion.correctAnswerIndex)]}")

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
class minigame_wordle():
    def __init__(self, Creator, Eventhandler: EventHandler, Chat: Chat):
        self.type = "wordle"
        self.Creator = Creator
        self.event_Handler = Eventhandler
        self.Chat = Chat        
        f = open("Wordle_Wordlist.json", "r")
        data = json.load(f)
        words = data["data"]
        self.word = words[random.randint(0,len(words)-1)]
        self.word = self.word.lower() 
        self.event_Handler.loginfo("minigame_wordle", f"wordle started. word is: {self.word}")
        self.event_Handler.eventtofrontend("minigame_wordle", f"wordle started. word is: {self.word}")
        
        self.correct_letters = None
        self.misplaced_letters = None
        self.misplaced_letters = None
        
        global game, roundOver, roundwinner, roundcorrectanswer, roundguessedletters, roundwrongletters, roundmisplacedletters, roundcorrectletters, numberofguesses
                
        game = "wordle"
        roundOver = "false"
        roundwinner = "no one yet"
        roundcorrectanswer = self.word
        roundguessedletters = []
        roundwrongletters = []
        roundmisplacedletters = []
        roundcorrectletters = []
        numberofguesses = 0
        

        
    async def make_guess(self, cmd:ChatCommand):
        global roundOver, roundwinner, roundcorrectanswer, roundguessedletters, roundwrongletters, roundmisplacedletters, roundcorrectletters, numberofguesses

        if len(cmd.parameter) != 5:
            await self.event_Handler.send_message("Guess a 5 letter word")
            return
        guess = cmd.parameter.lower()
        #if they guess the word assign points
        if guess == self.word:
            roundOver = "true"
            roundwinner = cmd.user.name
            await cmd.reply(f"{cmd.user.name} Correctly guessed the word {self.word}")
            await self.event_Handler.send_message(f"{cmd.user.name} won the round and gained 100 points, Round over.")
            self.event_Handler.TwitchAPI.remove_command("guess")
            self.event_Handler.TwitchAPI.remove_command("gamehelp")
            self.Creator.current_game = None
            #TODO: update database
            self.Creator.get_player(cmd.user.name).hangman_Wins += 1
            self.Creator.get_player(cmd.user.name).total_wins += 1
            self.Creator.get_player(cmd.user.name).points += 100
            
            self.event_Handler.DBConn.UpdateMiniGamePlayer(self.Creator.get_player(cmd.user.name))
        #else game logic
        else:
            
            #check for correct letters
            correct_letters = {
                letter for letter, correct in zip(guess, self.word) if letter == correct
            }
            misplaced_letters = set(guess) & set(self.word) - correct_letters
            wrong_letters = set(guess) - set(self.word)
            

            
            #tidy up output
            output1 = ""
            output2 = ""
            output3 = ""
            if len(correct_letters) == 0:
                output1 = "No correct letters"
            elif len(correct_letters) >= 1:
                output1 = "correct letters: " + " ,".join(sorted(correct_letters))

            if len(misplaced_letters) == 0:
                output2 = "No misplaced letters"
            elif len(misplaced_letters) >= 1:
                output2 = "misplaced letters: " + " ,".join(sorted(misplaced_letters))

            if len(wrong_letters) == 0:
                output3 = "No wrong letters"
            elif len(wrong_letters) >= 1:
                output3 = "wrong letters: " + " ,".join(sorted(wrong_letters))
            
            numberofguesses += 1
            guesslist = guess.split()
            for letter in guesslist:
                if letter not in roundguessedletters:
                    roundguessedletters.append(letter)
            for letter in wrong_letters:
                if letter not in roundwrongletters:
                    roundwrongletters.append(letter)
            for letter in correct_letters:
                if letter not in roundcorrectletters:
                    roundcorrectletters.append(letter)
            for letter in misplaced_letters:
                if letter not in roundmisplacedletters:
                    roundmisplacedletters.append(letter)
            
            #send output   
            await cmd.reply(f"guessed {guess}")
            await self.event_Handler.send_message(output1)
            await self.event_Handler.send_message(output2)
            await self.event_Handler.send_message(output3)


    async def wordle_help(self, cmd: ChatCommand):
        await self.event_Handler.send_message(f"!guess to guess a word")
        await self.event_Handler.send_message(f"!wordlehelp to see commands")
        await self.event_Handler.send_message(f"When you guess a word. I will tell you what letters are correct, misplaced, and wrong.")
    
    def start(self):
        self.event_Handler.TwitchAPI.add_command("guess", self.make_guess)
        self.event_Handler.TwitchAPI.add_command("gamehelp", self.wordle_help)



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
                    cmd.user.name)
            self.players.append(player)
            self.event_Handler.loginfo(self.name, f'{cmd.user.name}: {cmd.user.name} added to minigame system')
            self.event_Handler.eventtofrontend(self.name, f'{cmd.user.name}: {cmd.user.name} added to minigame system')
            self.event_Handler.DBConn.AddMiniGamePlayer(player)
            await cmd.reply(f"you have been added to the minigame system")


    async def user_get_points(self, cmd: ChatCommand):
        if not any(x.name == cmd.user.name for x in self.players):
            await cmd.reply(f"you are not signed up for the minigame system")
            pass
        else:
            player = self.get_player(cmd.user.name)
            await cmd.reply(f": {player.points} points")

    async def user_get_stats(self, cmd: ChatCommand):
        if not any(x.name == cmd.user.name for x in self.players):
            await cmd.reply(f"you are not signed up for the minigame system")
            pass
        else:
            player = self.get_player(cmd.user.name)
            await cmd.reply(f": {player.points} points, {player.total_wins} wins({player.trivia_wins} trivia wins, {player.hangman_Wins} wordle wins)")

    #run when user asks for help
    async def minigame_help(self, cmd: ChatCommand):
        await self.event_Handler.send_message(f"!signup to join the minigame system (only ever needs to be run once)")
        await self.event_Handler.send_message(f"!points to see your points")
        await self.event_Handler.send_message(f"!stats to see your overall stats")
        await self.event_Handler.send_message(f"!gamehelp to see game specific commands for currently running game") 

    async def start_minigame(self, type:str):
        if type == "trivia":
            self.current_game = minigame_trivia(self,self.event_Handler, self.event_Handler.TwitchAPI.CHAT)
            await self.event_Handler.send_message(f"{self.current_game.get_question()}")
            await self.event_Handler.send_message(f"Answers")
            await self.event_Handler.send_message(f"!a: {self.current_game.get_answer(0)}")
            await self.event_Handler.send_message(f"!b: {self.current_game.get_answer(1)}")
            await self.event_Handler.send_message(f"!c: {self.current_game.get_answer(2)}")
            await self.event_Handler.send_message(f"!d: {self.current_game.get_answer(3)}")
            await self.event_Handler.send_message(f"!gamehelp to see commands")
            self.current_game.start()
        elif type == "wordle":
            self.current_game = minigame_wordle(self,self.event_Handler, self.event_Handler.TwitchAPI.CHAT)
            await self.event_Handler.send_message(f"Guess a 5 letter word")
            await self.event_Handler.send_message(f"!gamehelp to see commands")
            self.current_game.start()

    #start trivia game
    async def start_triva(self, cmd: ChatCommand):
        await self.start_minigame("trivia")

    #start hangman game
    async def start_wordle(self, cmd: ChatCommand):
        await self.start_minigame("wordle")


    async def on_webfrontend_message(self, command:str):
        if command == "start_trivia":
            await self.start_minigame("trivia")
        if command == "start_wordle":
            await self.start_minigame("wordle")

    #create minigame class
    def __init__(self, eventHandler: EventHandler):
        super().__init__("MiniGameSystem", eventHandler)
        self.players: list[minigameplayer] = []
        
        for player in self.event_Handler.DBConn.GetMiniGamePlayers():
            person = minigameplayer(player[0], player[1], player[2], player[3], player[4], player[5])
            self.players.append(person)
            self.event_Handler.loginfo(self.name, f'{person.name} added to minigame system loaded from db')
        self.current_game = None
        #create minigame commands
        self.event_Handler.TwitchAPI.add_command("signup", self.on_signup)
        self.event_Handler.TwitchAPI.add_command("mghelp", self.minigame_help)
        self.event_Handler.TwitchAPI.add_command("mgpoints", self.user_get_points)
        self.event_Handler.TwitchAPI.add_command("mgstats", self.user_get_stats)
        self.event_Handler.TwitchAPI.CHAT.register_command("starttrivia", self.start_triva,command_middleware=[UsrRestriction(allowed_users=self.event_Handler.TwitchAPI.PERMITTED_USERS)])
        self.event_Handler.TwitchAPI.CHAT.register_command("startwordle", self.start_wordle,command_middleware=[UsrRestriction(allowed_users=self.event_Handler.TwitchAPI.PERMITTED_USERS)])
        
        self.event_Handler.loginfo(self.name, " module loaded")
        
    #get list of players
    def get_players(self):
        return self.players

    #get player by name
    def get_player(self, name: str):
        for player in self.players:
            if player.name == name:
                return player
        return None

