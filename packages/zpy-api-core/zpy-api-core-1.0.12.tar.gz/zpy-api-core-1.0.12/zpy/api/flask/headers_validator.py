from flask.wrappers import Request
from typing import Optional, List

from zpy.api.http.header_validator import ZHeader, get_headers_or_raise


def flask_get_headers(
    request: Request,
    headers: List[str],
    throw: Optional[bool] = True,
    check_value: Optional[bool] = True,
    include_all: Optional[bool] = False,
    lower_headers: Optional[bool] = True,
) -> ZHeader:
    """
    Check if keys provided as headers are in the headers dict request

    :param request: Request flask
    :param throw : Raise exception if some header not found
    :param check_value: Verify header are in request and value is different of null or empty
    :param include_all: return all headers
    :param headers: headers key to validate
    :param lower_headers: Apply lower case to header name's
    :return: dict with headers
    """
    raw_headers: dict = dict(
        zip(request.headers.keys(lower_headers), request.headers.values())
    )
    return get_headers_or_raise(raw_headers, headers, throw, check_value, include_all)
