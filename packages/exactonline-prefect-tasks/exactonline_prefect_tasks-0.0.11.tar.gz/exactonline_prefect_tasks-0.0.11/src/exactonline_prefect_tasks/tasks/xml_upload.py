import json
import xmljson

import requests
from lxml import etree

from prefect.tasks.exactonline.api import Api
from prefect.tasks.exactonline.exceptions import MissingParametersException, ApiException, AuthException


def lambda_handler(event, context):
    """Lambda function to create a resource
    """

    if not ('division' in event) or event['division'] is None:
        raise MissingParametersException('Your request should provide a division.')

    if not ('module' in event) or event['module'] is None:
        raise MissingParametersException('Your request should provide a module.')

    if not ('data' in event) or event['data'] is None:
        raise MissingParametersException('Your request should provide data.')

    try:
        api = Api().get()
        xml_res = requests.post(
            'https://start.exactonline.nl/docs/XMLUpload.aspx?Topic=%s&_Division_=%s'
            % (event['module'], event['division']),
            data=etree.tostring(xmljson.badgerfish.etree(event['data'])[0]),
            headers={
                'Accept': 'application/xml',
                'Content-Type': 'application/xml',
                'Authorization': 'Bearer %s' % api.storage.get_access_token()
            }
        )
    except AuthException as e:
        print(e)
        raise e
    except Exception as e:
        print(e)
        raise ApiException(throwable=e)

    return json.loads(json.dumps(
        xmljson.badgerfish.data(
            etree.fromstring(
                xml_res.content
            )
        )
    ))


