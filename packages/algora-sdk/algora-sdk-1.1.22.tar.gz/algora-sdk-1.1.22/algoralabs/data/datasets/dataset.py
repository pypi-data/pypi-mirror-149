import json
from typing import List, Dict, Any

from algoralabs.common.requests import __delete_request, __put_request, __post_request, __get_request
from algoralabs.data.datasets.models import DatasetSearchRequest, DatasetRequest
from algoralabs.data.transformations.response_transformers import no_transform
from algoralabs.decorators.data import data_request


@data_request(transformer=no_transform)
def get_dataset(id: str) -> Dict[str, Any]:
    endpoint = f"config/datasets/dataset/{id}"
    return __get_request(endpoint)


@data_request(transformer=no_transform)
def get_datasets() -> List[Dict[str, Any]]:
    endpoint = f"config/datasets/dataset"
    return __get_request(endpoint)


@data_request(transformer=no_transform)
def search_datasets(request: DatasetSearchRequest) -> List[Dict[str, Any]]:
    endpoint = f"config/datasets/dataset/search"
    return __post_request(endpoint, json=json.loads(request.json()))


@data_request(transformer=no_transform)
def create_dataset(request: DatasetRequest) -> Dict[str, Any]:
    endpoint = f"config/datasets/dataset"
    return __put_request(endpoint, json=json.loads(request.json()))


@data_request(transformer=no_transform)
def update_dataset(id: str, request: DatasetRequest) -> Dict[str, Any]:
    endpoint = f"config/datasets/dataset/{id}"
    return __post_request(endpoint, json=json.loads(request.json()))


@data_request(transformer=no_transform)
def delete_dataset(id: str) -> None:
    endpoint = f"config/datasets/dataset/{id}"
    return __delete_request(endpoint)
