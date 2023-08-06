class Error(Exception):
    """There was an ambiguous exception that occurred while handling your
    request.
        """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, kwargs)
        self._args = args
        self._kwargs = kwargs

    def __str__(self):
        return f'{self.__class__.__name__}\nargs: {self._args}\nkwargs: {self._kwargs}'


class AppError(Error):
    """All unrecoverable Exceptions inherit from this class"""


class ApiError(Error):
    """All Api Exceptions inherit from this class"""


class NotAuthorized(ApiError):
    """All Http Status 401 Exceptions inherit from this class"""
