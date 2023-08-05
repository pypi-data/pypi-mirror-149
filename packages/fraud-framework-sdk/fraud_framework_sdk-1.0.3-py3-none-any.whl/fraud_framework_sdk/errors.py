"""Errors that can be raised by this SDK"""


class FraudFrameworkClientError(Exception):
    """Base class for Client errors"""


class FraudFrameworkRequestError(FraudFrameworkClientError):
    """Error raised when there's a problem with the request that's being submitted."""


class FraudFrameworkApiError(FraudFrameworkClientError):
    """Error raised when FraudFramework does not send the expected response.
    Attributes:
        response (FraudFrameworkResponse): The FraudFrameworkResponse object containing all of the data sent back from the API.
    Note:
        The message (str) passed into the exception is used when
        a user converts the exception to a str.
        i.e. str(FraudFrameworkApiError("This text will be sent as a string."))
    """

    def __init__(self, message, response):
        msg = f"{message}\nThe server responded with: {response}"
        self.response = response
        super().__init__(msg)
