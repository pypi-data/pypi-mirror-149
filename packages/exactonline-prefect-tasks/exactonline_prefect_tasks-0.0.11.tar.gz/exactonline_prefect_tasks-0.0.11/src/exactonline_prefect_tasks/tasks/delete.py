from exactonline.resource import DELETE

from ..api import Api
from ..exceptions import ApiException, MissingParametersException, AuthException, NoRecordFoundException

from prefect import Task
from prefect.utilities.tasks import defaults_from_attrs

from typing import Any


class Delete(Task):
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
            raise MissingParametersException('Your request should provide an id.')

        try:
            api = Api().get()
            api.set_division(event['division'])
            api.restv1(
                DELETE('%s(guid\'%s\')' % (event['module'], event['id']))
            )
            return {}
        except AuthException as e:
            print(e)
            raise e
        except Exception as e:
            print(e)
            raise ApiException(throwable=e)
