from typing import Union, List, Dict, Any

from pandas import DataFrame

from algoralabs.common.requests import __get_request


def __base_request(extension: str, **kwargs):
    """
    Base GET request for IEX

    :param extension: URI extension
    :param kwargs: request query params
    :return: response
    """
    endpoint = f"data/datasets/query/iex/{extension}"
    return __get_request(endpoint=endpoint, params=kwargs)


def transform_one_or_many(data: Union[List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]], key: str) -> Union[
    DataFrame, Dict[str, DataFrame]]:
    if isinstance(data, dict):
        for s in data:
            data[s] = DataFrame(data[s][key])
        return data

    return DataFrame(data)
