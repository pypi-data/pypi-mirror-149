""" JSON Exceptions
"""


class JSONError(Exception):
    """Exception raised by the JSON validation."""

    def __init__(self, message):
        self.message = message
