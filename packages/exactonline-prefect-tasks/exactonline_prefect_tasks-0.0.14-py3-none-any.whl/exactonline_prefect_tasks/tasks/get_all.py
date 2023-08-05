from exactonline.resource import GET

from ..api import Api
from ..exceptions import ApiException, MissingParametersException, AuthException, NoRecordFoundException

from prefect import Task
from prefect.utilities.tasks import defaults_from_attrs

from typing import Any


class GetAll(Task):
    def __init__(self, event: dict = None, **kwargs: Any):
        self.event = event
        super().__init__(**kwargs)

    @defaults_from_attrs("event")
    def run(self, event) -> dict:
        if not ('division' in event) or event['division'] is None:
            raise MissingParametersException('Your request should provide a division.')

        if not ('module' in event) or event['module'] is None:
            raise MissingParametersException('Your request should provide a module.')

        qs = ''
        if 'top' in event and not (event['top'] is None):
            qs = '$top=%d' % event['top']
        if 'select' in event and not (event['select'] is None):
            if qs:
                qs = qs + '&'
            qs = qs + ('$select=%s' % ','.join(event['select']))

        try:
            api = Api().get()
            api.set_division(event['division'])
            resources = api.restv1(GET('%s?%s' % (event['module'], qs)))
        except AuthException as e:
            print(e)
            raise e
        except Exception as e:
            print(e)
            raise ApiException(throwable=e)

        return resources

