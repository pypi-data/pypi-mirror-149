from exactonline.resource import GET

from ..api import Api
from ..exceptions import ApiException, MissingParametersException, AuthException, NoRecordFoundException

from prefect import *
from prefect.utilities.tasks import defaults_from_attrs

from typing import Any


class GetById(Task):
    def __init__(self, event: dict = None, **kwargs: Any):
        self.event = event
        super().__init__(**kwargs)

    @defaults_from_attrs("event")
    def run(self, event) -> dict:
        if not ('division' in event) or event['division'] is None:
            raise MissingParametersException('Your request should provide a division.')

        if not ('module' in event) or event['module'] is None:
            raise MissingParametersException('Your request should provide a module.')

        if not ('id' in event) or event['id'] is None:
            raise MissingParametersException('Your request should provide an id to search for.')

        id_key = 'ID'
        if 'id_key' in event and not (event['id_key'] is None):
            id_key = event['id_key']

        qs = ''
        if 'top' in event and not (event['top'] is None):
            qs = '$top=%d' % event['top']
        if 'select' in event and not (event['select'] is None):
            if qs:
                qs = qs + '&'
            qs = qs + ('$select=%s' % ','.join(event['select']))

        if qs:
            qs = qs + '&'
        qs = qs + ('$filter=%s%%20eq%%20guid\'%s\'' % (id_key, event['id']))

        logger = prefect.context.get('logger')

        try:
            api = Api().get()
            api.set_division(event['division'])
            resources = api.restv1(GET('%s?%s' % (event['module'], qs)))
            logger.info('Instance access expiry: {} '.format(api.get_access_expiry()))
            logger.info('Access expiry: {} '.format(api.storage.get_access_expiry()))
        except AuthException as e:
            print(e)
            raise e
        except Exception as e:
            print(e)
            raise ApiException(throwable=e)

        if len(resources) < 1:
            raise NoRecordFoundException()

        return resources[0]
