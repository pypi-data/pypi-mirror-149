import json
import os
from time import time

from configparser import ConfigParser

from exactonline.api import ExactApi

from .exceptions import AuthException

from .aws import SecretsManagerStorage, SecretsManagerClient


from typing import Any


class Api:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        try:
            self.aws_config = read_config(os.getenv('AWS_CONFIG_FILE'))

            self.aws_access_key = self.aws_config.get('default').get('aws_access_key_id')
            self.aws_secret_key = self.aws_config.get('default').get('aws_secret_access_key')
            self.aws_secretsmanager_secret_name = os.getenv('AWS_SM_EXACT_ONLINE_SECRET_NAME')
            self.aws_secretsmanager_region = self.aws_config.get('secretsmanager').get('region')

            self.secretsmanager_client = SecretsManagerClient.get_instance(
                self.aws_access_key, self.aws_secret_key,
                region_name=self.aws_secretsmanager_region,
            )

            self.secretsmanager_client.name = self.aws_secretsmanager_secret_name

            self.api = ExactApi(storage=SecretsManagerStorage(secretsmanager_client=self.secretsmanager_client,
                                                              name=self.aws_secretsmanager_secret_name, secret=None))

            self.get_fresh_token()

        except Exception as e:
            raise AuthException(throwable=e)

    @staticmethod
    def get():
        try:
            Api._instance.get_fresh_token()
        except Exception as e:
            print(e)
            raise AuthException(throwable=e)

        return Api._instance.api

    def get_fresh_token(self):
        try:
            self.secretsmanager_client.get_value()
            self.api.storage.read_config()
        except Exception as e:
            print(e)
            raise AuthException(throwable=e)

        access_token = self.api.storage.get_access_token()

        try:
            if access_token is None or access_token == "":
                self.api.refresh_token()
            elif time() + 10 > Api._instance.api.storage.get_access_expiry():
                self.api.refresh_token()
        except:
            self.api.refresh_token()

        if Api._instance.api.storage.get_access_expiry() > time() and access_token != Api._instance.api.storage.get_access_token():
            self.secretsmanager_client.put_value(
                secret_value=json.dumps({s: dict(self.api.storage.items(s)) for s in self.api.storage.sections()}))


def read_config(filepath):
    """Read AWS configuration file"""
    config = ConfigParser()
    config.read(filepath)
    return {s: dict(config.items(s)) for s in config.sections()}
