"""Monitor manager for events"""
import os
import logging
import time

from datetime import datetime
import pandas
from watchdog.events import FileSystemEventHandler

from managers.process import CsvProcessing

logger = logging.getLogger(__name__)

class CreatedHandler(FileSystemEventHandler):
    """Override class for handling on create """

    def process(self, filename: str) -> None:#pylint: disable=no-self-use
        """Process created .csv"""
        try:
            file_name = os.path.normpath(filename)
            if self.check_created_size(file_name):
                CsvProcessing(file_name).parse_csv()
        except pandas.errors.ParserError as pdex:
            logger.error(str(pdex))
        except Exception as ex: #pylint: disable=broad-except
            logger.error("Problems with processing .csv %s", str(ex))
        logger.info("File finished processing")

    def on_created(self, event:object) -> str: #pylint: disable=inconsistent-return-statements
        """Watchdog event on_created returns created file"""
        try:
            if event.is_directory:
                logger.info("Created folder")
                return
            _, ext = os.path.splitext(event.src_path)
            logger.info("Created file %s", {event.src_path})
            if ext == '.csv':
                self.process(event.src_path)
            return event.src_path
        except Exception as ex: #pylint: disable=broad-except
            logger.error("File probably deleted while processing %s", str(ex))

    @staticmethod
    def check_created_size(filename) -> bool:
        """Checking file size if stable return True"""
        # Watchdog does not have the implementation to check if the file is created or still creating
        # So we are checking file size if it is stable for some time we are taking it as created
        old_size = -1
        while old_size != os.path.getsize(filename):
            old_size = os.path.getsize(filename)
            time.sleep(1)
        return True
