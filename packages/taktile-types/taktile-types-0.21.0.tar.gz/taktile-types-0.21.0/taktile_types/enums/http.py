"""Enums about HTTP"""

from taktile_types.enums.common import ExtendedEnum


class Method(ExtendedEnum):
    """HTTP Methods"""

    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    CONNECT = "CONNECT"
    PATCH = "PATCH"
    TRACE = "TRACE"
    OPTIONS = "OPTIONS"
