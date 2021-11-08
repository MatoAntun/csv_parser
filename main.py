"""Bidnamic coding challenge script main"""
import sys
import os
import time
import logging

from watchdog.observers import Observer
from managers.monitor import CreatedHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Handle running script"""
    try:
        logger.info("Script started, enjoy :)")
        path = sys.argv[1] if len(sys.argv) > 1 else '.'
        event_handler = CreatedHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=False)
        observer.deamon = True
        observer.start()
        try:
            while True:
                time.sleep(20)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt inside watchdog observer")
            observer.stop()
        observer.join()

        if observer.is_alive():
            logging.info('still alive')
        else:
            logging.info('thread ending')

    except Exception as ex: #pylint: disable=broad-except
        logger.info(ex)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.warning('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0) # pylint: disable=protected-access
