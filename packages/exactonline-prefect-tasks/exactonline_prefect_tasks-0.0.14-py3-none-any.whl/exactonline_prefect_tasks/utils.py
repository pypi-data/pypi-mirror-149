import os
import json
from jsonmerge import merge


def load_configuration(path: str = None) -> dict:
    env = {
        'user_id': os.getenv('ZOHO_USER_ID'),
        'client_id': os.getenv('ZOHO_CLIENT_ID'),
        'client_secret': os.getenv('ZOHO_CLIENT_SECRET'),
        'refresh_token': os.getenv('ZOHO_REFRESH_TOKEN'),
        'region': os.getenv('ZOHO_DATA_CENTER')
    }

    config = merge(env, read_json_file(path))

    if 'user_id' not in config:
        demand_configuration(path, 'client_id', 'ZOHO_USER_ID')
    if 'client_id' not in config:
        demand_configuration(path, 'client_id', 'ZOHO_CLIENT_ID')
    if 'client_secret' not in config:
        demand_configuration(path, 'client_secret', 'ZOHO_CLIENT_SECRET')
    if 'refresh_token' not in config:
        demand_configuration(path, 'refresh_token', 'ZOHO_REFRESH_TOKEN')

    return config


def demand_configuration(path: str = None, key: str = None, env: str = None):
    raise Exception("Missing required config {}. Either:\n\
    1. Update {} in {}\n\
    2. Set {} in environment variables".format(key, key, path, env))


def read_json_file(path: str = None) -> dict:
    json_dict = {}
    if path:
        with open(path, "r", encoding="utf-8") as json_file:
            json_dict = json.load(json_file)

    return json_dict
