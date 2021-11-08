""""File manipulation manager"""
import os
import logging
from datetime import datetime

from config import settings

logger = logging.getLogger(__name__)

class FileManager():#pylint: disable=no-self-use
    """Methods for managing work with files"""

    def __init__(self, currency:str) -> None:
        """Constructors for file manager class"""
        self.file_path = settings.ROOT_FOLDER
        self.search_terms = settings.SEARCH_FOLDER
        self.currency = currency

    def check_folder_exist(self, folder_path:str) -> bool:
        """Check if file path exist if not create it"""
        norm_path = os.path.normpath(folder_path)
        if not os.path.exists(norm_path):
            try:
                os.makedirs(folder_path)
            except OSError as os_error:
                logger.error(str(os_error))
                raise os_error
        return True

    def check_processed_path(self) -> bool:
        """Check if root folder and folder for data exist"""
        folder_structure = [
            self.file_path,
            f"{self.file_path}/{self.currency}",
            f"{self.file_path}/{self.currency}/{self.search_terms}"
            ]
        if any([self.check_folder_exist(folder) for folder in folder_structure]):#pylint: disable=(use-a-generator)
            return True
        return False

    def generate_filename(self) -> str:
        """Generate timestamp name"""
        # ISO 8601 standard for timestamp
        date = datetime.now().strftime("%Y%m%dT%H%M%S")
        return f"{date}.csv"

    def generated_filepath(self) -> str:
        """Generate complete filepath"""
        return f"./{self.file_path}/{self.currency}/{self.search_terms}/{self.generate_filename()}"
