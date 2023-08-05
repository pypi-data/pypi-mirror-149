from typing import Dict, List, Tuple, Union, Any, Optional

from marshmallow.exceptions import ValidationError

from zpy.api.http.errors import BadRequest, ZHttpError
from zpy.utils.objects import ZObjectModel


def parse_request(
        request: dict, model: Union[ZObjectModel, Any], raise_err: bool = True
) -> Tuple[Optional[ZObjectModel], ZHttpError]:
    """
    Parse and validate request according model specification.

    @param request:
    @param model:
    @param raise_err:
    @return:
    """

    model_result: Union[List, ZObjectModel] = None
    errors: Union[List, None, BadRequest] = None
    try:
        if request is None or len(request.items()) == 0:
            error = BadRequest(
                "The request was not provided, validation request error",
                f"Missing fields {model().__missing_fields__} not provided",
            )
            if raise_err:
                raise error
            return None, error
        model_result = model(**request)
    except ValidationError as e:
        model_result = e.valid_data
        # if isinstance(e.messages, Dict):
        #     errors = [e.messages]
        # else:
        #     errors = e.messages
        errors = BadRequest(None, f"{e.messages}")
        if raise_err:
            raise errors
    return model_result, errors
