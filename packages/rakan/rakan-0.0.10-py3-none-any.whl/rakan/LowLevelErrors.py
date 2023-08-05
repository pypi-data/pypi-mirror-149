class BadRequest(Exception):
    def __init__(self, message='Error code 400: there is a syntax error in the request and the request has therefore been denied.') -> None:
        super().__init__(message)


class Unauthorized(Exception):
    def __init__(self, message='Error code 401: the request being made did not contain the necessary authentication credentials and therefore the client was denied access.') -> None:
        super().__init__(message)


class Forbidden(Exception):
    def __init__(self, message='Error code 403: the server understood the request but refuses to authorize it.') -> None:
        super().__init__(message)


class NotFound(Exception):
    def __init__(self, message='Error code 404: the server has not found a match for the API request being made.') -> None:
        super().__init__(message)


class UnsupportedMediaType(Exception):
    def __init__(self, message='Error code 415: the server is refusing to service the request because the body of the request is in a format that is not supported.') -> None:
        super().__init__(message)


class RateLimiExceeded(Exception):
    def __init__(self, message='Error code 429: the application has exhausted its maximum number of allotted API calls allowed for a given duration.') -> None:
        super().__init__(message)


class InternalServerError(Exception):
    def __init__(self, message='Error code 500: an unexpected condition or exception which prevented the server from fulfilling an API request.') -> None:
        super().__init__(message)


class ServiceUnavailable(Exception):
    def __init__(self, message='Error code 503: the server is currently unavailable to handle requests because of an unknown reason.') -> None:
        super().__init__(message)


class UnknowError(Exception):
    def __init__(self, message='I have no clue of what happened. You\'re fucked.') -> None:
        super().__init__(message)


class NoMMRData(Exception):
    def __init__(self, message='No recent MMR data is available.') -> None:
        super().__init__(message)
