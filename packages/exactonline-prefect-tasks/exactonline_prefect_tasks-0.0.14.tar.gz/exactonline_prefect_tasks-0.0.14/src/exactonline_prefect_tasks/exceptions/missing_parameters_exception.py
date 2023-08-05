
class MissingParametersException(Exception):
    """An exception raised when the incoming request misses some required parameters"""

    def __init__(self, message='Some required parameters are missing in your request.'):
        self.message = message

    def __str__(self):
        return str(self.message)
