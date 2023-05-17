import vk_api
import random
import time
import datetime
import calendar

from Technical import logger  # the logger file

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType  # VK Api
import tokens  # tokens. There are main_token and VKGroupID.
from Database import database  # database
from Messaging import for_chat  # for work with the chat
from Messaging import for_user  # for work with the user
from Technical import variables  # some variables: admins, chats_to_notify, about_system, help
from Config import config_work  # for work with config
from financial_system import taxSystem  # for work with tax system from financial system
from Technical import technical  # technical: sender reports to the special chat and the user notification system
from paths import database_path, config_path, logs_path
from Systems import commands


vk_session = vk_api.VkApi(token = tokens.main_token)

longpoll = VkBotLongPoll(vk_session, tokens.VKGroupID)

logger = logger.get_logger(__name__, logs_path)

configWork = config_work.configWork(logger, config_path)

db = database.DataBase(None, None, logger, database_path)

technical = technical.technical(vk_session, logger, db)

ts = taxSystem(logger, technical, database_path)

# Setting variables
admins = variables.admins
chats_to_notify = variables.chats_to_notify
about_system = variables.about_system
help = variables.help


# Log the start.
logger.info("Start!")  # Logger
print("Start!")

# Work with calendar: set the first day in week (Monday).
calendar.setfirstweekday(0)

# Print the notification about the turning of the system.
if configWork.readValue("Settings", "DoNotificateChats") == "True":
    for chat_to_notify in chats_to_notify:
        vk_session.method("messages.send", {"peer_id" : chat_to_notify, "message" : "Система включена. 😊", "random_id" : 0})
    
    logger.info("Notificate the chats.")  # Logger


# The main block of the system.
while True:

    # Set the time and collect the taxes.
    try:
        d = datetime.datetime.today()
    
        # Collect the taxes in time and check that we haven`t already collect it.
        if calendar.weekday(d.year, d.month, d.day) == 6:
            if (d.hour == 12) and (d.minute in range(59)):
                if configWork.readValue("Finance", "WasTaxCollection") == "False":

                    ts.tax_collection_for_individuals(configWork.readValue("Variables", "TaxIndividualCitizen"), configWork.readValue("Variables", "TaxTndividualMigrant"))
                    configWork.changeValue("Finance", "WasTaxCollection", "True")
    
        
        # This is in order to carry out tax collection once on Sunday.
        if calendar.weekday(d.year, d.month, d.day) == 5:
            if configWork.readValue("Finance", "WasTaxCollection") == "True":
                
                configWork.changeValue("Finance", "WasTaxCollection", "False")
                logger.info("Didn`t collect the taxes, because it was already collected yesterday.")  # Logger


    except Exception as e:
        logger.exception(f"Failed with exit code: 1;")
        technical.senderTechnical(e, datetime.datetime.today())  # send to the special chat the info. e - exception and the datatime.


    try:

        for event in longpoll.listen():

            if event.type == VkBotEventType.MESSAGE_NEW:

                # If the message from the chat.
                if event.object.message['peer_id'] != event.object.message['from_id']:

                    msg = event.object.message['text'].split()
                    id = event.object.message['peer_id'] 
                    user_id = event.object.message['from_id']

                    logger.info(f"New message from the chat {user_id} by {id}: {msg}")  # Logger

                    for_chat.forChat(msg, id, user_id, db, vk_session, longpoll, admins, about_system, configWork, logger, technical, help, ts, commands)


                # If the message from the user.
                elif event.object.message['peer_id'] == event.object.message['from_id']:

                    msg = event.object.message['text'].split()
                    id = event.object.message['from_id'] 

                    logger.info(f"New message from the user {id}: {msg}")  # Logger

                    for_user.forUser(msg, id, db, vk_session, longpoll, admins, about_system, configWork, logger, technical, help, ts, commands)


    # If something went wrong
    except Exception as e: 
        logger.exception(f"Failed with exit code: 1; \nEB: bot.py/001")
        technical.senderTechnical(e, datetime.datetime.today())  # send to the special chat the info. e - exception and the datatime.