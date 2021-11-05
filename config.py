"""Config file for manipulating .env"""
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Setting class for loading .env"""
    PROCESSED_FOLDER: str
    SEARCH_FOLDER: str

    PROCESSED_FOLDER = os.getenv('PROCESSED_FOLDER')
    SEARCH_FOLDER = os.getenv('SEARCH_FOLDER')

settings = Settings()