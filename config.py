"""Coding challenge Config module"""
import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()
class Settings(BaseSettings):
    """Base Config"""
    ROOT_FOLDER: str
    SEARCH_FOLDER: str

    ROOT_FOLDER = os.getenv('ROOT_FOLDER')
    SEARCH_FOLDER = os.getenv('SEARCH_FOLDER')

settings = Settings()
