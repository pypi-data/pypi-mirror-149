from typing import Optional

import requests

from algoralabs.common.config import EnvironmentConfig
from algoralabs.decorators.authorization import authenticated_request


config = EnvironmentConfig()


@authenticated_request
def __get_request(
        endpoint: str,
        url_key: str = "algora",
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
):
    return requests.get(
        url=f"{config.get_url(url_key)}/{endpoint}",
        headers=headers or {},
        params=params,
        timeout=timeout
    )


@authenticated_request
def __put_request(
        endpoint: str,
        url_key: str = "algora",
        data=None,
        json=None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
):
    return requests.put(
        url=f"{config.get_url(url_key)}/{endpoint}",
        data=data,
        json=json,
        headers=headers or {},
        params=params,
        timeout=timeout
    )


@authenticated_request
def __post_request(
        endpoint: str,
        url_key: str = "algora",
        files=None,
        data=None,
        json=None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
):
    return requests.post(
        url=f"{config.get_url(url_key)}/{endpoint}",
        files=files,
        data=data,
        json=json,
        headers=headers or {},
        params=params,
        timeout=timeout
    )


@authenticated_request
def __delete_request(
        endpoint: str,
        url_key: str = "algora",
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
):
    return requests.delete(
        url=f"{config.get_url(url_key)}/{endpoint}",
        headers=headers or {},
        params=params,
        timeout=timeout
    )
