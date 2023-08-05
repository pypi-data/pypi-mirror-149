import os
from configparser import NoOptionError, NoSectionError, ConfigParser

from exactonline.storage import ExactOnlineConfig, MissingSetting

from prefect.configuration import load_toml


class S3Storage(ExactOnlineConfig, ConfigParser):
    """
    Configuration based on the SafeConfigParser and the
    ExactOnlineConfig.

    Takes an S3 key as input and writes/reads that file
    """
    def __init__(self, key, config_path, s3_client, **kwargs):
        super(S3Storage, self).__init__(**kwargs)

        self.key = key
        self.config_path = config_path
        self.s3_client = s3_client

        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

        if hasattr(self.config_path, 'read'):
            self.overwrite = False
        else:
            self.overwrite = self.config_path

    def read_config(self):
        if hasattr(self.config_path, 'read'):
            if hasattr(self, 'read_file'):
                self.read_file(self.config_path)
            else:
                self.readfp(self.config_path)
        else:
            self.read([self.config_path])

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
        self.save()

    def save(self):
        if self.overwrite:
            with open(self.overwrite, 'w') as output:
                self.write(output)
            self.s3_client.upload_file(self.overwrite, self.key)
