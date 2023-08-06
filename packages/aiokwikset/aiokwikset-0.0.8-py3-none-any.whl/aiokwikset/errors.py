"""Define package errors."""


class KwiksetError(Exception):
    """Define a base error."""

    pass


class RequestError(KwiksetError):
    """Define an error related to invalid requests."""

    pass
