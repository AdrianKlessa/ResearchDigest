import configparser
from typing import List


def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def get_api_key()->str:
    config = get_config()
    return config['gemini']['api_key']

def get_interests()->List[str]:
    config = get_config()
    interests = config['topics']['research_interests']
    interests = interests.split(',')
    interests = [interest.strip() for interest in interests]
    return interests

def get_tesseract_path()->str:
    config = get_config()
    return config['tesseract']['tesseract_path']

def get_use_tesseract()->bool:
    config = get_config()
    return config.getboolean('tesseract', 'use_tesseract')

def get_papers_path()->str:
    config = get_config()
    return config['filepaths']['papers_path']

def get_reports_path()->str:
    config = get_config()
    return config['filepaths']['reports_path']