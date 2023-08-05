
class ApiException(Exception):
    """An exception raised when a problem occurs while calling the API"""

    def __init__(self, message='An error occurred while calling the API.', throwable=None):
        self.message = message
        self.throwable = throwable

    def __str__(self):
        return str(self.message)

    def get_throwable(self):
        return self.throwable
