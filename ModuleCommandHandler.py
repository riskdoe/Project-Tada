import asyncio
from Module import Module
from EventHandler import EventHandler
from twitchAPI.chat import ChatCommand
from twitchAPI.chat.middleware import UserRestriction as UsrRestriction
import logging
from twitchAPI.chat.middleware import UserRestriction as UsrRestriction
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_htmx import htmx, htmx_init

router = APIRouter()

htmx_init(templates = Jinja2Templates(directory="templates"))


basiccommandlist = []

def construct_command_page():
    if len(basiccommandlist) == 0:
        return {
            "commands": "None",
        }
    else:
        return {
            "commands": basiccommandlist,
        }

@router.get("/commands", response_class=HTMLResponse)
@htmx("commands", "index", construct_command_page)
def Get_commands(request: Request):
    pass



class CommandHandler(Module):
#    async def help_command(self,cmd: ChatCommand):
#        await self.event_Handler.send_message("help command")


    async def Faq_command(self,cmd: ChatCommand):
        await self.event_Handler.send_message("FAQ")
        for faq in self.faq:
            await self.event_Handler.send_message(faq)

    async def Rules_command(self,cmd: ChatCommand):
        await self.event_Handler.send_message("Rules")
        rulecount = 1
        for rule in self.rules:
            await self.event_Handler.send_message(f"{rulecount}: {rule}")
            rulecount = rulecount + 1

    async def commands_list(self,cmd: ChatCommand):
        commandlist :str = ""

        for command in self.basic_commands:
            commandlist += f"!{command} "
        await self.event_Handler.send_message(commandlist)

    async def ban_command(self,cmd: ChatCommand):
        logging.info(f"CommandHandler: {cmd.name} command called")
        if len(cmd.parameter) == 0:
            await self.event_Handler.send_message("Please provide User and reason")
            return
        res = cmd.parameter.split(' ', 1)
        user = res[0]
        Reason = res[1]
        await self.event_Handler.ban_user(user, Reason)
        logging.info(f"CommandHandler.ban_command: Params: '{user}' || '{Reason}'")
        #this should get auto logged in sql table due to onban function
    
    async def unban_command(self,cmd: ChatCommand):
        logging.info(f"CommandHandler: {cmd.name} command called")
        if len(cmd.parameter) == 0:
            await self.event_Handler.send_message("Please provide User")
            return
        if " " in cmd.parameter:
            await self.event_Handler.send_message("Please provide only one User")
            return
        user = cmd.parameter
        await self.event_Handler.unban_user(user)
        logging.info(f"CommandHandler.unban_command: Params: '{user}'")
        #this should get auto logged in sql table due to onban function

    #basic handler for basic response commands
    async def basic_handler(self, cmd: ChatCommand):
        output = self.basic_commands[cmd.name]
        logging.info(f"CommandHandler: {cmd.name} command called")
        await self.event_Handler.send_message(output)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

    def get_updated_basic_commands(self):
        basiccommandlist.clear()
        for basic_command in self.event_Handler.DBConn.GetBasicCommands():
            logging.info(f"CommandHandler: Added basic command: {basic_command}")
            self.basic_commands[basic_command[0]] = basic_command[1]
            self.event_Handler.TwitchAPI.CHAT.register_command(basic_command[0], self.basic_handler)
            basiccommandlist.append({
                "command": basic_command[0],
                "response": basic_command[1],
                "enabled": "True"
            })
            
