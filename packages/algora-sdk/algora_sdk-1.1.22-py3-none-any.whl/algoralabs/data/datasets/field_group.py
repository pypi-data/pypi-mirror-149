import json
from typing import Dict, List, Any

from algoralabs.common.requests import __delete_request, __post_request, __get_request, __put_request
from algoralabs.data.datasets.models import FieldGroupRequest
from algoralabs.data.transformations.response_transformers import no_transform
from algoralabs.decorators.data import data_request


@data_request(transformer=no_transform)
def get_field_group(id: str) -> Dict[str, Any]:
    endpoint = f"config/datasets/field-group/{id}"
    return __get_request(endpoint)


@data_request(transformer=no_transform)
def get_field_groups() -> List[Dict[str, Any]]:
    endpoint = f"config/datasets/field-group"
    return __get_request(endpoint)


@data_request(transformer=no_transform)
def create_field_group(request: FieldGroupRequest) -> Dict[str, Any]:
    endpoint = f"config/datasets/field-group"
    return __put_request(endpoint, json=json.loads(request.json()))


@data_request(transformer=no_transform)
def update_field_group(id: str, request: FieldGroupRequest) -> Dict[str, Any]:
    endpoint = f"config/datasets/field-group/{id}"
    return __post_request(endpoint, json=json.loads(request.json()))


@data_request(transformer=no_transform)
def delete_field_group(id: str) -> None:
    endpoint = f"config/datasets/field-group/{id}"
    return __delete_request(endpoint)
