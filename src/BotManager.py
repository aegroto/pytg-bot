import telegram, logging, time

from telegram.ext import Updater
from telegram.error import BadRequest, RetryAfter

from pytg.Manager import Manager
from pytg.load import manager

class BotManager(Manager):
    def __init__(self):
        super().__init__()
        settings = manager("config").load_settings("bot", "token")

        self.bot = telegram.Bot(settings["token"])
        self.updater = Updater(settings["token"], use_context=True)

        self.__logger = logging.getLogger("{} {}".format(__name__, id(self)))

    def safe_request(self, callback, max_tries=20, timeout_sleep=5.0):
        done = False
        tries = 0

        result = None

        while not done and tries < max_tries:
            tries += 1

            try:
                result = callback()

                done = True
            except BadRequest as e:
                if "Message is not modified" in str(e):
                    self.__logger.info("Skipping request as message hasn't changed ({})".format(str(e)))
                    done = True
                    break
                else:
                    self.__logger.info("Unhandled bad request error: " + str(e))
            except RetryAfter as e:
                self.__logger.info("Flood error, retrying in {}...".format(e.retry_after))

                time.sleep(e.retry_after)
            except Exception as e:
                self.__logger.info("Exception thrown: " + str(e))

                time.sleep(timeout_sleep)

            if not done:
                self.__logger.info("Retrying: {}/{}".format(tries, max_tries))

        if not done:
            self.__logger.warn("Failed to accomplish the request")
        
        return result