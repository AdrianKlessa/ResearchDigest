import configparser

def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def get_api_key()->str:
    config = get_config()
    return config['gemini']['api_key']