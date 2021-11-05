""""File manipulation manager"""
import os
import logging
from config import settings 
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileManager():
    """Methods for managing work with files"""

    def __init__(self) -> None: # currency:str
        """Constructors for file manager class"""
        self.file_path = settings.PROCESSED_FOLDER
        self.search_terms = settings.SEARCH_FOLDER
        self.currency = 'GBP'
        
    def check_folder_exist(self, folder_path:str) -> bool:
        """Check if file path exist if not create it"""
        if not os.path.exists(folder_path):
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
        if any([self.check_folder_exist(folder) for folder in folder_structure]):
            return True
        return False       
    
    def generate_filename(self) -> str:
        """Generate timestamp name"""
        date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
        return f"{date}.csv"
