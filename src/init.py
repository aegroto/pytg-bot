import logging

from .BotManager import BotManager

logger = logging.getLogger(__name__) 

def initialize():
    logging.info("Initializing bot module...")

    BotManager.initialize()

def connect():
    logging.info("Connecting bot module...")

    load_manager().connect()

def load_manager():
    return BotManager.load() 

def main():
    # Start polling
    load_manager().updater.start_polling()
    logging.info("Polling.")

def depends_on():
    return ["config"]