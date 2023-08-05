from exactonline.resource import GET

from ..api import Api
from ..exceptions import ApiException, MissingParametersException, AuthException

from prefect import Task
from prefect.utilities.tasks import defaults_from_attrs

from typing import Any


class Read(Task):
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

        try:
            api = Api().get()
            api.set_division(event['division'])
            resource = api.restv1(GET('%s?%s=guid\'%s\'' %
                                      (event['module'], id_key, event['id'])))
        except AuthException as e:
            print(e)
            raise e
        except Exception as e:
            print(e)
            raise ApiException(throwable=e)

        return resource
