"""This module contains API-related exceptions."""


class APIError(Exception):
    """An exception denoting generic API errors.

    This error is raised when the API returns invalid response data, like invalid JSON.
    """

    pass


class EmptyResponseError(APIError):
    """An exception denoting an empty API response.

    This error is raised when the API response content is empty, or it contains an empty JSON
    object.
    """

    pass
