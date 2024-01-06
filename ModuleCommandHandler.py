import asyncio
from Module import Module
from EventHandler import EventHandler
from twitchAPI.chat import ChatCommand
import logging

EVENTHANDLER = None


class CommandHandler(Module):
    async def help_command(self,cmd: ChatCommand):
        await EVENTHANDLER.send_message("help command")

    async def commands_list(self,cmd: ChatCommand):
        commandlist :str = ""
        for command in self.commands:
            commandlist += f"!{command} "
        for command in self.basic_commands:
            commandlist += f"!{command} "
        await EVENTHANDLER.send_message(commandlist)


    #basic handler for basic response commands
    async def basic_handler(self, cmd: ChatCommand):
        output = self.basic_commands[cmd.name]
        logging.info(f"CommandHandler: {cmd.name} command called")
        await EVENTHANDLER.send_message(output)
    
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
        
    #create commands for adding, removing, and editing commands
    async def add_command(self,cmd: ChatCommand):
        logging.info(f"CommandHandler: {cmd.name} command called")
        if len(cmd.parameter) == 0:
            await EVENTHANDLER.send_message("Please provide a command to add")
        else:
            res = cmd.parameter.split(' ', 1)
            if len(res) != 2:
                await EVENTHANDLER.send_message("Please provide a command and a response")
                return
            param1 = res[0]
            param2 = res[1]
            if param1 in self.basic_commands:
                await EVENTHANDLER.send_message("Command already exists")
                return
            self.basic_commands[param1] = param2
            EVENTHANDLER.TwitchAPI.CHAT.register_command(param1, self.basic_handler)
            await EVENTHANDLER.send_message(f"Command {param1} added")
            logging.info(f"CommandHandler.add_command: Params: '{param1}' || '{param2}'")

    async def remove_command(self,cmd: ChatCommand):
        logging.info(f"CommandHandler: {cmd.name} command called")
        if len(cmd.parameter) == 0:
            await EVENTHANDLER.send_message("Please provide a command to remove")
        else:
            result = self.basic_commands.pop(cmd.parameter, "failed")
            if result == "failed":
                await EVENTHANDLER.send_message("Command not found")
            else:
                EVENTHANDLER.TwitchAPI.CHAT.unregister_command(cmd.parameter)
                await EVENTHANDLER.send_message(f"Command {cmd.parameter} removed")
            logging.info(f"CommandHandler.remove_command: Params {cmd.parameter}")

    async def edit_command(self,cmd: ChatCommand):
        logging.info(f"CommandHandler: {cmd.name} command called")
        if len(cmd.parameter) == 0:
            await EVENTHANDLER.send_message("Please provide a command to edit")
        else:
            res = cmd.parameter.split(' ', 1)
            if len(res) != 2:
                await EVENTHANDLER.send_message("Please provide a command and a response")
                return
            param1 = res[0]
            param2 = res[1]
            self.basic_commands[param1] = param2
            logging.info(f"CommandHandler.edit_command: Params {cmd.parameter}")
            await EVENTHANDLER.send_message(f"Command {param1} edited")
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

    
    def __init__(self, eventHandler: EventHandler):
        super().__init__("CommandHandler" , eventHandler)
        global help, commands_list
        global EVENTHANDLER
        EVENTHANDLER = eventHandler
        self.commands = {}
        self.commands["help"] = self.help_command
        self.commands["commands"] = self.commands_list
        self.commands["add_command"] = self.add_command
        self.commands["remove_command"] = self.remove_command
        self.commands["edit_command"] = self.edit_command
        self.basic_commands = {}
        for command in self.commands:
            logging.info(f"CommandHandler: Added command: {command}")
            eventHandler.Add_command(command, self.commands[command])
        logging.info("CommandHandler module loaded")


