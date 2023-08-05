
class NoRecordFoundException(Exception):
    """An exception raised when no record is found for a certain id"""

    def __init__(self, message='No record could be found based on your selection.'):
        self.message = message

    def __str__(self):
        return str(self.message)
