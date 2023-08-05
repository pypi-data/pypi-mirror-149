"""
Tasks for interacting with Exact Online.
"""
try:
    from exactonline.api import *
    from .exceptions import ApiException, AuthException, MissingParametersException, NoRecordFoundException
    from .aws import S3Storage, S3Client, SecretsManagerClient, SecretsManagerStorage
    from .tasks import Create, Read, GetById, GetAll, Search, Delete
except ImportError:
    raise ImportError(
        'Using `prefect.tasks.exactonline` requires Prefect to be installed with the "exactonline" extra.'
    )
