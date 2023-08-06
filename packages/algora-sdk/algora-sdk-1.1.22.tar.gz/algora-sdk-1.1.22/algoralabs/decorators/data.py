import functools
import logging
from typing import Tuple, Dict, Any, Callable

import pandas as pd
from requests import Response

from algoralabs.common.errors import ApiError

logger = logging.getLogger(__name__)


def data_request(
        request: Callable = None,
        *,
        process_response=lambda response: response.json(),
        transformer=lambda data: pd.DataFrame(data)
) -> Callable:
    """
    """

    @functools.wraps(request)
    def decorator(f):
        @functools.wraps(f)
        def wrap(*args: Tuple, **kwargs: Dict[str, Any]) -> Any:
            """
            Wrapper for the decorated function

            Args:
                *args: args for the function
                **kwargs: keyword args for the function

            Returns:
                The output of the wrapped function
            """
            response: Response = f(*args, **kwargs)
            if response.status_code != 200 | response.status_code != 201:
                error = ApiError(
                    f"Request to {response.url} failed with status code {response.status_code}: {response.text}"
                )
                logger.error(error)
                raise error

            data = process_response(response)
            return transformer(data)

        return wrap

    if request is None:
        return decorator
    return decorator(request)
