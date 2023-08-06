class ZbError(Exception):
    """
    The base class for all `Zb` specific errors.
    """

    def __init__(self, status, message):
        self.status = status
        self.message = message

    def __repr__(self) -> str:
        return f"{type(self).__name__}(" f"status={self.status}, " f"message={self.message})"


class ZbServerError(ZbError):
    """
    Represents a `Zb` specific 500 series HTTP error.
    """

    def __init__(self, status, message, headers):
        self.status = status
        self.message = message
        self.headers = headers


class ZbClientError(ZbError):
    """
    Represents a `Zb` specific 400 series HTTP error.
    """

    def __init__(self, status, message, headers):
        self.status = status
        self.message = message
        self.headers = headers


class ZbOperationError(ZbError):
    """
    Represents a `Zb` application logical error.
    """

    def __init__(self, status, message):
        self.status = status
        self.message = message


class ZbSpotOperationError(ZbError):
    """
    Represents a `Zb` application logical error.
    """

    def __init__(self, status, message):
        self.status = status
        self.message = message
