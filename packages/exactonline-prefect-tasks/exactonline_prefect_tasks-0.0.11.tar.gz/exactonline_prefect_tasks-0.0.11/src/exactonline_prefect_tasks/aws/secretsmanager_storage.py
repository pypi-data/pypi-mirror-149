import os
import json
from configparser import NoOptionError, NoSectionError, ConfigParser
from time import time

from exactonline.storage import ExactOnlineConfig, MissingSetting


class SecretsManagerStorage(ExactOnlineConfig, ConfigParser):
    """
    Configuration based on the SafeConfigParser and the
    ExactOnlineConfig.

    Takes a Secret Manager Secret name as input and writes/reads that Secret
    """
    def __init__(self, secretsmanager_client, name, secret=None, **kwargs):
        super(SecretsManagerStorage, self).__init__(**kwargs)

        self.secretsmanager_client = secretsmanager_client
        self.name = name
        self.secret = secret

    def read_config(self):
        secret_response = self.secretsmanager_client.get_value()
        self.secret = json.loads(secret_response.get('SecretString'))
        self.read_dict(self.secret)

    def get(self, section, option, **kwargs):
        """
        Get method that raises MissingSetting if the value was unset.

        This differs from the SafeConfigParser which may raise either a
        NoOptionError or a NoSectionError.

        We take extra **kwargs because the Python 3.5 configparser extends the
        get method signature and it calls self with those parameters.

            def get(self, section, option, *, raw=False, vars=None,
                    fallback=_UNSET):
        """
        try:
            ret = super(ExactOnlineConfig, self).get(section, option, **kwargs)
        except (NoOptionError, NoSectionError):
            raise MissingSetting(option, section)

        return ret

    def set(self, section, option, value: str = None):
        """
        Set method that (1) auto-saves if possible and (2) auto-creates
        sections.
        """
        try:
            super(ExactOnlineConfig, self).set(section, option, value)
        except NoSectionError:
            self.add_section(section)
            super(ExactOnlineConfig, self).set(section, option, value)

        # Save automatically!
        # self.save()

    def save(self):
        if self.secret.get('transient'):
            if self.secret.get('transient').get('access_expiry'):
                if time() + 10 > float(self.secret.get('transient').get('access_expiry')):
                    if time() + 10 > float(self.get('transient', 'access_expiry')):
                        self.secretsmanager_client.put_value(secret_value=json.dumps({s: dict(self.items(s)) for s in self.sections()}))
