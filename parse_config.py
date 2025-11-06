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