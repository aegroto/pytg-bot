import logging

from pytg.load import manager

from .BotManager import BotManager

def initialize_manager():
    return BotManager() 

def main():
    # Start polling
    manager("bot").updater.start_polling()
    logging.info("Polling.")

def depends_on():
    return ["config"]