import logging
from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_htmx import htmx, htmx_init

Frontendlog: list[str] = []

router = APIRouter()

htmx_init(templates = Jinja2Templates(directory="templates"))

def construct_frontendlog():
    global Frontendlog
    out = []
    if Frontendlog == []:
        return {"log": ["log empty",""]}
    else:
        out = Frontendlog[::-1]
        if len(out) > 250:
            out = out[:250]
        return {"log": out}

@router.get("/log", response_class=HTMLResponse)
@htmx("frontendlog", "index", construct_frontendlog)
async def get_log(request: Request):
    pass


class tadaLogger():
    #set up logger
    def __init__(self):
        #clear the log file
        f = open('output.log', 'w')
        f.close()
        
        
        logFormatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8',
            level= logging.INFO
            )

        
        logging.info("Logger started")


    def gettime(self):
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def logwarning(self,caller:str, message:str):
        global Frontendlog
        logging.warning(f"{caller}:{message}")
        Frontendlog.append(f"warning: {caller}: {message}")
        
        logmessage = f"{self.gettime()} | warning: {caller}: {message}\n"
        f = open('output.log', 'a')
        f.write(logmessage)
        f.close()
    
    def loginfo(self,caller:str, message:str):
        global Frontendlog
        logging.info(f"{caller}:{message}")
        #Frontendlog.append(f"info: {caller}: {message}")
        
        logmessage = f"{self.gettime()} | info: {caller}: {message}\n"
        f = open('output.log', 'a')
        f.write(logmessage)
        f.close()
    
    def logerror(self,caller:str, message:str):
        global Frontendlog
        logging.error(f"{caller}:{message}")
        Frontendlog.append(f"error: {caller}: {message}")
        
        logmessage = f"{self.gettime()} | error: {caller}: {message}\n"
        f = open('output.log', 'a')
        f.write(logmessage)
        f.close()

    def logdebug(self,caller:str, message:str):
        global Frontendlog
        logging.debug(f"{caller}:{message}")
        #Frontendlog.append(f"debug: {caller}: {message}")
        
        logmessage = f"{self.gettime()} | debug: {caller}: {message}\n"
        f = open('output.log', 'a')
        f.write(logmessage)
        f.close()
    
    def eventtofrontend(self,caller:str, message:str):
        global Frontendlog
        Frontendlog.append(f"{caller}:{message}")