#create commands for adding, removing, and editing commands
    def add_command(self,command, response):
        if command in self.basic_commands:
            return False
        self.event_Handler.TwitchAPI.CHAT.register_command(command, self.basic_handler)
        self.event_Handler.DBConn.AddBasicCommand(command, response)
        self.get_updated_basic_commands()
        logging.info(f"CommandHandler.add_command: Params: '{command}' || '{response}'")
        return True
   
    async def add_command_callback(self,cmd: ChatCommand):
        logging.info(f"CommandHandler: {cmd.name} command called")
        if len(cmd.parameter) == 0:
            await self.event_Handler.send_message("Please provide a command to add")
        else:
            res = cmd.parameter.split(' ', 1)
            if len(res) != 2:
                await self.event_Handler.send_message("Please provide a command and a response")
                return
            param1 = res[0]
            param2 = res[1]
            out = self.add_command(param1, param2)
            if out == False:
                await self.event_Handler.send_message("Command already exists")
            else:
                await self.event_Handler.send_message(f"Command {param1} added")


    def remove_command(self,command):
        if command not in self.basic_commands:
            return False
        self.event_Handler.TwitchAPI.CHAT.unregister_command(command)
        self.event_Handler.DBConn.RemoveBasicCommand(command)
        self.get_updated_basic_commands()
        logging.info(f"CommandHandler.remove_command: Params {command}")
        return True
    
    
    async def remove_command_callback(self,cmd: ChatCommand):
        logging.info(f"CommandHandler: {cmd.name} command called")
        if len(cmd.parameter) == 0:
            await self.event_Handler.send_message("Please provide a command to remove")
        else:
            param1 = cmd.parameter
            out = self.remove_command(param1)
            if out == False:
                await self.event_Handler.send_message("Command not found")
            else:
                await self.event_Handler.send_message(f"Command {param1} removed")
                

    def edit_command(self,command, response):
        if command not in self.basic_commands:
            return False
        self.event_Handler.DBConn.EditBasicCommand(command, response)
        self.get_updated_basic_commands()
        logging.info(f"CommandHandler.edit_command: Params {command}")
        return True

    async def edit_command_callback(self,cmd: ChatCommand):
        logging.info(f"CommandHandler: {cmd.name} command called")
        if len(cmd.parameter) == 0:
            await self.event_Handler.send_message("Please provide a command to edit")
        else:
            res = cmd.parameter.split(' ', 1)
            if len(res) != 2:
                await self.event_Handler.send_message("Please provide a command and a response")
                return
            param1 = res[0]
            param2 = res[1]
            out = self.edit_command(param1, param2)
            if out == False:
                await self.event_Handler.send_message("Command not found")
            else:
                await self.event_Handler.send_message(f"Command {param1} edited")

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

    async def get_stats(self,cmd: ChatCommand):
        logging.info(f"CommandHandler: {cmd.name} command called")
        if len(cmd.parameter) == 0:
            user = cmd.user.name
            stats = self.event_Handler.DBConn.get_user_stats(user)
            await self.event_Handler.send_message(f'{user}: total watchtime: {stats["totalwatchtime"] / 60}Mins, total messages: {stats["totalmessages"]}, total streams veiwed: {stats["totalstreamsveiwed"]}')
        else:
            user = cmd.parameter
            stats = self.event_Handler.DBConn.get_user_stats(user)
            if stats == None:
                await self.event_Handler.send_message(f'{user} not found')
            else:
                await self.event_Handler.send_message(f'{user}: total watchtime: {stats["totalwatchtime"] / 60}Mins, total messages: {stats["totalmessages"]}, total streams veiwed: {stats["totalstreamsveiwed"]}')


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

    
    def __init__(self, eventHandler: EventHandler):
        super().__init__("CommandHandler" , eventHandler)
        global commandlist
        self.event_Handler = eventHandler
        #faq list
        self.faq = eventHandler.config.faq_list
        #rules list
        self.rules = eventHandler.config.rules_list
        
        
        self.commands = {}
        #self.commands["help"] = self.help_command
        self.commands["commands"] = self.commands_list
        self.commands["add_command"] = self.add_command_callback
        self.commands["remove_command"] = self.remove_command_callback
        self.commands["edit_command"] = self.edit_command_callback
        self.commands["ban"] = self.ban_command
        self.commands["unban"] = self.unban_command
        self.commands["stats"] = self.get_stats       
        self.commands["faq"] = self.Faq_command
        self.commands["rules"] = self.Rules_command
        
        
        
        self.basic_commands = {}
        for command in self.commands:
            logging.info(f"CommandHandler: Added command: {command}")
            if (   command == "add_command" 
                or command == "remove_command" 
                or command == "edit_command"
                or command == "ban"
                or command == "unban"
                ):
                self.event_Handler.TwitchAPI.CHAT.register_command(
                    command,
                    self.commands[command],
                    command_middleware=[UsrRestriction(allowed_users=self.event_Handler.TwitchAPI.PERMITTED_USERS)])
            else:
                eventHandler.Add_command(command, self.commands[command])
        
        self.get_updated_basic_commands()


        logging.info("CommandHandler module loaded")
        
    async def on_webfrontend_message(self, command):
        if type(command) == dict:
            if list(command.keys())[0] == "Edit_command":
                self.edit_command(command["Edit_command"], command["Commandoutput"])
            if list(command.keys())[0] == "Add_command":
                self.add_command(command["Add_command"], command["Commandoutput"])
            if list(command.keys())[0] == "Delete_command":
                self.remove_command(command["Delete_command"])
            


