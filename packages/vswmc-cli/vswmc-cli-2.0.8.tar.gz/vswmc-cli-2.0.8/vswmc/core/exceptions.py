class VswmcError(Exception):
    """Base class for raised exceptions."""

    pass


class ConnectionFailure(VswmcError):
    """VSWMC is not or no longer available."""

    pass


class TimeoutError(VswmcError):
    """The operation exceeded the given deadline."""

    pass


class NotFound(VswmcError):
    """The resource was not found."""

    pass


class Unauthorized(VswmcError):
    """Unable to get access the resource."""

    pass
