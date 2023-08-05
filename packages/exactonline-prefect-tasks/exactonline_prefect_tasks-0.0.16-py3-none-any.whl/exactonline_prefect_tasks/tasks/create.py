from exactonline.resource import POST

from ..api import Api
from ..exceptions import ApiException, MissingParametersException, AuthException, NoRecordFoundException

from prefect import Task
from prefect.utilities.tasks import defaults_from_attrs

from typing import Any


class Create(Task):
    def __init__(self, event: dict = None, **kwargs: Any):
        self.event = event
        super().__init__(**kwargs)

    @defaults_from_attrs("event")
    def run(self, event) -> dict:
        if not ('division' in event) or event['division'] is None:
            raise MissingParametersException('Your request should provide a division.')

        if not ('module' in event) or event['module'] is None:
            raise MissingParametersException('Your request should provide a module.')

        if not ('data' in event) or event['data'] is None:
            raise MissingParametersException('Your request should provide data.')

        try:
            api = Api().get()
            api.set_division(event['division'])
            resource = api.restv1(POST(event['module'], event['data']))
            resource.update(event['data'])
        except AuthException as e:
            print(e)
            raise e
        except Exception as e:
            print(e)
            raise ApiException(throwable=e)

        return resource
