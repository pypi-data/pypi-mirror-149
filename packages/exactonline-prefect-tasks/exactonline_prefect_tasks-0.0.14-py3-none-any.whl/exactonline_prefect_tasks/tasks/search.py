from exactonline.resource import GET

import urllib.parse
from ..api import Api
from ..exceptions import ApiException, MissingParametersException, AuthException, NoRecordFoundException

from prefect import Task
from prefect.utilities.tasks import defaults_from_attrs

from typing import Any


class Search(Task):
    def __init__(self, event: dict = None, **kwargs: Any):
        self.event = event
        super().__init__(**kwargs)

    @defaults_from_attrs("event")
    def run(self, event) -> dict:
        if not ('division' in event) or event['division'] is None:
            raise MissingParametersException('Your request should provide a division.')

        if not ('module' in event) or event['module'] is None:
            raise MissingParametersException('Your request should provide a module.')

        if not ('criteria' in event) or event['criteria'] is None:
            raise MissingParametersException('Your request should provide a criteria to search for.')

        qs = ''
        if 'top' in event and not (event['top'] is None):
            qs = '$top=%d' % event['top']
        if 'select' in event and not (event['select'] is None):
            if qs:
                qs = qs + '&'
            qs = qs + ('$select=%s' % ','.join(event['select']))

        if qs:
            qs = qs + '&'
        criteria = self.parse_criteria(event['criteria'])
        qs = qs + ('$filter=%s' % criteria)

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

    @staticmethod
    def safe_str(obj):
        try:
            return str(obj)
        except UnicodeEncodeError:
            return obj.encode('utf8', 'ignore').decode('utf8')
        except:
            return ""

    def parse_criteria(self, obj):
        if '$and' in obj:
            criteria_str = "%20and%20".join('(' + self.parse_criteria(c) + ')' for c in obj['$and'])
        elif '$or' in obj:
            criteria_str = "%20or%20".join('(' + self.parse_criteria(c) + ')' for c in obj['$or'])
        else:
            field = next(iter(obj))
            op = next(iter(obj[field]))
            criteria_str = field + '%20' + op + '%20' + urllib.parse.quote(obj[field][op])

        return criteria_str
