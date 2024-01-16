import asyncio
from Module import Module
from EventHandler import EventHandler
from twitchAPI.chat import ChatCommand
from twitchAPI.chat.middleware import UserRestriction as UsrRestriction
import logging

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
        
    #create commands for adding, removing, and editing commands
    async def add_command(self,cmd: ChatCommand):
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
            if param1 in self.basic_commands:
                await self.event_Handler.send_message("Command already exists")
                return
            self.basic_commands[param1] = param2
            self.event_Handler.TwitchAPI.CHAT.register_command(param1, self.basic_handler)
            self.event_Handler.DBConn.AddBasicCommand(param1, param2)
            await self.event_Handler.send_message(f"Command {param1} added")
            logging.info(f"CommandHandler.add_command: Params: '{param1}' || '{param2}'")

    async def remove_command(self,cmd: ChatCommand):
        logging.info(f"CommandHandler: {cmd.name} command called")
        if len(cmd.parameter) == 0:
            await self.event_Handler.send_message("Please provide a command to remove")
        else:
            result = self.basic_commands.pop(cmd.parameter, "failed")
            if result == "failed":
                await self.event_Handler.send_message("Command not found")
            else:
                self.event_Handler.TwitchAPI.CHAT.unregister_command(cmd.parameter)
                self.event_Handler.DBConn.RemoveBasicCommand(cmd.parameter)
                await self.event_Handler.send_message(f"Command {cmd.parameter} removed")
            logging.info(f"CommandHandler.remove_command: Params {cmd.parameter}")

    async def edit_command(self,cmd: ChatCommand):
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
            if param1 not in self.basic_commands:
                await self.event_Handler.send_message("Command not found")
                return
            self.basic_commands[param1] = param2
            self.event_Handler.DBConn.EditBasicCommand(param1, param2)
            logging.info(f"CommandHandler.edit_command: Params {cmd.parameter}")
            await self.event_Handler.send_message(f"Command {param1} edited")
            

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

    
    def __init__(self, eventHandler: EventHandler):
        super().__init__("CommandHandler" , eventHandler)
        self.event_Handler = eventHandler
        #faq list
        self.faq = eventHandler.config.faq_list
        #rules list
        self.rules = eventHandler.config.rules_list
        
        
        self.commands = {}
        #self.commands["help"] = self.help_command
        self.commands["commands"] = self.commands_list
        self.commands["add_command"] = self.add_command
        self.commands["remove_command"] = self.remove_command
        self.commands["edit_command"] = self.edit_command
        self.commands["ban"] = self.ban_command
        self.commands["unban"] = self.unban_command
        
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
        
        for basic_command in self.event_Handler.DBConn.GetBasicCommands():
            logging.info(f"CommandHandler: Added basic command: {basic_command}")
            self.basic_commands[basic_command[0]] = basic_command[1]
            self.event_Handler.TwitchAPI.CHAT.register_command(basic_command[0], self.basic_handler)

            
        logging.info("CommandHandler module loaded")


