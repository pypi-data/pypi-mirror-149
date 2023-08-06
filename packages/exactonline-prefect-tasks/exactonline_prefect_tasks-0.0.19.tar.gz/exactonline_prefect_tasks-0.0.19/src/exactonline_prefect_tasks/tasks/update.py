from exactonline.resource import PUT

from prefect.tasks.exactonline.api import Api
from prefect.tasks.exactonline.exceptions import MissingParametersException, ApiException, AuthException


def lambda_handler(event, context):
    """Lambda function to update a resource
    """

    if not ('division' in event) or event['division'] is None:
        raise MissingParametersException('Your request should provide a division.')

    if not ('module' in event) or event['module'] is None:
        raise MissingParametersException('Your request should provide a module.')

    if not ('id' in event) or event['id'] is None:
        raise MissingParametersException('Your request should provide an id.')

    if not ('data' in event) or event['data'] is None:
        raise MissingParametersException('Your request should provide data.')

    try:
        api = Api().get()
        api.set_division(event['division'])
        api.restv1(
            PUT('%s(guid\'%s\')' % (event['module'], event['id']), event['data'])
        )
        return {}
    except AuthException as e:
        print(e)
        raise e
    except Exception as e:
        print(e)
        raise ApiException(throwable=e)
